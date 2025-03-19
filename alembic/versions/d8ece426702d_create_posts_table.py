"""create posts table

Revision ID: d8ece426702d
Revises: 
Create Date: 2025-03-19 22:38:28.501849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8ece426702d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id', sa.Integer,nullable=False,primary_key=True),
                    sa.Column('title',sa.String,nullable=False,primary_key=True))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
