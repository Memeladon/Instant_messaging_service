"""create user table

Revision ID: 193f4a40074f
Revises: 71fe1b069cfb
Create Date: 2024-10-23 05:13:42.620162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table


# revision identifiers, used by Alembic.
revision: str = '193f4a40074f'
down_revision: Union[str, None] = '71fe1b069cfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


USERS = table("users", sa.Column('id', sa.Uuid(), nullable=False),
              sa.Column('username', sa.String(), nullable=False),
              sa.Column('password', sa.String(), nullable=False),
              sa.Column('role', sa.String(), nullable=False),
              sa.Column('is_active', sa.Boolean(), nullable=False))

USER_ID = "ae7ee1ee-fade-4c11-afc0-53a702780211"


def upgrade() -> None:
    op.bulk_insert(USERS, [
        {
            "id": USER_ID,
            "username": "admin",
            "password": "$scrypt$ln=16,r=8,p=1$wXjP+X8v5Tzn3BsjRGhNiQ$OMVKqmnCnrR324quXK8U4L0FIUQBjhT5pv+6Ox9Jl1M",
            "role": "ADMIN",
            "is_active": "true"
        }
    ])


def downgrade() -> None:
    op.execute(USERS.delete().where(USERS.c.id == USER_ID))
