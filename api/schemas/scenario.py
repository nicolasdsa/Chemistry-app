from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ScenarioStepBase(BaseModel):
    scenario_id: Optional[int] = None
    order_index: int
    action_type: str
    instrument_id: Optional[int] = None
    reagent_id: Optional[int] = None
    source_container_name: Optional[str] = None
    target_container_name: Optional[str] = None
    amount_value: Optional[float] = None
    amount_unit: Optional[str] = None
    text_instruction: str
    sound_effect_path: Optional[str] = None


class ScenarioStepCreate(ScenarioStepBase):
    scenario_id: int
    action_type: str


class ScenarioStepUpdate(BaseModel):
    order_index: Optional[int] = None
    action_type: Optional[str] = None
    instrument_id: Optional[int] = None
    reagent_id: Optional[int] = None
    source_container_name: Optional[str] = None
    target_container_name: Optional[str] = None
    amount_value: Optional[float] = None
    amount_unit: Optional[str] = None
    text_instruction: Optional[str] = None
    sound_effect_path: Optional[str] = None


class ScenarioStepRead(ScenarioStepBase):
    id: int
    scenario_id: int
    source_container_name: Optional[str] = None
    target_container_name: Optional[str] = None
    amount_value: Optional[float] = None
    amount_unit: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ScenarioBase(BaseModel):
    title: str
    description: str
    is_active: bool = True
    initial_state: Optional[dict[str, Any]] = None


class ScenarioCreate(ScenarioBase):
    pass


class ScenarioUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    initial_state: Optional[dict[str, Any]] = None


class ScenarioRead(ScenarioBase):
    id: int
    created_at: datetime
    updated_at: datetime
    steps: list[ScenarioStepRead] = Field(default_factory=list)
    initial_state: Optional[dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)
