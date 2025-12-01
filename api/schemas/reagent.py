from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ReagentBase(BaseModel):
    name: str
    formula: str
    physical_state: str
    tags: Optional[Any] = None


class ReagentCreate(ReagentBase):
    pass


class ReagentUpdate(BaseModel):
    name: Optional[str] = None
    formula: Optional[str] = None
    physical_state: Optional[str] = None
    tags: Optional[Any] = None


class ReagentRead(ReagentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
