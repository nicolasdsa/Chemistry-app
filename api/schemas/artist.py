from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ArtistTimelineEntryBase(BaseModel):
    year: int
    title: str | None = None
    description: str


class ArtistTimelineEntryCreate(ArtistTimelineEntryBase):
    pass


class ArtistTimelineEntryRead(ArtistTimelineEntryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ArtistBase(BaseModel):
    name: str
    image_path: str | None = None
    bio: str


class ArtistCreate(ArtistBase):
    timeline: list[ArtistTimelineEntryCreate] | None = None


class ArtistUpdate(BaseModel):
    name: str | None = None
    image_path: str | None = None
    bio: str | None = None
    timeline: list[ArtistTimelineEntryCreate] | None = None


class ArtistRead(ArtistBase):
    id: int
    timeline: list[ArtistTimelineEntryRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
