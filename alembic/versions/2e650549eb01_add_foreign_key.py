"""add foreign-key

Revision ID: 2e650549eb01
Revises: 5187377f38d4
Create Date: 2021-12-25 01:39:24.455502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e650549eb01'
down_revision = '5187377f38d4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('owner_id',
                            sa.Integer(),
                            nullable=False)
                  )
    op.create_foreign_key('posts_users_fk',
                          source_table='posts',
                          referent_table='users',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
