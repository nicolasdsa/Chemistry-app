from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.dependencies import get_db  
from controllers.instrument import (
    list_instruments, 
    create_instrument, 
    get_instrument, 
    update_instrument, 
    delete_instrument
)
from schemas.instrument import InstrumentCreate, InstrumentUpdate

router = APIRouter(
    prefix="/instruments",
    tags=["Instruments"],
    default_response_class=HTMLResponse,
)

@router.post("/", response_class=HTMLResponse)
def create_instrument_route(
    payload: InstrumentCreate,
    db: Session = Depends(get_db)  
):
    return create_instrument(payload, db)  

@router.get("/", response_class=HTMLResponse)
def list_instruments_route(
    db: Session = Depends(get_db)
):
    return list_instruments(db)

@router.get("/{instrument_id}", response_class=HTMLResponse)
def get_instrument_route(
    instrument_id: int,
    db: Session = Depends(get_db)
):
    return get_instrument(instrument_id, db)

@router.put("/{instrument_id}", response_class=HTMLResponse)
def update_instrument_route(
    instrument_id: int,
    payload: InstrumentUpdate,
    db: Session = Depends(get_db)
):
    return update_instrument(instrument_id, payload, db)

@router.delete("/{instrument_id}", response_class=HTMLResponse)
def delete_instrument_route(
    instrument_id: int,
    db: Session = Depends(get_db)
):
    return delete_instrument(instrument_id, db)