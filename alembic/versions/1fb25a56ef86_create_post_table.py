"""create post table

Revision ID: 1fb25a56ef86
Revises: 
Create Date: 2021-12-25 01:19:33.577847

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = '1fb25a56ef86'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id',
                              sa.Integer(),
                              nullable=False,
                              primary_key=True),
                    sa.Column('title',
                              sa.String,
                              nullable=False)
                    )
    pass


def downgrade():
    op.drop_table('posts')
    pass
