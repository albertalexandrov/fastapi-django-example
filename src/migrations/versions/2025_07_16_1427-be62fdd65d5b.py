"""empty message

Revision ID: be62fdd65d5b
Revises: fb075959aac1
Create Date: 2025-07-16 14:27:43.421996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'be62fdd65d5b'
down_revision: Union[str, None] = 'fb075959aac1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('service_users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=16), nullable=False),
    sa.Column('password', sa.String(length=16), nullable=False),
    sa.Column('role', sa.String(length=32), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )


def downgrade() -> None:
    op.drop_table('service_users')
