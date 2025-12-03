from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from controllers.reagent import create_reagent, list_reagents, get_reagent, update_reagent, delete_reagent
from schemas.reagent import ReagentCreate, ReagentUpdate
from core.dependencies import get_db  

router = APIRouter(
    prefix="/reagents",
    tags=["Reagents"],
    default_response_class=HTMLResponse,
)

@router.post("/", response_class=HTMLResponse)
def create_reagent_route(
    payload: ReagentCreate,
    db: Session = Depends(get_db) 
):
    return create_reagent(payload, db)

@router.get("/", response_class=HTMLResponse)
def list_reagents_route(
    db: Session = Depends(get_db) 
):
    return list_reagents(db)

@router.get("/{reagent_id}", response_class=HTMLResponse)
def get_reagent_route(
    reagent_id: int, 
    db: Session = Depends(get_db)
):
    return get_reagent(reagent_id, db)

@router.put("/{reagent_id}", response_class=HTMLResponse)
def update_reagent_route(
    reagent_id: int,
    payload: ReagentUpdate,
    db: Session = Depends(get_db)
):
    return update_reagent(reagent_id, payload, db)

@router.delete("/{reagent_id}", response_class=HTMLResponse)    
def delete_reagent_route(
    reagent_id: int,
    db: Session = Depends(get_db)
):
    return delete_reagent(reagent_id, db)