"""Simple IoU tracker — teaching-friendly; upgrade to DeepSORT for production."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.detector import Detection


def _iou(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    return inter / (area_a + area_b - inter + 1e-6)


@dataclass
class Track:
    track_id: int
    xyxy: tuple[float, float, float, float]
    confidence: float
    age: int = 0
    hits: int = 0
    history: list[tuple[float, float]] = field(default_factory=list)

    @property
    def centroid(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.xyxy
        return ((x1 + x2) / 2, (y1 + y2) / 2)


class SimpleTracker:
    def __init__(self, iou_threshold: float = 0.3, max_age: int = 30) -> None:
        self.iou_threshold = iou_threshold
        self.max_age = max_age
        self._next_id = 1
        self._tracks: dict[int, Track] = {}

    def update(self, detections: list[Detection]) -> list[Track]:
        used: set[int] = set()
        for det in detections:
            best_id, best_iou = None, 0.0
            for tid, tr in self._tracks.items():
                if tid in used:
                    continue
                score = _iou(det.xyxy, tr.xyxy)
                if score > best_iou:
                    best_iou, best_id = score, tid
            if best_id is not None and best_iou >= self.iou_threshold:
                tr = self._tracks[best_id]
                tr.xyxy = det.xyxy
                tr.confidence = det.confidence
                tr.age = 0
                tr.hits += 1
                tr.history.append(tr.centroid)
                if len(tr.history) > 60:
                    tr.history.pop(0)
                used.add(best_id)
            else:
                tid = self._next_id
                self._next_id += 1
                self._tracks[tid] = Track(
                    track_id=tid,
                    xyxy=det.xyxy,
                    confidence=det.confidence,
                    hits=1,
                    history=[((det.xyxy[0] + det.xyxy[2]) / 2, (det.xyxy[1] + det.xyxy[3]) / 2)],
                )
                used.add(tid)

        dead = []
        for tid, tr in self._tracks.items():
            if tid not in used:
                tr.age += 1
            if tr.age > self.max_age:
                dead.append(tid)
        for tid in dead:
            del self._tracks[tid]

        return [t for t in self._tracks.values() if t.hits >= 1 and t.age == 0]
