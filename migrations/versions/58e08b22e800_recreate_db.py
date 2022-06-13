"""recreate db

Revision ID: 58e08b22e800
Revises: 
Create Date: 2022-06-13 02:52:43.504406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58e08b22e800'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shopper',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shopper_id', sa.Integer(), nullable=False),
    sa.Column('item', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Numeric(precision=8, scale=2), nullable=False),
    sa.Column('quantity', sa.String(length=17), nullable=False),
    sa.Column('total', sa.Numeric(precision=8, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['shopper_id'], ['shopper.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart')
    op.drop_table('shopper')
    # ### end Alembic commands ###