import uuid
import datetime

from jose import jwt
from jose import JWTError

from ..core.config import settings


class JWTTokensMixin:
    @staticmethod
    async def generate_token(
        user_id: uuid.uuid4,
        refresh: bool = False,
    ) -> str:
        expire = settings.jwt.refresh_token_expire if refresh else settings.jwt.access_token_expire
        expire_timedelta = datetime.timedelta(minutes=expire)
        expire_time = datetime.datetime.utcnow() + expire_timedelta

        claims = {
            "exp": expire_time,
            "sub": str(user_id),
        }
        if refresh:
            claims["refresh"] = True

        encoded_jwt = jwt.encode(
            claims=claims,
            key=settings.jwt.secret_key,
            algorithm=settings.jwt.algorithm,
        )
        return encoded_jwt

    async def generate_access_token(self, user_id: uuid.uuid4) -> str:
        return await self.generate_token(user_id)

    async def generate_refresh_token(self, user_id: uuid.uuid4) -> str:
        return await self.generate_token(user_id, refresh=True)

    async def generate_tokens_for_user(self, user_id: uuid.uuid4) -> dict:
        return {
            "access_token": await self.generate_access_token(user_id),
            "refresh_token": await self.generate_refresh_token(user_id),
            "token_type": "bearer",
        }

    async def is_token_valid_bearer(self, jwt_token: str) -> bool:
        if jwt_token.startswith("Bearer ") or jwt_token.startswith("bearer "):
            return True
        return False

    async def get_decoded_token(self, jwt_token: str) -> dict | None:
        return jwt.decode(
            jwt_token,
            settings.jwt.secret_key,
            algorithms=[settings.jwt.algorithm],
        )

    async def check_token_exp_valid(self, decoded_token: dict) -> bool:
        try:
            exp = decoded_token["exp"]
            current_time = datetime.datetime.utcnow()
            if current_time < datetime.datetime.utcfromtimestamp(exp):
                return True
            else:
                return False
        except JWTError:
            return False
        except (Exception,):
            return False

    async def is_token_valid(
        self,
        jwt_token: str,
        check_refresh: bool = False,
    ) -> bool:
        try:
            decoded_token = await self.get_decoded_token(jwt_token)
            token_exp_valid = await self.check_token_exp_valid(decoded_token)
            if not token_exp_valid:
                return False
            if check_refresh and not decoded_token.get("refresh"):
                return False
            return True
        except JWTError:
            return False
        except (Exception,):
            return False

    async def get_jwt_token_data(
        self,
        jwt_token: str,
        check_bearer: bool = True,
    ) -> dict | None:
        try:
            if check_bearer:
                if await self.is_token_valid_bearer(jwt_token):
                    jwt_token = jwt_token.split("Bearer ")[1].strip()
                else:
                    return None
            decoded_token = await self.get_decoded_token(jwt_token)
            exp = decoded_token["exp"]
            current_time = datetime.datetime.utcnow()
            if current_time < datetime.datetime.utcfromtimestamp(exp):
                return decoded_token
            else:
                return None
        except JWTError:
            return None
