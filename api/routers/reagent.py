from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from controllers.reagent import create_reagent, list_reagents, get_reagent, update_reagent, delete_reagent
from schemas.reagent import ReagentCreate, ReagentUpdate

router = APIRouter(
    prefix="/reagents",
    tags=["Reagents"],
    default_response_class=HTMLResponse,
)

@router.post("/", response_model=HTMLResponse)
def create_reagent_route(
    payload: ReagentCreate,
) -> HTMLResponse:
    return create_reagent(payload)

@router.get("/", response_model=HTMLResponse)
def list_reagents_route() -> HTMLResponse:
    return list_reagents()

@router.get("/{reagent_id}", response_model=HTMLResponse)
def get_reagent_route(reagent_id: int) -> HTMLResponse:
    return get_reagent(reagent_id)

@router.put("/{reagent_id}", response_model=HTMLResponse)
def update_reagent_route(
    reagent_id: int,
    payload: ReagentUpdate,
) -> HTMLResponse:
    return update_reagent(reagent_id, payload)

@router.delete(
    "/{reagent_id}",
    response_model=HTMLResponse,
)    
def delete_reagent_route(reagent_id: int) -> HTMLResponse:
    return delete_reagent(reagent_id)
