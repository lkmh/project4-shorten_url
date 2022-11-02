"""edit hash to 8

Revision ID: b12b3d67c26c
Revises: 53e81b3fe1d0
Create Date: 2022-11-02 20:02:37.872415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b12b3d67c26c'
down_revision = '53e81b3fe1d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('urls', 'hash_url', existing_type=sa.String(8))
    op.alter_column('url_views', 'hash_url', existing_type=sa.String(8))


def downgrade() -> None:
    op.alter_column('urls', 'hash_url', existing_type=sa.String(255))
    op.alter_column('url_views', 'hash_url', existing_type=sa.String(255))
