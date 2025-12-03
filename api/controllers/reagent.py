from __future__ import annotations

import json

from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from schemas.reagent import (
    ReagentCreate,
    ReagentRead,
    ReagentUpdate,
)
from services import reagent as reagent_service


def create_reagent(payload: ReagentCreate, db: Session): 
    reagent = reagent_service.create_reagent(
        db=db,
        name=payload.name,
        formula=payload.formula,
        physical_state=payload.physical_state,
        tags=payload.tags,
    )
    data = ReagentRead.model_validate(reagent).model_dump()
    return HTMLResponse(content=json.dumps(data), status_code=201)


def list_reagents(db: Session):
    reagents = reagent_service.list_reagents(db)
    data = [ReagentRead.model_validate(item).model_dump() for item in reagents]
    return HTMLResponse(content=json.dumps(data), status_code=200)


def get_reagent(reagent_id: int, db: Session):
    reagent = reagent_service.get_reagent_by_id(db, reagent_id)
    data = ReagentRead.model_validate(reagent).model_dump()
    return HTMLResponse(content=json.dumps(data), status_code=200)


def update_reagent(reagent_id: int, payload: ReagentUpdate, db: Session):
    reagent = reagent_service.update_reagent(
        db=db,
        reagent_id=reagent_id,
        name=payload.name,
        formula=payload.formula,
        physical_state=payload.physical_state,
        tags=payload.tags,
    )
    data = ReagentRead.model_validate(reagent).model_dump()
    return HTMLResponse(content=json.dumps(data), status_code=200)


def delete_reagent(reagent_id: int, db: Session):
    reagent_service.delete_reagent(db, reagent_id)
    return HTMLResponse(content="", status_code=204)