from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class InstrumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None
    instrument_type: str
    is_container: bool = True
    allowed_physical_states: Optional[str] = None


class InstrumentCreate(InstrumentBase):
    is_container: bool = True
    allowed_physical_states: Optional[str] = None


class InstrumentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_path: Optional[str] = None
    instrument_type: Optional[str] = None
    is_container: Optional[bool] = None
    allowed_physical_states: Optional[str] = None


class InstrumentRead(InstrumentBase):
    id: int
    instrument_type: str
    is_container: bool
    allowed_physical_states: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
