"""create urls table

Revision ID: f98342359d7f
Revises: 30fd108c0276
Create Date: 2022-10-23 13:30:13.061757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f98342359d7f'
down_revision = '30fd108c0276'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'urls',
    sa.Column('id', sa.Integer, sa.Identity(always=True), primary_key=True),
    sa.Column('original_url', sa.String(255), nullable=False),
    sa.Column('hash_url', sa.String(255), nullable=False, unique=True),
    sa.Column('created_date', sa.Integer, nullable=False),
    sa.Column('userid', sa.Integer),
  )


def downgrade():
  op.drop_table('urls')