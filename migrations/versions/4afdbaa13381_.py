"""empty message

Revision ID: 4afdbaa13381
Revises: 
Create Date: 2019-11-28 14:49:20.575701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4afdbaa13381'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instructors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('studios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bizname', sa.String(), nullable=False),
    sa.Column('opening_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('studios')
    op.drop_table('instructors')
    # ### end Alembic commands ###
