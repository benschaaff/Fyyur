"""empty message

Revision ID: f278fd4e0a09
Revises: 9ec84c061ef0
Create Date: 2019-11-13 01:23:55.713486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f278fd4e0a09'
down_revision = '9ec84c061ef0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###
