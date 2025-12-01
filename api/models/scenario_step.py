from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.scenario import Scenario
    from models.instrument import Instrument
    from models.reagent import Reagent

class ScenarioStep(Base):
    __tablename__ = "scenario_steps"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    scenario_id: Mapped[int] = mapped_column(
        ForeignKey("scenarios.id", ondelete="CASCADE"), nullable=False
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    instrument_id: Mapped[int | None] = mapped_column(
        ForeignKey("instruments.id", ondelete="SET NULL"), nullable=True
    )
    reagent_id: Mapped[int | None] = mapped_column(
        ForeignKey("reagents.id", ondelete="SET NULL"), nullable=True
    )
    
    target_container: Mapped[str] = mapped_column(String(100), nullable=False)
    text_instruction: Mapped[str] = mapped_column(Text, nullable=False)
    sound_effect_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    scenario: Mapped[Scenario] = relationship(back_populates="steps")
    
    instrument: Mapped[Instrument | None] = relationship(
        back_populates="scenario_steps"
    )
    
    reagent: Mapped[Reagent | None] = relationship(back_populates="scenario_steps")