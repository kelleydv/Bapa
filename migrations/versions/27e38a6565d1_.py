"""empty message

Revision ID: 27e38a6565d1
Revises: 189ebf4caf69
Create Date: 2016-10-31 11:34:13.418902

"""

# revision identifiers, used by Alembic.
revision = '27e38a6565d1'
down_revision = '189ebf4caf69'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('picture', sa.PickleType(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('profiles', 'picture')
    ### end Alembic commands ###
