"""create user table

Revision ID: b8b54459d85c
Revises: 96d51a51cef8
Create Date: 2025-08-27 14:59:48.357562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8b54459d85c'
down_revision: Union[str, Sequence[str], None] = '96d51a51cef8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True,index=True),
                    sa.Column('email',sa.String(),nullable=False,unique=True),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
