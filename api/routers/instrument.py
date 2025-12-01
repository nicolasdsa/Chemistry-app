from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from controllers.instrument import list_instruments, create_instrument, get_instrument, update_instrument, delete_instrument
from schemas.instrument import InstrumentCreate, InstrumentUpdate
router = APIRouter(
    prefix="/instruments",
    tags=["Instruments"],
    default_response_class=HTMLResponse,
)

@router.post(
    "/",
    response_model=HTMLResponse,
)
def create_instrument_route(
    payload: InstrumentCreate,
) -> HTMLResponse:
    return create_instrument(payload)

@router.get("/", response_model=HTMLResponse)
def list_instruments_route() -> HTMLResponse:
    return list_instruments()


@router.get(
    "/{instrument_id}",
    response_model=HTMLResponse,
)
def get_instrument_route(instrument_id: int) -> HTMLResponse:
    return get_instrument(instrument_id)

@router.put(
    "/{instrument_id}",
    response_model=HTMLResponse,
)
def update_instrument_route(
    instrument_id: int,
    payload: InstrumentUpdate,
) -> HTMLResponse:
    return update_instrument(instrument_id, payload)

@router.delete(
    "/{instrument_id}",
    response_model=HTMLResponse,
)
def delete_instrument_route(instrument_id: int) -> HTMLResponse:
    return delete_instrument(instrument_id)
