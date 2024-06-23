"""plate_unique_only

Revision ID: ba4ce2dc82ea
Revises: ce54ade67bfd
Create Date: 2024-06-23 23:00:42.142684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba4ce2dc82ea'
down_revision = 'ce54ade67bfd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.drop_constraint('cars_resident_id_plate_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.create_unique_constraint('cars_resident_id_plate_key', ['resident_id', 'plate'])

    # ### end Alembic commands ###
