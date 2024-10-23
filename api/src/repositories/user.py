from typing import Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.models import User
from .generic import GenericRepository


class UserRepository(GenericRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_user_by_id(self, user_id: uuid4) -> Optional[User]:
        return await self.get_by_id(user_id)

    async def exists_by_column(self, column, value: str) -> bool:
        return await self.exists_by_cond([column == value])

    async def exists_by_username(self, username: str) -> bool:
        return await self.exists_by_column(User.username, username)

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.get_one_by_cond([User.username == username])
