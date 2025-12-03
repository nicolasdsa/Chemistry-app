from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.dependencies import get_db  
from controllers.reaction import (
    ReactionCreatePayload,
    ReactionUpdatePayload,
    create_reaction,
    delete_reaction,
    get_reaction,
    list_reactions,
    update_reaction,
)

router = APIRouter(
    prefix="/reactions",
    tags=["Reactions"],
    default_response_class=HTMLResponse,
)


@router.post("/", response_class=HTMLResponse, status_code=201)
def create_reaction_route(
    payload: ReactionCreatePayload,
    db: Session = Depends(get_db)  
):
    return create_reaction(payload, db)  

@router.get("/", response_class=HTMLResponse)
def list_reactions_route(
    db: Session = Depends(get_db)
):
    return list_reactions(db)


@router.get("/{reaction_id}", response_class=HTMLResponse)
def get_reaction_route(
    reaction_id: int,
    db: Session = Depends(get_db)
):
    return get_reaction(reaction_id, db)


@router.put("/{reaction_id}", response_class=HTMLResponse)
def update_reaction_route(
    reaction_id: int, 
    payload: ReactionUpdatePayload,
    db: Session = Depends(get_db)
):
    return update_reaction(reaction_id, payload, db)


@router.delete("/{reaction_id}", response_class=HTMLResponse, status_code=204)
def delete_reaction_route(
    reaction_id: int,
    db: Session = Depends(get_db)
):
    return delete_reaction(reaction_id, db)