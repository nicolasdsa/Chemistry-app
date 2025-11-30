from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.core.database import Base


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

    scenario: Mapped["Scenario"] | None = relationship(back_populates="reactions")
    product_reagent: Mapped["Reagent"] = relationship(
        back_populates="product_reactions", foreign_keys=[product_reagent_id]
    )
    reagents: Mapped[list["ReactionReagent"]] = relationship(
        back_populates="reaction",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
