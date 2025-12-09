from __future__ import annotations

from typing import Iterable, Optional, Tuple, Union

import cv2

DEFAULT_DEVICE: Union[int, str] = "/dev/video0"
DEFAULT_RESOLUTION: Tuple[int, int] = (640, 480)


class CameraUnavailableError(RuntimeError):
    """Raised when the camera cannot be opened or used."""


def set_resolution(
    capture: cv2.VideoCapture,
    width: int,
    height: int,
) -> bool:
    """
    Apply a smaller resolution to keep bandwidth/CPU usage low on a Raspberry Pi.
    Returns True if both width and height were accepted by the driver.
    """
    if width <= 0 or height <= 0:
        return False

    ok_width = capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    ok_height = capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return bool(ok_width and ok_height)


def open_camera(
    device: Union[int, str, None] = DEFAULT_DEVICE,
    resolution: Optional[Tuple[int, int]] = DEFAULT_RESOLUTION,
    backend: int = cv2.CAP_ANY,
) -> cv2.VideoCapture:
    """
    Open the camera (webcam, USB, /dev/video*) and validate that frames can be read.
    Accepts int (0,1,...) or device path. Falls back through a small list of candidates.
    Raises CameraUnavailableError when no device works.
    """
    def _to_candidate(dev: Union[int, str]) -> Union[int, str]:
        # Convert numeric strings to ints so OpenCV indexes work.
        if isinstance(dev, str) and dev.isdigit():
            return int(dev)
        return dev

    candidates: Iterable[Union[int, str]] = []
    if device is not None:
        candidates = (_to_candidate(device),)
    else:
        candidates = ("/dev/video0", 0, 1)

    last_err: str | None = None
    for dev in candidates:
        capture = cv2.VideoCapture(dev, backend)
        if not capture.isOpened():
            capture.release()
            last_err = f"Camera {dev} is not available."
            continue
        if resolution:
            set_resolution(capture, *resolution)
        ok, _ = capture.read()
        if ok:
            return capture
        capture.release()
        last_err = f"Camera {dev} opened but did not return frames."

    raise CameraUnavailableError(last_err or "No camera available.")


__all__ = [
    "CameraUnavailableError",
    "DEFAULT_DEVICE",
    "DEFAULT_RESOLUTION",
    "open_camera",
    "set_resolution",
]
