"""edit hash to 8 redo redo

Revision ID: 7fa2dc573629
Revises: e295dd005d59
Create Date: 2022-11-02 20:15:55.896851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fa2dc573629'
down_revision = 'e295dd005d59'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('urls', 'hash_url', type_=sa.String(8))
    op.alter_column('url_views', 'hash_url', type_=sa.String(8))


def downgrade() -> None:
    op.alter_column('urls', 'hash_url', type_=sa.String(255))
    op.alter_column('url_views', 'hash_url', type_=sa.String(255))
