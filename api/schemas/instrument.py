from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class InstrumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None


class InstrumentCreate(InstrumentBase):
    pass


class InstrumentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_path: Optional[str] = None


class InstrumentRead(InstrumentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
