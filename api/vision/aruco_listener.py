from __future__ import annotations

import logging
import threading
import time
from typing import Any, Dict, Iterable, Tuple

import cv2
import numpy as np
from sqlalchemy.orm import Session

from services import scenario_run as scenario_run_service
from vision.camera_config import DEFAULT_DEVICE, open_camera

logger = logging.getLogger(__name__)

# Simple cooldown to avoid spamming the scenario engine with the same event.
_last_trigger: Dict[Tuple[int, int], float] = {}
COOLDOWN_SECONDS = 1.0


def _state_get(state: Any, key: str, default: Any = None) -> Any:
    return getattr(state, key, default) if not isinstance(state, dict) else state.get(key, default)


def _state_set(state: Any, key: str, value: Any) -> None:
    if isinstance(state, dict):
        state[key] = value
    else:
        setattr(state, key, value)


def _marker_center(corners: np.ndarray) -> Tuple[float, float]:
    pts = corners.reshape((4, 2))
    return float(np.mean(pts[:, 0])), float(np.mean(pts[:, 1]))


def _marker_tilt_angle_deg(corners: np.ndarray) -> float:
    """
    Heuristic tilt: angle of the vector between the first two corners.
    For ArUco ordering, this roughly captures rotation around the Z axis.
    """
    pts = corners.reshape((4, 2))
    vec = pts[1] - pts[0]
    return float(np.degrees(np.arctan2(vec[1], vec[0])))


def _is_tilted(angle_deg: float, threshold: float = 25.0) -> bool:
    # Acceptable tilt if rotated away from flat/horizontal by more than threshold.
    return abs(angle_deg) > threshold


def _find_target_below(
    source_center: Tuple[float, float],
    candidates: Iterable[Tuple[int, Tuple[float, float]]],
    max_dx: float = 120.0,
    max_dy: float = 300.0,
) -> int | None:
    sx, sy = source_center
    best_target = None
    best_dy = max_dy
    for marker_id, (tx, ty) in candidates:
        dx = abs(tx - sx)
        dy = ty - sy
        if dy <= 15 or dy > max_dy or dx > max_dx:
            continue
        if dy < best_dy:
            best_dy = dy
            best_target = marker_id
    return best_target


def _should_trigger(pair: Tuple[int, int]) -> bool:
    now = time.monotonic()
    last = _last_trigger.get(pair)
    if last is None or now - last >= COOLDOWN_SECONDS:
        _last_trigger[pair] = now
        return True
    return False


def start_aruco_listener(app_state: dict, device: Any = DEFAULT_DEVICE) -> None:
    """
    Starts a background thread that reads frames, detects ArUco markers, and sends
    simple "tilt over container" events to the scenario engine.
    """

    def _worker() -> None:
        cam_source = _state_get(app_state, "camera_device", device)
        try:
            capture = open_camera(device=cam_source)
        except Exception as exc:  # noqa: BLE001
            logger.error("Não foi possível abrir a câmera %s: %s", cam_source, exc)
            return

        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        aruco_params = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

        while True:
            ok, frame = capture.read()
            if not ok:
                logger.warning("Frame inválido da câmera; parando listener ArUco.")
                break
            _state_set(app_state, "latest_frame", frame)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners_list, ids, _ = detector.detectMarkers(gray)
            if ids is None or len(corners_list) == 0:
                continue

            markers = {}
            tilts = {}
            for idx, corners in zip(ids.flatten(), corners_list):
                markers[int(idx)] = _marker_center(corners)
                tilts[int(idx)] = _marker_tilt_angle_deg(corners)

            tilted_sources = [
                marker_id for marker_id, angle in tilts.items() if _is_tilted(angle)
            ]
            if not tilted_sources:
                continue

            # Simplified "pouring" heuristic: a tilted marker is source; target is the closest marker below it.
            for source_id in tilted_sources:
                source_center = markers[source_id]
                target_id = _find_target_below(
                    source_center,
                    ((mid, ctr) for mid, ctr in markers.items() if mid != source_id),
                )
                if target_id is None:
                    continue
                pair = (source_id, target_id)
                if not _should_trigger(pair):
                    continue

                _state_set(app_state, "latest_frame", frame)

                run_id = _state_get(app_state, "current_run_id")
                session_factory = _state_get(app_state, "db_session_factory")
                if not run_id or not session_factory:
                    logger.debug("Sem run ativo ou Session factory; evento ignorado.")
                    continue

                try:
                    with session_factory() as db:  # type: ignore[call-arg]
                        scenario_run_service.apply_action_from_vision(
                            db=db,
                            run_id=run_id,
                            source_marker_id=source_id,
                            target_marker_id=target_id,
                            trigger_type="tilt_over_container",
                        )
                except Exception as exc:  # noqa: BLE001
                    logger.info(
                        "Evento ArUco ignorado para par (%s -> %s): %s", source_id, target_id, exc
                    )
                    continue

        capture.release()

    thread = threading.Thread(
        target=_worker, name=f"aruco-listener-{str(device)}", daemon=True
    )
    thread.start()


__all__ = ["start_aruco_listener"]
