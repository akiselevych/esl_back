import uuid

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID

from ..db.base import Base
from ..db.mixins import IdColMixin
from ..db.mixins import BaseModelMixin
from .hashing import Hashing


class User(BaseModelMixin, Base):
    id: Mapped[uuid.uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True, doc="Username")
    hashed_password: Mapped[str] = mapped_column(nullable=False, doc="Hashed password")
    is_superuser: Mapped[bool] = mapped_column(default=False, doc="Is superuser")
    steam_connected: Mapped[bool] = mapped_column(default=False, doc="Is steam connected")
    cover_image: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"User: {self.username}"

    def check_password(self, password: str) -> bool:
        return Hashing.verify_password(password, self.hashed_password)


class JWTBlackList(IdColMixin, Base):
    __tablename__ = "jwt_blacklist"

    token: Mapped[str] = mapped_column(nullable=False, unique=True, index=True, doc="JWT token")

    def __repr__(self) -> str:
        return f"Token: {self.token}"
