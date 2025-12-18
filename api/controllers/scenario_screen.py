from __future__ import annotations

import json

from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from schemas.scenario_screen import ScenarioScreenCreate, ScenarioScreenRead
from services import scenario as scenario_service
from services import scenario_screen as scenario_screen_service


def get_screen(screen_id: int, db: Session):
    screen = scenario_screen_service.get_screen(db, screen_id)
    data = ScenarioScreenRead.model_validate(screen).model_dump(mode="json")
    return HTMLResponse(content=json.dumps(data), status_code=200)


def list_screens_for_scenario(scenario_id: int, db: Session):
    scenario_service.get_scenario_by_id(db, scenario_id)
    screens = scenario_screen_service.list_screens_for_scenario(db, scenario_id)
    data = [ScenarioScreenRead.model_validate(item).model_dump(mode="json") for item in screens]
    return HTMLResponse(content=json.dumps(data), status_code=200)


def create_screens_for_scenario(
    scenario_id: int, screens: list[ScenarioScreenCreate], db: Session
):
    scenario = scenario_service.get_scenario_by_id(db, scenario_id)
    created = scenario_screen_service.create_screens_for_scenario(
        db=db, scenario=scenario, screens_data=[screen.model_dump() for screen in screens]
    )
    db.commit()
    for screen in created:
        db.refresh(screen)
    data = [ScenarioScreenRead.model_validate(item).model_dump(mode="json") for item in created]
    return HTMLResponse(content=json.dumps(data), status_code=201)
