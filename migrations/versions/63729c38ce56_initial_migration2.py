"""Initial Migration2

Revision ID: 63729c38ce56
Revises: db2e66b208b3
Create Date: 2019-03-08 09:40:12.669568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63729c38ce56'
down_revision = 'db2e66b208b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('diseases', 'picture_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('diseases', sa.Column('picture_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
