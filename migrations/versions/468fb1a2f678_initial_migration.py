"""Initial migration.

Revision ID: 468fb1a2f678
Revises: 
Create Date: 2024-06-22 15:48:37.978558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '468fb1a2f678'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('residents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('second_name', sa.String(length=50), nullable=True),
    sa.Column('surname', sa.String(length=50), nullable=True),
    sa.Column('pas_series', sa.Integer(), nullable=True),
    sa.Column('pas_number', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('residents')
    # ### end Alembic commands ###
