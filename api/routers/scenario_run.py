from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.dependencies import get_db  
from controllers.scenario_run import (
    AddReagentPayload,
    StartRunPayload,
    add_reagent,
    apply_action_to_run,
    get_run,
    start_run,
)
from schemas.scenario_run import ScenarioRunActionApply

router = APIRouter(
    prefix="/scenario-runs",
    tags=["ScenarioRuns"],
    default_response_class=HTMLResponse,
)


@router.post("/", response_class=HTMLResponse, status_code=201)
def start_run_route(
    payload: StartRunPayload,
    db: Session = Depends(get_db)  
):
    return start_run(payload, db) 


@router.post("/{run_id}/actions/add-reagent", response_class=HTMLResponse)
def add_reagent_route(
    run_id: str, 
    payload: AddReagentPayload,
    db: Session = Depends(get_db)
):
    return add_reagent(run_id, payload, db)


@router.post("/{run_id}/actions", response_class=HTMLResponse)
def apply_action_route(
    run_id: str, 
    payload: ScenarioRunActionApply,
    db: Session = Depends(get_db)
):
    return apply_action_to_run(run_id, payload, db)


@router.get("/{run_id}", response_class=HTMLResponse)
def get_run_route(
    run_id: str,
    db: Session = Depends(get_db)
):
    return get_run(run_id, db)
