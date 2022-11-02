"""create foreign key users => urls 

Revision ID: 203640f00865
Revises: 7fa2dc573629
Create Date: 2022-11-02 20:20:14.673994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '203640f00865'
down_revision = '7fa2dc573629'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key('fkey_urls_users', 'urls', 'users', ['userid'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fkey_urls_users', 'urls', type_='foreignkey')
