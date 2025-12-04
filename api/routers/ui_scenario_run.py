from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from controllers import ui_scenario_run
from core.dependencies import get_db

router = APIRouter(
    prefix="/ui/scenario-runs",
    tags=["ui-scenario-runs"],
    default_response_class=HTMLResponse,
)


@router.get("/{run_id}/state", response_class=HTMLResponse)
def run_state_partial(run_id: str, request: Request, db: Session = Depends(get_db)):
    return ui_scenario_run.run_state_partial(run_id, request, db)


@router.post("/{run_id}/actions", response_class=HTMLResponse)
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
):
    return await ui_scenario_run.apply_action_ui(
        request=request,
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
