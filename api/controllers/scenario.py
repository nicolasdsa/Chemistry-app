from __future__ import annotations

import json
from typing import Optional

from fastapi.responses import HTMLResponse
from pydantic import Field
from sqlalchemy.orm import Session

from schemas.scenario import (
    ScenarioCreate,
    ScenarioRead,
    ScenarioStepBase,
    ScenarioUpdate,
)
from services import scenario as scenario_service


class ScenarioCreatePayload(ScenarioCreate):
    steps: list[ScenarioStepBase] = Field(default_factory=list)


class ScenarioUpdatePayload(ScenarioUpdate):
    steps: Optional[list[ScenarioStepBase]] = None


def create_scenario(payload: ScenarioCreatePayload, db: Session):
    scenario = scenario_service.create_scenario(
        db=db,
        title=payload.title,
        description=payload.description,
        is_active=payload.is_active,
        steps=[step.model_dump() for step in payload.steps],
    )
    data = ScenarioRead.model_validate(scenario).model_dump(mode='json')
    return HTMLResponse(content=json.dumps(data), status_code=201)


def list_scenarios(db: Session):
    scenarios = scenario_service.list_scenarios(db)
    data = [ScenarioRead.model_validate(item).model_dump(mode='json') for item in scenarios]
    return HTMLResponse(content=json.dumps(data), status_code=200)


def get_scenario(scenario_id: int, db: Session):
    scenario = scenario_service.get_scenario_by_id(db, scenario_id)
    data = ScenarioRead.model_validate(scenario).model_dump(mode='json')
    return HTMLResponse(content=json.dumps(data), status_code=200)


def update_scenario(
    scenario_id: int, payload: ScenarioUpdatePayload, db: Session
):
    scenario = scenario_service.update_scenario(
        db=db,
        scenario_id=scenario_id,
        title=payload.title,
        description=payload.description,
        is_active=payload.is_active,
        steps=[step.model_dump() for step in payload.steps] if payload.steps is not None else None,
    )
    data = ScenarioRead.model_validate(scenario).model_dump(mode='json')
    return HTMLResponse(content=json.dumps(data), status_code=200)


def delete_scenario(scenario_id: int, db: Session):
    scenario_service.delete_scenario(db, scenario_id)
    return HTMLResponse(content="", status_code=204)