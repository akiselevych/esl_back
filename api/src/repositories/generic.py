import uuid

from typing import Generic
from typing import TypeVar
from typing import Union
from typing import Optional

from sqlalchemy import select
from sqlalchemy import exists
from sqlalchemy import insert
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.base import Base


Model = TypeVar("Model", bound=Base)


class GenericRepository(Generic[Model]):
    def __init__(self, session: AsyncSession, model: type[Model]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, obj_id: Union[int, uuid.uuid4]) -> Optional[Model]:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def exists_by_cond(self, conditions: list) -> bool:
        stmt = exists(self.model).where(and_(*conditions)).select()
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_one_by_cond(self, conditions: list) -> Optional[Model]:
        stmt = select(self.model).where(and_(*conditions))
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def insert_by_data(self, data: dict) -> None:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()
