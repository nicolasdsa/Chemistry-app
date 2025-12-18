from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.artist_timeline_entry import ArtistTimelineEntry
    from models.scenario import Scenario


class Artist(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str] = mapped_column(Text, nullable=False)

    timeline_entries: Mapped[list[ArtistTimelineEntry]] = relationship(
        back_populates="artist",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="ArtistTimelineEntry.year",
    )
    scenarios: Mapped[list[Scenario]] = relationship(
        back_populates="artist",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
