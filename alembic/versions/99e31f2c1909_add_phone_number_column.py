"""add phone number column

Revision ID: 99e31f2c1909
Revises: 38f74f3bbea2
Create Date: 2021-12-25 17:44:41.326572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99e31f2c1909'
down_revision = '38f74f3bbea2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users',
                  sa.Column('phone_number', sa.String(),
                            nullable=True, default='null')
                  )
    pass


def downgrade():
    op.drop_column('users', 'phone_number')
    pass
