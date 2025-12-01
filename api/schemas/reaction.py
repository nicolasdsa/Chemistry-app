from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReactionReagentBase(BaseModel):
    reagent_id: int
    coefficient: int = 1
    role: str


class ReactionReagentCreate(ReactionReagentBase):
    reaction_id: int


class ReactionReagentUpdate(BaseModel):
    reagent_id: Optional[int] = None
    coefficient: Optional[int] = None
    role: Optional[str] = None


class ReactionReagentRead(ReactionReagentBase):
    id: int
    reaction_id: int

    model_config = ConfigDict(from_attributes=True)


class ReactionBase(BaseModel):
    scenario_id: Optional[int] = None
    description: str
    product_reagent_id: int
    reaction_key: str
    message: str


class ReactionCreate(ReactionBase):
    pass


class ReactionUpdate(BaseModel):
    scenario_id: Optional[int] = None
    description: Optional[str] = None
    product_reagent_id: Optional[int] = None
    reaction_key: Optional[str] = None
    message: Optional[str] = None


class ReactionRead(ReactionBase):
    id: int
    reagents: list[ReactionReagentRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
