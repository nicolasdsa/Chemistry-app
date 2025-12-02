from __future__ import annotations

import json

from fastapi import Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.dependencies import get_db
from services import scenario_run as run_service


class StartRunPayload(BaseModel):
    scenario_id: int


class AddReagentPayload(BaseModel):
    container_name: str
    reagent_id: int


def start_run(payload: StartRunPayload) -> HTMLResponse:
    state = run_service.start_scenario_run(payload.scenario_id)
    return HTMLResponse(content=json.dumps(state), status_code=201)


def get_run(run_id: str) -> HTMLResponse:
    state = run_service.get_run_state(run_id)
    return HTMLResponse(content=json.dumps(state), status_code=200)


def add_reagent(
    run_id: str, payload: AddReagentPayload, db: Session = Depends(get_db)
) -> HTMLResponse:
    state = run_service.add_reagent_to_container(
        db=db,
        run_id=run_id,
        container_name=payload.container_name,
        reagent_id=payload.reagent_id,
    )
    return HTMLResponse(content=json.dumps(state), status_code=200)
