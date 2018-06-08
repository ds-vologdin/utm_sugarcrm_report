"""User password not unique

Revision ID: 0b5c759fce42
Revises: 148c04f19ce3
Create Date: 2018-06-08 14:55:10.261764

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '0b5c759fce42'
down_revision = '148c04f19ce3'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'password', nullable=False)
    op.drop_constraint('users_password_key', 'users')


def downgrade():
    op.alter_column('users', 'password', nullable=True)
    op.create_unique_constraint('users_password_key', 'users', 'password')
