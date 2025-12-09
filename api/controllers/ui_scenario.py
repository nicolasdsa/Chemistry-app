from __future__ import annotations

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.dependencies import get_db
from core.database import SessionLocal
from core.templates import templates
from models.instrument import Instrument
from models.reagent import Reagent
from services import scenario as scenario_service
from services import scenario_run as run_service
from services.utils_instruments import split_instruments_by_container
from vision.aruco_listener import start_aruco_listener


def _ensure_aruco_listener(request: Request) -> None:
    """
    Start the ArUco listener only when the user starts a scenario in the UI.
    """
    state = request.app.state
    if getattr(state, "aruco_listener_started", False):
        return
    state.db_session_factory = getattr(state, "db_session_factory", SessionLocal)
    state.latest_frame = getattr(state, "latest_frame", None)
    start_aruco_listener(state)
    state.aruco_listener_started = True


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
    camera_device = request.query_params.get("device") or request.query_params.get("camera")
    scenario = scenario_service.get_scenario_by_id(db, scenario_id)
    run_state = run_service.start_scenario_run(scenario_id, db=db)
    request.app.state.current_run_id = run_state.get("run_id")
    if camera_device:
        request.app.state.camera_device = camera_device
    _ensure_aruco_listener(request)
    reagents = db.query(Reagent).all()
    all_instruments = db.query(Instrument).all()
    transfer_instruments, container_instruments = split_instruments_by_container(all_instruments)
    containers_meta = run_state.get("containers_meta", {})
    container_names = [
        name for name, meta in containers_meta.items() if meta.get("is_container")
    ]
    instrument_map = {inst.id: inst.name for inst in all_instruments}
    return templates.TemplateResponse(
        "scenario_runs/run.html",
        {
            "request": request,
            "scenario": scenario,
            "run_state": run_state,
            "reagents": reagents,
            "transfer_instruments": transfer_instruments,
            "container_names": container_names,
            "containers_meta": containers_meta,
            "instrument_map": instrument_map,
        },
    )
