from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.scenario_step import ScenarioStep


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    instrument_type: Mapped[str] = mapped_column(String(100), nullable=False)
    is_container: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    allowed_physical_states: Mapped[str | None] = mapped_column(String(255), nullable=True)
    marker_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        unique=True,
        index=True,
        doc="ArUco marker identifier associated with the instrument.",
    )
    marker_image_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Path to the generated ArUco marker image.",
    )

    scenario_steps: Mapped[list[ScenarioStep]] = relationship(
        back_populates="instrument",
        passive_deletes=True,
    )
