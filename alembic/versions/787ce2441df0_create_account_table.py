"""create account table

Revision ID: 787ce2441df0
Revises:
Create Date: 2018-06-08 11:19:32.651932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '787ce2441df0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('login', sa.String(20), unique=True),
        sa.Column('password', sa.String(20), unique=True),
        sa.Column('name', sa.String(200)),
        sa.Column('email', sa.String(200)),
    )


def downgrade():
    op.drop_table('users')
