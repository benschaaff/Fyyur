"""empty message

Revision ID: 4bb5f8a0d6f0
Revises: 2acd625dd940
Create Date: 2019-11-15 19:06:25.497464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bb5f8a0d6f0'
down_revision = '2acd625dd940'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artist', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Artist', 'email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###