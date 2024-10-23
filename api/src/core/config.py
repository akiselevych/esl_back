import os

from functools import lru_cache

from typing import Union
from typing import Optional

from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator
from pydantic_settings import BaseSettings

from dotenv import load_dotenv


DEV_DOTENV: str = ".env.dev"
PROD_DOTENV: str = ".env.prod"


def load_environment():
    # Load the main .env file
    load_dotenv(dotenv_path=".env")

    # Determine the environment based on the DEBUG flag
    debug_mode: bool = os.getenv("DEBUG", "True") == "True"
    env_file: str = DEV_DOTENV if debug_mode else PROD_DOTENV

    try:
        load_dotenv(dotenv_path=env_file)
    except IOError:
        raise ValueError(f"Could not load environment file {env_file}")


class DotenvListHelper:
    @classmethod
    def assemble_list(cls, v: str) -> list[str]:
        if isinstance(v, str) and v.startswith("[") and v.endswith("]"):
            return [i.strip().strip("[]") for i in v.split(",")]
        raise ValueError(v)


class CorsSettings(BaseSettings):
    origins: str = Field(alias="cors_origins")

    @field_validator("origins")
    def assemble_cors_origins(cls, v: str) -> list[str]:
        return DotenvListHelper.assemble_list(v)


class DatabaseSettings(BaseSettings):
    name: str = Field(alias="db_name")
    user: str = Field(alias="db_user")
    password: str = Field(alias="db_password")
    host: str = Field(alias="db_host")
    port: int = Field(alias="db_port")
    url: Optional[str] = Field(default=None, alias="database_url")  # DBAPI URL

    @staticmethod
    def _get_default_db_url(connection_data: dict[str, int]) -> str:
        db_user = connection_data["db_user"]
        db_password = connection_data["db_password"]
        db_host = connection_data["db_host"]
        db_port = connection_data["db_port"]
        db_name = connection_data["db_name"]

        connection = f"{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return f"postgresql+asyncpg://{connection}?async_fallback=true"

    @model_validator(mode="before")
    def get_database_url(cls, values: dict[str, int]) -> dict[str, int]:
        if not values.get("database_url"):
            values["database_url"] = cls._get_default_db_url(values)
        return values


class JWTSettings(BaseSettings):
    access_token_expire: int = Field(alias="access_token_expire_minutes")
    refresh_token_expire: int = Field(alias="refresh_token_expire_minutes")
    algorithm: str = Field(alias="jwt_algorithm")
    secret_key: str = Field(alias="jwt_secret_key")


class Settings(BaseSettings):
    app_name: str = "Project API"
    app_version: Union[int, float] = 1
    debug: bool = True
    domain: str = "localhost:8000"
    domain_protocol: str = "http"
    secret_key: str

    # MEDIA FILES
    media_root: str = "media"
    media_mount_name: str = "media"
    media_url: str = "/media/"
    media_allowed_formats: str = "[png, jpg, jpeg]"  # str representation of list in .env file

    # STATIC FILES
    static_root: str = "static"
    static_mount_name: str = "static"
    static_url: str = "/static/"

    # USER DEFAULT AVATAR
    user_default_avatar_name: str = "default_avatar"  # without extension
    user_default_avatars_dir: str = "avatars"  # only dir name (not a path)
    user_default_avatar_extension: str = "png"

    # CORS SETTINGS
    cors: CorsSettings = Field(default_factory=CorsSettings)

    # DATABASE
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)

    # JWT
    jwt: JWTSettings = Field(default_factory=JWTSettings)

    @property
    def domain_url(self) -> str:
        return f"{self.domain_protocol}://{self.domain}"

    @property
    def full_media_url(self) -> str:
        return f"{self.domain_url}{self.media_url}"

    @property
    def full_static_url(self) -> str:
        return f"{self.domain_url}{self.static_url}"

    @property
    def user_default_avatar_url(self) -> str:
        path = self.full_static_url + self.user_default_avatars_dir
        return f"{path}/{self.user_default_avatar_name}.{self.user_default_avatar_extension}"

    @field_validator("media_allowed_formats")
    def assemble_media_allowed_formats(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        formats = DotenvListHelper.assemble_list(v)
        return [format.lower() for format in formats]


@lru_cache()
def get_settings() -> Settings:
    load_environment()
    return Settings()


settings = get_settings()
