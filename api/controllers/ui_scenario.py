from __future__ import annotations

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.dependencies import get_db
from core.templates import templates
from services import scenario as scenario_service
from services import scenario_run as run_service


def list_scenarios_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    scenarios = [s for s in scenario_service.list_scenarios(db) if s.is_active]
    return templates.TemplateResponse(
        "scenarios/list.html",
        {
            "request": request,
            "scenarios": scenarios,
        },
    )


def run_scenario_page(
    scenario_id: int, request: Request, db: Session = Depends(get_db)
) -> HTMLResponse:
    scenario = scenario_service.get_scenario_by_id(db, scenario_id)
    run_state = run_service.start_scenario_run(scenario_id, db=db)
    return templates.TemplateResponse(
        "scenario_runs/run.html",
        {
            "request": request,
            "scenario": scenario,
            "run_state": run_state,
        },
    )
