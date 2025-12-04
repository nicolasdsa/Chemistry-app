from __future__ import annotations

from fastapi import Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.dependencies import get_db
from core.templates import templates
from core.exceptions import BadRequestError, NotFoundError
from models.reagent import Reagent
from models.scenario import Scenario
from models.instrument import Instrument
from services import scenario_run as run_service


def _build_reagents_map(db: Session) -> dict[int, str]:
    reagents = db.query(Reagent).all()
    return {r.id: r.name for r in reagents}


def _build_instrument_map(db: Session) -> dict[int, str]:
    instruments = db.query(Instrument).all()
    return {i.id: i.name for i in instruments}


def run_state_partial(
    run_id: str,
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    run_state = run_service.get_run_state(run_id, db=db)
    reagents_map = _build_reagents_map(db)
    instrument_map = _build_instrument_map(db)
    scenario = db.get(Scenario, run_state["scenario_id"])
    return templates.TemplateResponse(
        "scenario_runs/partials/state.html",
        {
            "request": request,
            "run_state": run_state,
            "scenario": scenario,
            "reagents_map": reagents_map,
            "instrument_map": instrument_map,
            "error_message": None,
        },
    )


async def apply_action_ui(
    request: Request,
    run_id: str,
    action_type: str = Form(...),
    instrument_id: str = Form(""),
    source_container_name: str = Form(""),
    target_container_name: str = Form(""),
    reagent_id: str = Form(""),
    amount_value: str = Form(""),
    amount_unit: str = Form(""),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    # Normaliza e converte campos de formulário
    source_container_name = source_container_name or None
    target_container_name = target_container_name or None
    amount_unit = amount_unit or None
    instrument_id_val = int(instrument_id) if instrument_id not in (None, "") else None
    reagent_id_val = int(reagent_id) if reagent_id not in (None, "") else None
    amount_value_val = float(amount_value) if amount_value not in (None, "") else None

    try:
        run_service.apply_action(
            run_id=run_id,
            action_type=action_type,
            instrument_id=instrument_id_val,
            source_container_name=source_container_name,
            target_container_name=target_container_name,
            reagent_id=reagent_id_val,
            amount_value=amount_value_val,
            amount_unit=amount_unit,
            db=db,
        )
        run_state = run_service.get_run_state(run_id, db=db)
        reagents_map = _build_reagents_map(db)
        instrument_map = _build_instrument_map(db)
        scenario = db.get(Scenario, run_state["scenario_id"])
        return templates.TemplateResponse(
            "scenario_runs/partials/state.html",
            {
                "request": request,
                "run_state": run_state,
                "scenario": scenario,
                "reagents_map": reagents_map,
                "instrument_map": instrument_map,
                "error_message": None,
            },
        )
    except (BadRequestError, NotFoundError) as exc:
        run_state = run_service.get_run_state(run_id, db=db)
        reagents_map = _build_reagents_map(db)
        instrument_map = _build_instrument_map(db)
        scenario = db.get(Scenario, run_state["scenario_id"])
        return templates.TemplateResponse(
            "scenario_runs/partials/state.html",
            {
                "request": request,
                "run_state": run_state,
                "scenario": scenario,
                "reagents_map": reagents_map,
                "instrument_map": instrument_map,
                "error_message": str(exc),
            },
            status_code=400,
        )
