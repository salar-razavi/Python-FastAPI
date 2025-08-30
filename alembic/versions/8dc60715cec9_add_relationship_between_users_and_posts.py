"""add relationship between users and posts

Revision ID: 8dc60715cec9
Revises: b8b54459d85c
Create Date: 2025-08-27 15:07:35.048639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8dc60715cec9'
down_revision: Union[str, Sequence[str], None] = 'b8b54459d85c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id',sa.Integer(),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','owner_id')
    pass
