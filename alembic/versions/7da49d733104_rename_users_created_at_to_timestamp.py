"""rename users created_at to timestamp

Revision ID: 7da49d733104
Revises: 9ed4e3092c09
Create Date: 2026-10-06 14:56:19.985648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7da49d733104'
down_revision: Union[str, Sequence[str], None] = '9ed4e3092c09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "created_at",
        new_column_name="timestamp"
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "timestamp",
        new_column_name="created_at"
    )