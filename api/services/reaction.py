from __future__ import annotations

from typing import Sequence

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from models.reaction import Reaction
from models.reaction_reagent import ReactionReagent


def create_reaction(
    db: Session,
    description: str,
    product_reagent_id: int,
    message: str,
    scenario_id: int | None = None,
    reagents: Sequence[dict] | None = None,
) -> Reaction:
    reagent_ids = [item["reagent_id"] for item in reagents] if reagents else []
    reaction = Reaction(
        description=description,
        product_reagent_id=product_reagent_id,
        message=message,
        scenario_id=scenario_id,
        reaction_key=_generate_reaction_key(reagent_ids),
    )
    db.add(reaction)
    db.flush()

    if reagents:
        _replace_reagents(db, reaction, reagents)

    db.commit()
    db.refresh(reaction)
    return reaction


def get_reaction_by_id(db: Session, reaction_id: int) -> Reaction:
    reaction = db.get(Reaction, reaction_id)
    if not reaction:
        raise NotFoundError("Reação não encontrada.")
    return reaction


def list_reactions(db: Session) -> list[Reaction]:
    return db.query(Reaction).order_by(Reaction.id.desc()).all()


def update_reaction(
    db: Session,
    reaction_id: int,
    description: str | None = None,
    product_reagent_id: int | None = None,
    message: str | None = None,
    scenario_id: int | None = None,
    reagents: Sequence[dict] | None = None,
) -> Reaction:
    reaction = get_reaction_by_id(db, reaction_id)

    if description is not None:
        reaction.description = description
    if product_reagent_id is not None:
        reaction.product_reagent_id = product_reagent_id
    if message is not None:
        reaction.message = message
    if scenario_id is not None:
        reaction.scenario_id = scenario_id

    if reagents is not None:
        _replace_reagents(db, reaction, reagents)
        reagent_ids = [item["reagent_id"] for item in reagents]
        reaction.reaction_key = _generate_reaction_key(reagent_ids)

    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction


def delete_reaction(db: Session, reaction_id: int) -> None:
    reaction = get_reaction_by_id(db, reaction_id)
    db.delete(reaction)
    db.commit()


def get_required_reagents_for_reaction(reaction: Reaction) -> set[int]:
    return {link.reagent_id for link in reaction.reagents if link.role == "reagent"}


def _replace_reagents(db: Session, reaction: Reaction, reagents: Sequence[dict]) -> None:
    reaction.reagents.clear()
    for reagent_data in reagents:
        reaction.reagents.append(
            ReactionReagent(
                reaction_id=reaction.id,
                reagent_id=reagent_data["reagent_id"],
                coefficient=reagent_data.get("coefficient", 1),
                role=reagent_data.get("role", "reagent"),
            )
        )


def _generate_reaction_key(reagent_ids: Sequence[int]) -> str:
    if not reagent_ids:
        return ""
    sorted_ids = sorted(reagent_ids)
    return "+".join(str(rid) for rid in sorted_ids)
