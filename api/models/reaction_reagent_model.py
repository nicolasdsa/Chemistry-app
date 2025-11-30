from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.core.database import Base


class ReactionReagent(Base):
    __tablename__ = "reaction_reagents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reaction_id: Mapped[int] = mapped_column(
        ForeignKey("reactions.id", ondelete="CASCADE"), nullable=False
    )
    reagent_id: Mapped[int] = mapped_column(
        ForeignKey("reagents.id", ondelete="CASCADE"), nullable=False
    )
    coefficient: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    role: Mapped[str] = mapped_column(String(50), nullable=False)

    reaction: Mapped["Reaction"] = relationship(back_populates="reagents")
    reagent: Mapped["Reagent"] = relationship(back_populates="reaction_links")
