from starlette.datastructures import UploadFile

from ..services.base import BaseService
from ..core.config import settings
from ..media_helper import MediaFilesUploadHelper
from .models import User
from .hashing import Hashing
from .schemas import UserCreateSchema
from .schemas import UserAuthBaseSchema
from .schemas import UserReturnSchema
from .dataclasses import UserAuthData
from .dataclasses import CoverImageSetData
from .mixins import JWTTokensMixin


class UserService(JWTTokensMixin, BaseService):
    async def create_user(self, data: UserCreateSchema) -> UserAuthData:
        async with self.uow:
            if await self.uow.user.exists_by_username(data.username):
                return UserAuthData(error="User with this username already exists!")
            data = {
                "username": data.username,
                "hashed_password": Hashing.get_hashed_password(data.password),
            }
            user_id = await self.uow.user.insert_by_data(data)
            await self.uow.commit()
            return UserAuthData(
                tokens=await self.generate_tokens_for_user(user_id),
            )

    async def authenticate_user(self, data: UserAuthBaseSchema) -> UserAuthData:
        async with self.uow:
            user = await self.uow.user.get_by_username(data.username)
            if user is None:
                return UserAuthData(error="User with this username does not exist!")
            if not Hashing.verify_password(data.password, user.hashed_password):
                return UserAuthData(error="Incorrect password!")
            return UserAuthData(tokens=await self.generate_tokens_for_user(user.id))

    async def get_user_by_jwt_token(
        self,
        token: str,
        check_bearer: bool = True,
    ) -> User | None:
        token_data = await self.get_jwt_token_data(token, check_bearer)
        if token_data:
            try:
                user_id = token_data["sub"]
            except KeyError:
                return None

            async with self.uow:
                user = await self.uow.user.get_by_id(user_id)
                if not user:
                    return None
                await self.uow.expunge(user)
                return user

    async def get_user_profile_data(self, user: User) -> UserReturnSchema:
        return UserReturnSchema(
            username=user.username,
            cover_image=user.cover_image if user.cover_image else settings.user_default_avatar_url,
        )

    async def set_cover_image(self, user: User, image_file: UploadFile) -> CoverImageSetData:
        async with self.uow:
            cover_image_path, error = await MediaFilesUploadHelper(image_file).save_upload_file()
            if not error:
                user.cover_image = cover_image_path
                await self.uow.add(user)
                await self.uow.commit()
                return CoverImageSetData(success=True)
            return CoverImageSetData(error=error)

    async def verify_user_token(self, token: str) -> bool:
        token_valid = await self.is_token_valid(token)
        if not token_valid:
            return False
        async with self.uow:
            user = await self.get_user_by_jwt_token(token, check_bearer=False)
            if not user:
                return False
            return True

    async def get_user_access_token_from_refresh(self, token: str) -> str | None:
        token_valid = await self.is_token_valid(token, check_refresh=True)
        if not token_valid:
            return None
        async with self.uow:
            user = await self.get_user_by_jwt_token(token, check_bearer=False)
            if not user:
                return None
            return await self.generate_access_token(user.id)
