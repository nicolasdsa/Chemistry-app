from __future__ import annotations

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from core.dependencies import get_db
from core.templates import templates
from core.exceptions import BadRequestError, NotFoundError
from services import scenario_run as run_service


def run_state_partial(
    run_id: str, request: Request, db: Session = Depends(get_db)
) -> HTMLResponse:
    run_state = run_service.get_run_state(run_id, db=db)
    return templates.TemplateResponse(
        "scenario_runs/partials/state.html",
        {
            "request": request,
        "run_state": run_state,
    },
)


async def apply_action_ui(
    request: Request,
    run_id: str,
    action_type: str,
    instrument_id: int | None,
    source_container_name: str | None,
    target_container_name: str | None,
    reagent_id: int | None,
    amount_value: float | None,
    amount_unit: str | None,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    source_container_name = source_container_name or None
    target_container_name = target_container_name or None
    amount_unit = amount_unit or None
    try:
        run_service.apply_action(
            run_id=run_id,
            action_type=action_type,
            instrument_id=instrument_id,
            source_container_name=source_container_name,
            target_container_name=target_container_name,
            reagent_id=reagent_id,
            amount_value=amount_value,
            amount_unit=amount_unit,
            db=db,
        )
        run_state = run_service.get_run_state(run_id, db=db)
        return templates.TemplateResponse(
            "scenario_runs/partials/state.html",
            {
                "request": request,
                "run_state": run_state,
                "error_message": None,
            },
        )
    except (BadRequestError, NotFoundError) as exc:
        run_state = run_service.get_run_state(run_id, db=db)
        return templates.TemplateResponse(
            "scenario_runs/partials/state.html",
            {
                "request": request,
                "run_state": run_state,
                "error_message": str(exc),
            },
            status_code=400,
        )
