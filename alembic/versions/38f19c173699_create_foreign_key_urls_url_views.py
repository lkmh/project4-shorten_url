"""create foreign key urls => url_views 

Revision ID: 38f19c173699
Revises: 203640f00865
Create Date: 2022-11-02 20:26:51.238591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38f19c173699'
down_revision = '203640f00865'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key('fkey_urlviews_url', 'url_views', 'urls', ['hash_url'], ['hash_url'])


def downgrade() -> None:
    op.drop_constraint('fkey_urlviews_url', 'url_views', type_='foreignkey')
