from __future__ import annotations

import json

from fastapi import Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.dependencies import get_db
from schemas.instrument import (
    InstrumentCreate,
    InstrumentRead,
    InstrumentUpdate,
)
from services import instrument as instrument_service


def create_instrument(
    payload: InstrumentCreate, db: Session = Depends(get_db)
) -> HTMLResponse:
    instrument = instrument_service.create_instrument(
        db=db,
        name=payload.name,
        description=payload.description,
        image_path=payload.image_path,
    )
    data = InstrumentRead.model_validate(instrument).model_dump()
    return HTMLResponse(content=json.dumps(data), status_code=201)


def list_instruments(db: Session = Depends(get_db)) -> HTMLResponse:
    instruments = instrument_service.list_instruments(db)
    data = [InstrumentRead.model_validate(item).model_dump() for item in instruments]
    return HTMLResponse(content=json.dumps(data), status_code=200)


def get_instrument(instrument_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    instrument = instrument_service.get_instrument_by_id(db, instrument_id)
    data = InstrumentRead.model_validate(instrument).model_dump()
    return HTMLResponse(content=json.dumps(data), status_code=200)


def update_instrument(
    instrument_id: int, payload: InstrumentUpdate, db: Session = Depends(get_db)
) -> HTMLResponse:
    instrument = instrument_service.update_instrument(
        db=db,
        instrument_id=instrument_id,
        name=payload.name,
        description=payload.description,
        image_path=payload.image_path,
    )
    data = InstrumentRead.model_validate(instrument).model_dump()
    return HTMLResponse(content=json.dumps(data), status_code=200)


def delete_instrument(instrument_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    instrument_service.delete_instrument(db, instrument_id)
    return HTMLResponse(content="", status_code=204)
