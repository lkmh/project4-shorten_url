"""create url_views table

Revision ID: 53e81b3fe1d0
Revises: f98342359d7f
Create Date: 2022-10-23 13:36:15.634220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53e81b3fe1d0'
down_revision = 'f98342359d7f'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'url_views',
    sa.Column('id', sa.Integer, sa.Identity(always=True), primary_key=True),
    sa.Column('hash_url', sa.String(255), nullable=False),
    sa.Column('view_date', sa.Integer, nullable=False),
    sa.Column('user_agent', sa.String(255)),
    sa.Column('ip_address', sa.String(255)),
  )


def downgrade():
  op.drop_table('url_views')