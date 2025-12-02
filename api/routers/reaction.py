from fastapi import APIRouter
from fastapi.responses import HTMLResponse

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


@router.post("/", response_model=HTMLResponse, status_code=201)
def create_reaction_route(payload: ReactionCreatePayload) -> HTMLResponse:
    return create_reaction(payload)


@router.get("/", response_model=HTMLResponse)
def list_reactions_route() -> HTMLResponse:
    return list_reactions()


@router.get("/{reaction_id}", response_model=HTMLResponse)
def get_reaction_route(reaction_id: int) -> HTMLResponse:
    return get_reaction(reaction_id)


@router.put("/{reaction_id}", response_model=HTMLResponse)
def update_reaction_route(
    reaction_id: int, payload: ReactionUpdatePayload
) -> HTMLResponse:
    return update_reaction(reaction_id, payload)


@router.delete("/{reaction_id}", response_model=HTMLResponse, status_code=204)
def delete_reaction_route(reaction_id: int) -> HTMLResponse:
    return delete_reaction(reaction_id)
