"""empty message

Revision ID: 3b2ad3efd53c
Revises: b5da90843690
Create Date: 2020-06-16 19:31:13.337423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3b2ad3efd53c'
down_revision = 'b5da90843690'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('college_program', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('college_program'),
    sa.UniqueConstraint('id')
    )
    op.create_table('thesisstatus',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('status')
    )
    op.create_table('thesis',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('program', sa.String(length=30), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('call_number', sa.String(length=12), nullable=False),
    sa.Column('date_deploy', sa.DateTime(), nullable=True),
    sa.Column('date_input', sa.DateTime(), nullable=False),
    sa.Column('semester', sa.Integer(), nullable=False),
    sa.Column('thesis_file', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['program'], ['program.college_program'], ),
    sa.ForeignKeyConstraint(['status'], ['thesisstatus.status'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('call_number'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('thesisContributors',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('thesis_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['thesis_id'], ['thesis.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('thesisContributors')
    op.drop_table('thesis')
    op.drop_table('thesisstatus')
    op.drop_table('program')
    # ### end Alembic commands ###
