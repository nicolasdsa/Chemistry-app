from __future__ import annotations

from sqlalchemy.orm import Session

from core.exceptions import ConflictError, NotFoundError
from models.instrument import Instrument


def create_instrument(
    db: Session,
    name: str,
    description: str | None,
    image_path: str | None,
    instrument_type: str,
    is_container: bool = True,
    allowed_physical_states: str | None = None,
) -> Instrument:
    existing = db.query(Instrument).filter(Instrument.name == name).first()
    if existing:
        raise ConflictError("Instrumento já cadastrado.")

    instrument = Instrument(
        name=name,
        description=description,
        image_path=image_path,
        instrument_type=instrument_type,
        is_container=is_container,
        allowed_physical_states=allowed_physical_states,
    )
    db.add(instrument)
    db.commit()
    db.refresh(instrument)
    return instrument


def get_instrument_by_id(db: Session, instrument_id: int) -> Instrument:
    instrument = db.get(Instrument, instrument_id)
    if not instrument:
        raise NotFoundError("Instrumento não encontrado.")
    return instrument


def list_instruments(db: Session) -> list[Instrument]:
    return db.query(Instrument).order_by(Instrument.name).all()


def update_instrument(
    db: Session,
    instrument_id: int,
    name: str | None = None,
    description: str | None = None,
    image_path: str | None = None,
    instrument_type: str | None = None,
    is_container: bool | None = None,
    allowed_physical_states: str | None = None,
) -> Instrument:
    instrument = get_instrument_by_id(db, instrument_id)

    if name and name != instrument.name:
        existing = db.query(Instrument).filter(Instrument.name == name).first()
        if existing and existing.id != instrument.id:
            raise ConflictError("Instrumento já cadastrado.")
        instrument.name = name

    if description is not None:
        instrument.description = description
    if image_path is not None:
        instrument.image_path = image_path
    if instrument_type is not None:
        instrument.instrument_type = instrument_type
    if is_container is not None:
        instrument.is_container = is_container
    if allowed_physical_states is not None:
        instrument.allowed_physical_states = allowed_physical_states

    db.add(instrument)
    db.commit()
    db.refresh(instrument)
    return instrument


def delete_instrument(db: Session, instrument_id: int) -> None:
    instrument = get_instrument_by_id(db, instrument_id)
    db.delete(instrument)
    db.commit()
