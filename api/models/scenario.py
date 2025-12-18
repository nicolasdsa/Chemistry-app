from __future__ import annotations
from typing import TYPE_CHECKING  
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.artist import Artist
    from models.scenario_step import ScenarioStep
    from models.reaction import Reaction
    from models.scenario_screen import ScenarioScreen

class Scenario(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    artist_id: Mapped[int | None] = mapped_column(
        ForeignKey("artists.id", ondelete="SET NULL"), nullable=True
    )

    steps: Mapped[list[ScenarioStep]] = relationship(
        back_populates="scenario",
        cascade="all, delete-orphan",
        order_by="ScenarioStep.order_index",
        passive_deletes=True,
    )
    reactions: Mapped[list[Reaction]] = relationship(
        back_populates="scenario",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    screens: Mapped[list[ScenarioScreen]] = relationship(
        back_populates="scenario",
        cascade="all, delete-orphan",
        order_by="ScenarioScreen.order_index",
        passive_deletes=True,
    )
    artist: Mapped[Artist | None] = relationship(back_populates="scenarios")
