"""add last few columns to posts table

Revision ID: 2c86d5612246
Revises: 2e650549eb01
Create Date: 2021-12-25 01:45:21.427403

"""
from datetime import time
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c86d5612246'
down_revision = '2e650549eb01'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
