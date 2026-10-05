"""Adding a content column to posts table

Revision ID: 134ccdc43980
Revises: 09a198b4210a
Create Date: 2026-10-05 18:23:41.600921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '134ccdc43980'
down_revision: Union[str, Sequence[str], None] = '09a198b4210a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
