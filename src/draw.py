"""Draw boxes, zones, and labels."""

from __future__ import annotations

import cv2
import numpy as np

from src.tracker import Track
from src.zones import Zone


def draw_zones(frame, zones: list[Zone]) -> None:
    for z in zones:
        pts = [(int(x), int(y)) for x, y in z.polygon.exterior.coords]
        arr = np.array(pts, dtype=np.int32)
        color = (0, 0, 255) if z.zone_type == "restricted" else (0, 255, 255)
        cv2.polylines(frame, [arr], True, color, 2)
        cv2.putText(frame, z.name, pts[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)


def draw_tracks(frame, tracks: list[Track], alert_ids: set[int] | None = None) -> None:
    alert_ids = alert_ids or set()
    for t in tracks:
        x1, y1, x2, y2 = map(int, t.xyxy)
        color = (0, 0, 255) if t.track_id in alert_ids else (0, 255, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"ID {t.track_id}", (x1, max(0, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
