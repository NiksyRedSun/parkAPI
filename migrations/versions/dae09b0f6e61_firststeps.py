"""FirstSteps

Revision ID: dae09b0f6e61
Revises: 468fb1a2f678
Create Date: 2024-06-22 16:43:35.984541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dae09b0f6e61'
down_revision = '468fb1a2f678'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apartments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resident_id', sa.Integer(), nullable=False),
    sa.Column('num', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['resident_id'], ['residents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resident_id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=50), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=False),
    sa.Column('plate', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['resident_id'], ['residents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parking_slots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resident_id', sa.Integer(), nullable=False),
    sa.Column('num', sa.Integer(), nullable=False),
    sa.Column('letter', sa.String(length=1), nullable=False),
    sa.ForeignKeyConstraint(['resident_id'], ['residents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('residents', schema=None) as batch_op:
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('second_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('surname',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('pas_series',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('pas_number',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('residents', schema=None) as batch_op:
        batch_op.alter_column('pas_number',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('pas_series',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('surname',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('second_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    op.drop_table('parking_slots')
    op.drop_table('cars')
    op.drop_table('apartments')
    # ### end Alembic commands ###