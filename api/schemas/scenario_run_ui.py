from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ScenarioRunUIActionApply(BaseModel):
    action_type: str
    instrument_id: Optional[int] = None
    source_container_name: Optional[str] = None
    target_container_name: Optional[str] = None
    reagent_id: Optional[int] = None
    amount_value: Optional[float] = None
    amount_unit: Optional[str] = None
