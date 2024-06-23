"""res_uniq_constr

Revision ID: 24780c8944fc
Revises: 9508d1a4bb59
Create Date: 2024-06-23 01:00:14.110777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24780c8944fc'
down_revision = '9508d1a4bb59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('residents', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['pas_series', 'pas_number'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('residents', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###