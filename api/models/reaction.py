from __future__ import annotations

from typing import TYPE_CHECKING  

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from models.scenario import Scenario
    from models.reagent import Reagent
    from models.reaction_reagent import ReactionReagent

class Reaction(Base):
    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    scenario_id: Mapped[int | None] = mapped_column(
        ForeignKey("scenarios.id", ondelete="CASCADE"), nullable=True
    )
    
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    product_reagent_id: Mapped[int] = mapped_column(
        ForeignKey("reagents.id", ondelete="CASCADE"), nullable=False
    )
    
    reaction_key: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    # 3. CORREÇÃO PRINCIPAL: 
    # Remova as aspas. Agora é a classe Scenario (importada no TYPE_CHECKING) | None
    scenario: Mapped[Scenario | None] = relationship(back_populates="reactions")
    
    # Faça o mesmo para os outros relacionamentos se desejar padronizar:
    product_reagent: Mapped[Reagent] = relationship(
        back_populates="product_reactions", foreign_keys=[product_reagent_id]
    )
    
    reagents: Mapped[list[ReactionReagent]] = relationship(
        back_populates="reaction",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )