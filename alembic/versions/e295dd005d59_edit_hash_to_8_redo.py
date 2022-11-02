"""edit hash to 8 redo

Revision ID: e295dd005d59
Revises: b12b3d67c26c
Create Date: 2022-11-02 20:14:28.931437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e295dd005d59'
down_revision = 'b12b3d67c26c'
branch_labels = None
depends_on = None



def upgrade() -> None:
    op.alter_column('urls', 'hash_url', type=sa.String(8))
    op.alter_column('url_views', 'hash_url', type=sa.String(8))


def downgrade() -> None:
    op.alter_column('urls', 'hash_url', type=sa.String(255))
    op.alter_column('url_views', 'hash_url', type=sa.String(255))
