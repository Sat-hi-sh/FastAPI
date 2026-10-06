"""ensure posts timestamp column

Revision ID: e13b7d2ac868
Revises: 7da49d733104
Create Date: 2026-10-06 16:13:35.639753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e13b7d2ac868'
down_revision: Union[str, Sequence[str], None] = '7da49d733104'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = [
        column["name"]
        for column in inspector.get_columns("posts")
    ]

    if "timestamp" not in columns:
        op.add_column(
            "posts",
            sa.Column(
                "timestamp",
                sa.TIMESTAMP(timezone=True),
                nullable=False,
                server_default=sa.text("now()"),
            ),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = [
        column["name"]
        for column in inspector.get_columns("posts")
    ]

    if "timestamp" in columns:
        op.drop_column("posts", "timestamp")
