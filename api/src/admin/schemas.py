from pydantic import Field
from pydantic import BaseModel
from pydantic import field_validator


class AdminAuthSchema(BaseModel):
    username: str
    password: str


class AdminCreateSchema(BaseModel):
    username: str = Field(..., min_length=4)
    password: str = Field(..., min_length=4)
    password_confirm: str

    @field_validator("password_confirm")
    def validate_password_confirm(cls, value, values):
        if value != values.data.get("password"):
            raise ValueError("Passwords do not match")
        return value
