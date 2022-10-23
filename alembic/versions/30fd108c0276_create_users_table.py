"""create users table

Revision ID: 30fd108c0276
Revises: 
Create Date: 2022-10-23 13:23:10.343162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30fd108c0276'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'users',
    sa.Column('id', sa.Integer, sa.Identity(always=True), primary_key=True),
    sa.Column('email', sa.String(255), nullable=False, unique=True),
    sa.Column('hash_password', sa.String(255), nullable=False),
    sa.Column('created_date', sa.Integer, nullable=False),
  )


def downgrade():
  op.drop_table('users')