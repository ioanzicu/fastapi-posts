"""add content column to posts table

Revision ID: 4b93b933afba
Revises: 1fb25a56ef86
Create Date: 2021-12-25 01:27:23.920168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b93b933afba'
down_revision = '1fb25a56ef86'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('content',
                            sa.String(),
                            nullable=False)
                  )
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
