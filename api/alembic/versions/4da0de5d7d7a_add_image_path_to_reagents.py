"""add image_path to reagents

Revision ID: 4da0de5d7d7a
Revises: daee1a163be5
Create Date: 2024-10-18 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4da0de5d7d7a"
down_revision = "daee1a163be5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("reagents", sa.Column("image_path", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("reagents", "image_path")
