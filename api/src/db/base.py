import uuid

from typing import Union

from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import declared_attr


@as_declarative()
class Base:
    id: Union[int, uuid.uuid4]

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically"""
        return cls.__name__.lower()
