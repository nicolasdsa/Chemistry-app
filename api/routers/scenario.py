from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from controllers.scenario import (
    ScenarioCreatePayload,
    ScenarioUpdatePayload,
    create_scenario,
    delete_scenario,
    get_scenario,
    list_scenarios,
    update_scenario,
)

router = APIRouter(
    prefix="/scenarios",
    tags=["Scenarios"],
    default_response_class=HTMLResponse,
)


@router.post("/", response_model=HTMLResponse, status_code=201)
def create_scenario_route(payload: ScenarioCreatePayload) -> HTMLResponse:
    return create_scenario(payload)


@router.get("/", response_model=HTMLResponse)
def list_scenarios_route() -> HTMLResponse:
    return list_scenarios()


@router.get("/{scenario_id}", response_model=HTMLResponse)
def get_scenario_route(scenario_id: int) -> HTMLResponse:
    return get_scenario(scenario_id)


@router.put("/{scenario_id}", response_model=HTMLResponse)
def update_scenario_route(
    scenario_id: int, payload: ScenarioUpdatePayload
) -> HTMLResponse:
    return update_scenario(scenario_id, payload)


@router.delete("/{scenario_id}", response_model=HTMLResponse, status_code=204)
def delete_scenario_route(scenario_id: int) -> HTMLResponse:
    return delete_scenario(scenario_id)
