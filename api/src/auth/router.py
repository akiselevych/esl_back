from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import Header
from fastapi import status
from fastapi import File

from typing import Annotated

from ..db.dependencies import uowDEP
from .schemas import UserCreateSchema
from .schemas import JWTTokensSchema
from .schemas import UserAuthBaseSchema
from .schemas import UserReturnSchema
from .schemas import TokenVerifyOrRefreshSchema
from .service import UserService
from .exceptions import AuthException
from .exceptions import CredentialsException
from .exceptions import FileTypeException
from .exceptions import JWTTokenException


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=JWTTokensSchema)
async def user_register(
    data: UserCreateSchema,
    uow: uowDEP,
) -> JWTTokensSchema:
    create_data = await UserService(uow).create_user(data)
    if create_data.error:
        raise AuthException(error=create_data.error)
    return JWTTokensSchema(**create_data.tokens)


@router.post("/login/", status_code=status.HTTP_200_OK, response_model=JWTTokensSchema)
async def user_login(
    data: UserAuthBaseSchema,
    uow: uowDEP,
) -> JWTTokensSchema:
    auth_data = await UserService(uow).authenticate_user(data)
    if auth_data.error:
        raise AuthException(error=auth_data.error)
    return JWTTokensSchema(**auth_data.tokens)


@router.post("/token_verify/", status_code=status.HTTP_200_OK, response_model=bool)
async def verify_token(data: TokenVerifyOrRefreshSchema, uow: uowDEP) -> bool:
    return await UserService(uow).verify_user_token(data.token)


@router.post(
    "/access_token_from_refresh/", status_code=status.HTTP_200_OK, response_model=JWTTokensSchema
)
async def access_token_from_refresh(
    data: TokenVerifyOrRefreshSchema, uow: uowDEP
) -> JWTTokensSchema:
    token = await UserService(uow).get_user_access_token_from_refresh(data.token)
    if not token:
        raise JWTTokenException(error="Could not get access token from refresh")
    return JWTTokensSchema(access_token=token, token_type="bearer")


@router.get("/profile/", status_code=status.HTTP_200_OK, response_model=UserReturnSchema)
async def user_profile(
    uow: uowDEP,
    authorization: Annotated[str | None, Header()] = None,
):
    if authorization:
        user = await UserService(uow).get_user_by_jwt_token(authorization)
        if not user:
            raise CredentialsException()
        return await UserService(uow).get_user_profile_data(user)
    else:
        raise CredentialsException()


@router.put("/profile/change_cover/", status_code=status.HTTP_204_NO_CONTENT)
async def user_change_cover(
    uow: uowDEP,
    authorization: Annotated[str | None, Header()] = None,
    image_file: UploadFile = File(...),
):
    if authorization:
        user = await UserService(uow).get_user_by_jwt_token(authorization)
        if not user:
            raise CredentialsException()
        success, error = await UserService(uow).set_cover_image(user, image_file)
        if not success:
            raise FileTypeException(error=error)
    else:
        raise CredentialsException()
