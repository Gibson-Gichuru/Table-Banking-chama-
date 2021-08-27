"""empty message

Revision ID: e3b7b29b4bdc
Revises: 15ddd697d3f4
Create Date: 2021-08-16 20:14:42.356310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3b7b29b4bdc'
down_revision = '15ddd697d3f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('tele_username', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'tele_username')
    # ### end Alembic commands ###