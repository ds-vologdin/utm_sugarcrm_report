"""User password field increase

Revision ID: 148c04f19ce3
Revises: 787ce2441df0
Create Date: 2018-06-08 14:44:46.295285

"""
from alembic import op
from sqlalchemy import String


# revision identifiers, used by Alembic.
revision = '148c04f19ce3'
down_revision = '787ce2441df0'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'users', 'password', type_=String(100)
    )


def downgrade():
    op.alter_column(
        'users', 'password', type_=String(20)
    )
