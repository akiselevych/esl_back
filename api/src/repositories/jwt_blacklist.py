from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.models import JWTBlackList
from .generic import GenericRepository


class JWTBlackListRepository(GenericRepository[JWTBlackList]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, JWTBlackList)

    async def get_token_by_id(self, token_id: int) -> Optional[JWTBlackList]:
        return await self.get_by_id(token_id)
