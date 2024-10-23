import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class IdColMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __str__(self) -> str:
        return self.__repr__()


class TimeStampMixin:
    """Adds `created_at` and `updated_at` columns to the model"""

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )


class BaseModelMixin(IdColMixin, TimeStampMixin):
    pass
