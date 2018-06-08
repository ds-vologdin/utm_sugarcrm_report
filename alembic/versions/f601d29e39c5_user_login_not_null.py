"""User login not null

Revision ID: f601d29e39c5
Revises: 0b5c759fce42
Create Date: 2018-06-08 15:08:57.816553

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'f601d29e39c5'
down_revision = '0b5c759fce42'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'login', nullable=False)


def downgrade():
    op.alter_column('users', 'login', nullable=True)
