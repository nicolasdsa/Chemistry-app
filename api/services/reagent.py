from __future__ import annotations

from sqlalchemy.orm import Session

from api.core.exceptions import ConflictError, NotFoundError
from api.models.reagent import Reagent


def create_reagent(
    db: Session,
    name: str,
    formula: str,
    physical_state: str,
    tags: dict | list | str | None = None,
) -> Reagent:
    existing = db.query(Reagent).filter(Reagent.name == name).first()
    if existing:
        raise ConflictError("Reagente já cadastrado.")

    reagent = Reagent(
        name=name,
        formula=formula,
        physical_state=physical_state,
        tags=tags,
    )
    db.add(reagent)
    db.commit()
    db.refresh(reagent)
    return reagent


def get_reagent_by_id(db: Session, reagent_id: int) -> Reagent:
    reagent = db.get(Reagent, reagent_id)
    if not reagent:
        raise NotFoundError("Reagente não encontrado.")
    return reagent


def list_reagents(db: Session) -> list[Reagent]:
    return db.query(Reagent).order_by(Reagent.name).all()


def update_reagent(
    db: Session,
    reagent_id: int,
    name: str | None = None,
    formula: str | None = None,
    physical_state: str | None = None,
    tags: dict | list | str | None = None,
) -> Reagent:
    reagent = get_reagent_by_id(db, reagent_id)

    if name and name != reagent.name:
        existing = db.query(Reagent).filter(Reagent.name == name).first()
        if existing and existing.id != reagent.id:
            raise ConflictError("Reagente já cadastrado.")
        reagent.name = name

    if formula is not None:
        reagent.formula = formula
    if physical_state is not None:
        reagent.physical_state = physical_state
    if tags is not None:
        reagent.tags = tags

    db.add(reagent)
    db.commit()
    db.refresh(reagent)
    return reagent


def delete_reagent(db: Session, reagent_id: int) -> None:
    reagent = get_reagent_by_id(db, reagent_id)
    db.delete(reagent)
    db.commit()
