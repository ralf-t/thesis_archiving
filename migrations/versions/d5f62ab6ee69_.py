"""empty message

Revision ID: d5f62ab6ee69
Revises: 3609f653e4d8
Create Date: 2020-12-02 19:47:53.937635

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd5f62ab6ee69'
down_revision = '3609f653e4d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('log', 'user_id',
               existing_type=mysql.BIGINT(display_width=20, unsigned=True),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('log', 'user_id',
               existing_type=mysql.BIGINT(display_width=20, unsigned=True),
               nullable=False)
    # ### end Alembic commands ###
