from sqlalchemy.exc import SQLAlchemyError

from ..auth.hashing import Hashing
from ..services.base import BaseService
from ..auth.models import User
from .schemas import AdminAuthSchema
from .schemas import AdminCreateSchema
from .dataclasses import AdminCreateData


class AdminAuthService(BaseService):
    async def validate_user_credentials(self, data: AdminAuthSchema) -> bool:
        async with self.uow:
            user: User = await self.uow.user.get_by_username(data.username)
            if not user or not user.check_password(data.password) or not user.is_superuser:
                return False
            return True

    async def create_admin(self, data: AdminCreateSchema) -> AdminCreateData:
        async with self.uow:
            try:
                if await self.uow.user.exists_by_username(data.username):
                    return AdminCreateData(
                        created=False,
                        error="User with provided username already exists",
                    )
                data = {
                    "username": data.username,
                    "hashed_password": Hashing.get_hashed_password(data.password),
                    "is_superuser": True,
                }
                await self.uow.user.insert_by_data(data)
                await self.uow.commit()
            except SQLAlchemyError as e:
                return AdminCreateData(created=False, error=str(e))
        return AdminCreateData(created=True)
