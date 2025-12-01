from __future__ import annotations
from typing import TYPE_CHECKING  

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.scenario_step import ScenarioStep
    from models.reaction_reagent import ReactionReagent
    from models.reaction import Reaction

class Reagent(Base):
    __tablename__ = "reagents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    formula: Mapped[str] = mapped_column(String(100), nullable=False)
    physical_state: Mapped[str] = mapped_column(String(50), nullable=False)
    tags: Mapped[dict | list | str | None] = mapped_column(JSON, nullable=True)

    scenario_steps: Mapped[list[ScenarioStep]] = relationship(
        back_populates="reagent",
        passive_deletes=True,
    )
    reaction_links: Mapped[list[ReactionReagent]] = relationship(
        back_populates="reagent",
        passive_deletes=True,
    )
    product_reactions: Mapped[list[Reaction]] = relationship(
        back_populates="product_reagent",
        passive_deletes=True,
    )
