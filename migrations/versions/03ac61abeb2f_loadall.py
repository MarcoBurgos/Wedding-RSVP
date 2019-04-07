"""loadall

Revision ID: 03ac61abeb2f
Revises: 225f73b83838
Create Date: 2019-04-06 21:31:52.018071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03ac61abeb2f'
down_revision = '225f73b83838'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('phone_number', sa.String(length=10), nullable=False),
    sa.Column('guests', sa.Integer(), nullable=False),
    sa.Column('guests_names', sa.String(length=128), nullable=False),
    sa.Column('guests_confirmed', sa.String(length=128), nullable=True),
    sa.Column('total_guests', sa.Integer(), nullable=True),
    sa.Column('is_RSVP', sa.Boolean(), nullable=True),
    sa.Column('date_RSVP', sa.DateTime(), nullable=True),
    sa.Column('update_date_RSVP', sa.DateTime(), nullable=True),
    sa.Column('update_times', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###