from pydantic import BaseModel
from pydantic import field_validator

from typing import Optional

from ..core.schemas import MainSchema
from .validators import validate_password


class UserReturnSchema(MainSchema):
    username: str
    cover_image: str


class UserAuthBaseSchema(BaseModel):
    username: str
    password: str


class UserCreateSchema(UserAuthBaseSchema):
    password_confirm: str

    @field_validator("password")
    def validate_password(cls, value):
        validation_data = validate_password(value)
        if validation_data.error is not None:
            raise ValueError(validation_data.error)
        return value

    @field_validator("password_confirm")
    def validate_password_confirm(cls, value, values):
        if value != values.data.get("password"):
            raise ValueError("Passwords do not match")
        return value


class JWTTokensSchema(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None


class TokenVerifyOrRefreshSchema(BaseModel):
    token: str
