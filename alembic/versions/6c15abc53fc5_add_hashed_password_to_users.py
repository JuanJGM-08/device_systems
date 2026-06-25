"""add hashed_password to users

Revision ID: 6c15abc53fc5
Revises: f4d6e03c7be9
Create Date: 2026-06-24 19:18:14.375156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '6c15abc53fc5'
down_revision: Union[str, Sequence[str], None] = 'f4d6e03c7be9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite no soporta ALTER COLUMN, agregamos como NULL
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'hashed_password')