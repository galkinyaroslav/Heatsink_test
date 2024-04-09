"""Add role nullable=True

Revision ID: 99d16655bcd7
Revises: 38fde7e02d52
Create Date: 2023-08-07 14:17:11.693549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99d16655bcd7'
down_revision = '38fde7e02d52'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('roles_table', 'permissions', existing_type=sa.JSON(), nullable=True)


def downgrade() -> None:
    op.alter_column('roles_table', 'permissions', existing_type=sa.JSON(), nullable=False)

