from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.dependencies import get_db  
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


@router.post("/", response_class=HTMLResponse, status_code=201)
def create_scenario_route(
    payload: ScenarioCreatePayload,
    db: Session = Depends(get_db)  
):
    return create_scenario(payload, db)


@router.get("/", response_class=HTMLResponse)
def list_scenarios_route(
    db: Session = Depends(get_db)
):
    return list_scenarios(db)


@router.get("/{scenario_id}", response_class=HTMLResponse)
def get_scenario_route(
    scenario_id: int,
    db: Session = Depends(get_db)
):
    return get_scenario(scenario_id, db)


@router.put("/{scenario_id}", response_class=HTMLResponse)
def update_scenario_route(
    scenario_id: int, 
    payload: ScenarioUpdatePayload,
    db: Session = Depends(get_db)
):
    return update_scenario(scenario_id, payload, db)


@router.delete("/{scenario_id}", response_class=HTMLResponse, status_code=204)
def delete_scenario_route(
    scenario_id: int,
    db: Session = Depends(get_db)
):
    return delete_scenario(scenario_id, db)