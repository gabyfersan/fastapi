"""Generate tables to original

Revision ID: da4b21721b8f
Revises: c08e632350d2
Create Date: 2023-10-10 22:26:05.994258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da4b21721b8f'
down_revision: Union[str, None] = 'c08e632350d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
