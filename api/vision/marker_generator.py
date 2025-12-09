from __future__ import annotations

from pathlib import Path
from typing import Literal

import cv2
import numpy as np

# Where marker images will be stored (served via /assets)
BASE_DIR = Path(__file__).resolve().parent.parent
MARKER_DIR = BASE_DIR / "assets" / "aruco_markers"


def generate_aruco_marker(
    marker_id: int,
    size_px: int = 600,
    dictionary: Literal[
        "DICT_4X4_50",
        "DICT_4X4_100",
        "DICT_5X5_50",
        "DICT_5X5_100",
    ] = "DICT_4X4_50",
) -> str:
    """
    Generates a PNG image of the ArUco marker and returns the relative path in assets.
    """
    if marker_id < 0:
        raise ValueError("marker_id precisa ser não-negativo.")

    MARKER_DIR.mkdir(parents=True, exist_ok=True)

    dict_attr = getattr(cv2.aruco, dictionary)
    aruco_dict = cv2.aruco.getPredefinedDictionary(dict_attr)

    marker_img = np.zeros((size_px, size_px), dtype=np.uint8)
    cv2.aruco.generateImageMarker(aruco_dict, marker_id, size_px, marker_img, borderBits=1)

    filename = f"marker_{marker_id}.png"
    abs_path = MARKER_DIR / filename
    cv2.imwrite(str(abs_path), marker_img)

    # Return path relative to /assets for easy serving
    return f"aruco_markers/{filename}"


__all__ = ["generate_aruco_marker"]
