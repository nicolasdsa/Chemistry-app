from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from controllers.scenario_run import (
    AddReagentPayload,
    StartRunPayload,
    add_reagent,
    get_run,
    start_run,
)

router = APIRouter(
    prefix="/scenario-runs",
    tags=["ScenarioRuns"],
    default_response_class=HTMLResponse,
)


@router.post("/", response_model=HTMLResponse, status_code=201)
def start_run_route(payload: StartRunPayload) -> HTMLResponse:
    return start_run(payload)


@router.post("/{run_id}/actions/add-reagent", response_model=HTMLResponse)
def add_reagent_route(run_id: str, payload: AddReagentPayload) -> HTMLResponse:
    return add_reagent(run_id, payload)


@router.get("/{run_id}", response_model=HTMLResponse)
def get_run_route(run_id: str) -> HTMLResponse:
    return get_run(run_id)
