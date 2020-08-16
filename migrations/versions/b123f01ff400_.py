"""empty message

Revision ID: b123f01ff400
Revises: 260745950bbe
Create Date: 2020-06-16 15:59:30.810823

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b123f01ff400'
down_revision = '260745950bbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('username', sa.String(length=11), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('surname', sa.String(length=40), nullable=False),
    sa.Column('firstname', sa.String(length=40), nullable=False),
    sa.Column('middle_initial', sa.String(length=5), nullable=True),
    sa.Column('suffix', sa.String(length=5), nullable=True),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_role',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('role_id', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.name'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.drop_table('student')
    op.drop_table('thesis')
    op.drop_table('program')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('college_program', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='program_pkey'),
    sa.UniqueConstraint('college_program', name='program_college_program_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('student',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('student_number', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('thesis', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['thesis'], ['thesis.title'], name='student_thesis_fkey'),
    sa.PrimaryKeyConstraint('id', name='student_pkey'),
    sa.UniqueConstraint('name', name='student_name_key'),
    sa.UniqueConstraint('student_number', name='student_student_number_key')
    )
    op.create_table('thesis',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('program', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('date_deploy', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('date_input', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('semester', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('adviser', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('thesis_file', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('call_number', sa.VARCHAR(length=12), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['program'], ['program.college_program'], name='thesis_program_fkey'),
    sa.PrimaryKeyConstraint('id', name='thesis_pkey'),
    sa.UniqueConstraint('call_number', name='thesis_call_number_key'),
    sa.UniqueConstraint('title', name='thesis_title_key')
    )
    op.drop_table('user_role')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
