from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from vision.marker_generator import MARKER_DIR, generate_aruco_marker

router = APIRouter(prefix="/markers", tags=["markers"])


@router.get("/{marker_id}/image", response_class=FileResponse)
def get_marker_image(
    marker_id: int,
    size: int = Query(600, ge=100, le=2000, description="Lado em pixels"),
) -> FileResponse:
    """
    Generates (if necessary) and returns the PNG image of the ArUco marker for printing.
    """
    relative_path = generate_aruco_marker(marker_id=marker_id, size_px=size)
    abs_path = Path(MARKER_DIR.parent) / relative_path
    if not abs_path.exists():
        raise HTTPException(status_code=404, detail="Imagem do marcador não encontrada.")
    return FileResponse(path=abs_path, media_type="image/png")


__all__ = ["router"]
