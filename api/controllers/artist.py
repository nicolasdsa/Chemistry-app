from __future__ import annotations

import json

from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from schemas.artist import ArtistCreate, ArtistRead, ArtistUpdate
from services import artist as artist_service


def create_artist(payload: ArtistCreate, db: Session):
    artist = artist_service.create_artist(db=db, data=payload)
    data = ArtistRead.model_validate(artist).model_dump(mode="json")
    return HTMLResponse(content=json.dumps(data), status_code=201)


def list_artists(db: Session):
    artists = artist_service.list_artists(db)
    data = [ArtistRead.model_validate(item).model_dump(mode="json") for item in artists]
    return HTMLResponse(content=json.dumps(data), status_code=200)


def get_artist(artist_id: int, db: Session):
    artist = artist_service.get_artist(db, artist_id)
    data = ArtistRead.model_validate(artist).model_dump(mode="json")
    return HTMLResponse(content=json.dumps(data), status_code=200)


def update_artist(artist_id: int, payload: ArtistUpdate, db: Session):
    artist = artist_service.update_artist(db, artist_id, payload)
    data = ArtistRead.model_validate(artist).model_dump(mode="json")
    return HTMLResponse(content=json.dumps(data), status_code=200)


def delete_artist(artist_id: int, db: Session):
    artist_service.delete_artist(db, artist_id)
    return HTMLResponse(content="", status_code=204)
