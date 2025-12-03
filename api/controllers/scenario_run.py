from __future__ import annotations

import json

from fastapi import Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.dependencies import get_db
from schemas.scenario_run import ScenarioRunActionApply
from services import scenario_run as run_service


class StartRunPayload(BaseModel):
    scenario_id: int


class AddReagentPayload(BaseModel):
    container_name: str
    reagent_id: int


def start_run(payload: StartRunPayload, db: Session = Depends(get_db)):
    state = run_service.start_scenario_run(payload.scenario_id, db=db)
    return HTMLResponse(content=json.dumps(state), status_code=201)


def get_run(run_id: str, db: Session = Depends(get_db)):
    state = run_service.get_run_state(run_id, db=db)
    return HTMLResponse(content=json.dumps(state), status_code=200)


def add_reagent(
    run_id: str, payload: AddReagentPayload, db: Session = Depends(get_db)
):
    state = run_service.add_reagent_to_container(
        db=db,
        run_id=run_id,
        container_name=payload.container_name,
        reagent_id=payload.reagent_id,
    )
    return HTMLResponse(content=json.dumps(state), status_code=200)


def apply_action_to_run(
    run_id: str, action_data: ScenarioRunActionApply, db: Session = Depends(get_db)
):
    state = run_service.apply_action(
        run_id=run_id,
        action_type=action_data.action_type,
        instrument_id=action_data.instrument_id,
        source_container_name=action_data.source_container_name,
        target_container_name=action_data.target_container_name,
        reagent_id=action_data.reagent_id,
        amount_value=action_data.amount_value,
        amount_unit=action_data.amount_unit,
        db=db,
    )
    return HTMLResponse(content=json.dumps(state), status_code=200)
