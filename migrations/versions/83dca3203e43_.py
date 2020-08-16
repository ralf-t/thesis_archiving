"""empty message

Revision ID: 83dca3203e43
Revises: b123f01ff400
Create Date: 2020-06-16 16:52:04.474585

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '83dca3203e43'
down_revision = 'b123f01ff400'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userRole',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('role_id', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.name'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    )
    op.drop_table('user_role')
    op.create_unique_constraint(None, 'role', ['id'])
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'role', type_='unique')
    op.create_table('user_role',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.name'], name='user_role_role_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='user_role_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='user_role_pkey')
    )
    op.drop_table('userRole')
    # ### end Alembic commands ###
