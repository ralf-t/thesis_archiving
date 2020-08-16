"""empty message

Revision ID: 260745950bbe
Revises: fc540a41d0f9
Create Date: 2020-06-14 22:12:08.709732

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '260745950bbe'
down_revision = 'fc540a41d0f9'
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
    op.create_table('thesis',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('program', sa.String(length=30), nullable=False),
    sa.Column('date_deploy', sa.DateTime(), nullable=True),
    sa.Column('date_input', sa.DateTime(), nullable=False),
    sa.Column('semester', sa.Integer(), nullable=False),
    sa.Column('adviser', sa.String(length=50), nullable=False),
    sa.Column('thesis_file', sa.String(length=20), nullable=True),
    sa.Column('call_number', sa.String(length=12), nullable=False),
    sa.ForeignKeyConstraint(['program'], ['program.college_program'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('call_number'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('student',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('student_number', sa.BIGINT(), nullable=False),
    sa.Column('thesis', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['thesis'], ['thesis.title'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('student_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    op.drop_table('thesis')
    op.drop_table('program')
    # ### end Alembic commands ###
