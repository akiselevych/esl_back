"""Removed email

Revision ID: a60edafdb814
Revises: f69524f80da7
Create Date: 2024-01-28 18:47:04.862545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a60edafdb814"
down_revision: Union[str, None] = "f69524f80da7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_user_email", table_name="user")
    op.drop_column("user", "email")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_index("ix_user_email", "user", ["email"], unique=True)
    # ### end Alembic commands ###
