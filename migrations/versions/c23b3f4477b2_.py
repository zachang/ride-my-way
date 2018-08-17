"""empty message

Revision ID: c23b3f4477b2
Revises: 
Create Date: 2018-08-15 11:40:45.300533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c23b3f4477b2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('first_name', sa.String(length=250), nullable=False),
    sa.Column('last_name', sa.String(length=250), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('phone_no', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('user_image', sa.String(length=200), nullable=True),
    sa.Column('is_social', sa.Boolean(), nullable=True),
    sa.Column('reg_type', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_no'),
    sa.UniqueConstraint('username')
    )
    op.create_table('ride',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('car_name', sa.String(length=100), nullable=True),
    sa.Column('departure_time', sa.String(length=250), nullable=False),
    sa.Column('seat_count', sa.Integer(), nullable=False),
    sa.Column('seat_taken', sa.Integer(), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rate',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('ride_id', sa.String(), nullable=False),
    sa.Column('rate_status', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ride_id'], ['ride.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('userId', sa.String(), nullable=False),
    sa.Column('rideId', sa.String(), nullable=False),
    sa.Column('status', sa.String(length=10), server_default='pending', nullable=True),
    sa.ForeignKeyConstraint(['rideId'], ['ride.id'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    op.drop_table('rate')
    op.drop_table('ride')
    op.drop_table('user')
    # ### end Alembic commands ###