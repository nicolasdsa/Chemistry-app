from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.scenario_screen import ScenarioScreen


class ScenarioScreenSliderImage(Base):
    __tablename__ = "scenario_screen_slider_images"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    screen_id: Mapped[int] = mapped_column(
        ForeignKey("scenario_screens.id", ondelete="CASCADE"), nullable=False
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    image_path: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str | None] = mapped_column(Text, nullable=True)

    screen: Mapped[ScenarioScreen] = relationship(back_populates="slider_images")
