from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from models.reaction import Reaction
from services.reaction import _generate_reaction_key

RunState = Dict[str, Any]

# In-memory store for active runs
_runs: Dict[str, RunState] = {}


def start_scenario_run(scenario_id: int) -> RunState:
    run_id = str(uuid.uuid4())
    state: RunState = {"run_id": run_id, "scenario_id": scenario_id, "containers": {}}
    _runs[run_id] = state
    return state


def get_run_state(run_id: str) -> RunState:
    if run_id not in _runs:
        raise NotFoundError("Execução do cenário não encontrada.")
    return _runs[run_id]


def add_reagent_to_container(
    db: Session, run_id: str, container_name: str, reagent_id: int
) -> RunState:
    state = get_run_state(run_id)
    containers: Dict[str, List[int]] = state.setdefault("containers", {})
    reagents = containers.setdefault(container_name, [])
    reagents.append(reagent_id)

    reaction_key = _generate_reaction_key(reagents)
    reaction = (
        db.query(Reaction)
        .filter(
            Reaction.reaction_key == reaction_key,
            or_(Reaction.scenario_id == state["scenario_id"], Reaction.scenario_id.is_(None)),
        )
        .first()
    )

    message: Optional[str] = None
    if reaction:
        containers[container_name] = [reaction.product_reagent_id]
        message = reaction.message
        state["message"] = message
    else:
        state.pop("message", None)

    return state
