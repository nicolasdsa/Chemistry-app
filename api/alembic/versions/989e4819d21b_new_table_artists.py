"""new table artists

Revision ID: 989e4819d21b
Revises: 4da0de5d7d7a
Create Date: 2025-12-18 01:34:54.331041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '989e4819d21b'
down_revision: Union[str, Sequence[str], None] = '4da0de5d7d7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('artists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('image_path', sa.String(length=255), nullable=True),
        sa.Column('bio', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_artists_id'), 'artists', ['id'], unique=False)

    op.create_table('artist_timeline_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('artist_id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_artist_timeline_entries_id'), 'artist_timeline_entries', ['id'], unique=False)

    op.create_table('scenario_screens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scenario_id', sa.Integer(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('screen_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('body_text', sa.Text(), nullable=True),
        sa.Column('image_path', sa.String(length=255), nullable=True),
        sa.Column('gif_path', sa.String(length=255), nullable=True),
        sa.Column('button_label', sa.String(length=100), nullable=True),
        sa.Column('animation_key', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scenario_screens_id'), 'scenario_screens', ['id'], unique=False)

    op.create_table('scenario_screen_slider_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('screen_id', sa.Integer(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False),
        sa.Column('image_path', sa.String(length=255), nullable=False),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['screen_id'], ['scenario_screens.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scenario_screen_slider_images_id'), 'scenario_screen_slider_images', ['id'], unique=False)

    with op.batch_alter_table('scenarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('artist_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_scenarios_artists', 'artists', ['artist_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('scenarios', schema=None) as batch_op:
        batch_op.drop_constraint('fk_scenarios_artists', type_='foreignkey')
        batch_op.drop_column('artist_id')

    op.drop_index(op.f('ix_scenario_screen_slider_images_id'), table_name='scenario_screen_slider_images')
    op.drop_table('scenario_screen_slider_images')
    op.drop_index(op.f('ix_scenario_screens_id'), table_name='scenario_screens')
    op.drop_table('scenario_screens')
    op.drop_index(op.f('ix_artist_timeline_entries_id'), table_name='artist_timeline_entries')
    op.drop_table('artist_timeline_entries')
    op.drop_index(op.f('ix_artists_id'), table_name='artists')
    op.drop_table('artists')
