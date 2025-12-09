from __future__ import annotations

import asyncio
from typing import AsyncGenerator

import cv2
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import StreamingResponse

from vision.camera_config import open_camera

router = APIRouter(prefix="/camera", tags=["camera"])


def _encode_frame_to_jpeg(frame) -> bytes:
    ok, buffer = cv2.imencode(".jpg", frame)
    if not ok:
        raise HTTPException(status_code=500, detail="Falha ao codificar frame da câmera.")
    return buffer.tobytes()


@router.get("/frame", response_class=Response)
async def get_frame(request: Request, device: str | None = None) -> Response:
    """
    Returns a single snapshot (JPEG) from the camera. Uses the latest frame from the listener
    if available; otherwise, it attempts to quickly open the camera.
    """
    frame = getattr(request.app.state, "latest_frame", None)
    chosen_device = device or getattr(request.app.state, "camera_device", None)

    if frame is None:
        try:
            capture = open_camera(device=chosen_device)
            ok, frame = capture.read()
            capture.release()
            if not ok:
                frame = None
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=503, detail=f"Câmera indisponível: {exc}") from exc

    if frame is None:
        raise HTTPException(status_code=503, detail="Câmera indisponível.")

    jpeg_bytes = _encode_frame_to_jpeg(frame)
    return Response(content=jpeg_bytes, media_type="image/jpeg")


@router.get("/stream")
async def stream(request: Request, device: str | None = None) -> StreamingResponse:
    """
    Simple MJPEG stream. Uses the latest frame seen by the listener; if it is not
    available, it attempts to open the camera locally as a fallback.
    """
    boundary = "frame"
    chosen_device = device or getattr(request.app.state, "camera_device", None)

    async def _frame_generator() -> AsyncGenerator[bytes, None]:
        capture = None
        try:
            while True:
                frame = getattr(request.app.state, "latest_frame", None)
                if frame is None:
                    if capture is None:
                        try:
                            capture = open_camera(device=chosen_device)
                        except Exception:
                            yield b""
                            break
                    ok, frame = capture.read()
                    if not ok:
                        break
                try:
                    jpeg_bytes = _encode_frame_to_jpeg(frame)
                except HTTPException:
                    break

                yield (
                    b"--" + boundary.encode() + b"\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg_bytes + b"\r\n"
                )
                await asyncio.sleep(0.2)
        finally:
            if capture is not None:
                capture.release()

    return StreamingResponse(
        _frame_generator(),
        media_type=f"multipart/x-mixed-replace; boundary={boundary}",
    )
