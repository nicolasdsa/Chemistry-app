from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from controllers.artist import (
    create_artist,
    delete_artist,
    get_artist,
    list_artists,
    update_artist,
)
from schemas.artist import ArtistCreate, ArtistUpdate
from core.dependencies import get_db


router = APIRouter(
    prefix="/artists",
    tags=["Artists"],
    default_response_class=HTMLResponse,
)


@router.post("/", response_class=HTMLResponse, status_code=201)
def create_artist_route(payload: ArtistCreate, db: Session = Depends(get_db)):
    return create_artist(payload, db)


@router.get("/", response_class=HTMLResponse)
def list_artists_route(db: Session = Depends(get_db)):
    return list_artists(db)


@router.get("/{artist_id}", response_class=HTMLResponse)
def get_artist_route(artist_id: int, db: Session = Depends(get_db)):
    return get_artist(artist_id, db)


@router.put("/{artist_id}", response_class=HTMLResponse)
@router.patch("/{artist_id}", response_class=HTMLResponse)
def update_artist_route(
    artist_id: int, payload: ArtistUpdate, db: Session = Depends(get_db)
):
    return update_artist(artist_id, payload, db)


@router.delete("/{artist_id}", response_class=HTMLResponse, status_code=204)
def delete_artist_route(artist_id: int, db: Session = Depends(get_db)):
    return delete_artist(artist_id, db)
