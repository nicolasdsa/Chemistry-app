from __future__ import annotations

import json
from typing import Optional

from fastapi import Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.dependencies import get_db
from schemas.reaction import ReactionRead, ReactionReagentBase, ReactionUpdate
from services import reaction as reaction_service


class ReactionCreatePayload(BaseModel):
    scenario_id: Optional[int] = None
    description: str
    product_reagent_id: int
    message: str
    reagents: list[ReactionReagentBase] = Field(default_factory=list)


class ReactionUpdatePayload(ReactionUpdate):
    reagents: Optional[list[ReactionReagentBase]] = None


def create_reaction(payload: ReactionCreatePayload, db: Session = Depends(get_db)) -> HTMLResponse:
    reaction = reaction_service.create_reaction(
        db=db,
        description=payload.description,
        product_reagent_id=payload.product_reagent_id,
        message=payload.message,
        scenario_id=payload.scenario_id,
        reagents=[item.model_dump() for item in payload.reagents],
    )
    data = ReactionRead.model_validate(reaction).model_dump()
    return HTMLResponse(content=json.dumps(data), status_code=201)


def list_reactions(db: Session = Depends(get_db)) -> HTMLResponse:
    reactions = reaction_service.list_reactions(db)
    data = [ReactionRead.model_validate(item).model_dump() for item in reactions]
    return HTMLResponse(content=json.dumps(data), status_code=200)


def get_reaction(reaction_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    reaction = reaction_service.get_reaction_by_id(db, reaction_id)
    data = ReactionRead.model_validate(reaction).model_dump()
    return HTMLResponse(content=json.dumps(data), status_code=200)


def update_reaction(
    reaction_id: int, payload: ReactionUpdatePayload, db: Session = Depends(get_db)
) -> HTMLResponse:
    reaction = reaction_service.update_reaction(
        db=db,
        reaction_id=reaction_id,
        description=payload.description,
        product_reagent_id=payload.product_reagent_id,
        message=payload.message,
        scenario_id=payload.scenario_id,
        reagents=[item.model_dump() for item in payload.reagents] if payload.reagents is not None else None,
    )
    data = ReactionRead.model_validate(reaction).model_dump()
    return HTMLResponse(content=json.dumps(data), status_code=200)


def delete_reaction(reaction_id: int, db: Session = Depends(get_db)) -> HTMLResponse:
    reaction_service.delete_reaction(db, reaction_id)
    return HTMLResponse(content="", status_code=204)
