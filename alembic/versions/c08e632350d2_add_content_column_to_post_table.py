"""Add content column to post table

Revision ID: c08e632350d2
Revises: cdffb0c85fa8
Create Date: 2023-10-10 21:58:04.174464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c08e632350d2'
down_revision: Union[str, None] = 'cdffb0c85fa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
