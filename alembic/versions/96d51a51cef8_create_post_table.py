"""create post table

Revision ID: 96d51a51cef8
Revises: 
Create Date: 2025-08-25 13:16:28.232996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96d51a51cef8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True,index=True),
                    sa.Column('title',sa.String(),nullable=False,index=True),
                    sa.Column('content',sa.String(),nullable=False),
                    sa.Column('published',sa.Boolean(),server_default="True",nullable=False),
                    sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
    
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
