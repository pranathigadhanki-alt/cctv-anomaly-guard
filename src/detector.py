"""YOLOv8 person detection."""

from __future__ import annotations

from dataclasses import dataclass

from ultralytics import YOLO

PERSON_CLASS_ID = 0


@dataclass
class Detection:
    xyxy: tuple[float, float, float, float]
    confidence: float

    @property
    def centroid(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.xyxy
        return ((x1 + x2) / 2, (y1 + y2) / 2)


class PersonDetector:
    def __init__(self, model_name: str = "yolov8n.pt", conf: float = 0.4) -> None:
        self.model = YOLO(model_name)
        self.conf = conf

    def detect(self, frame) -> list[Detection]:
        results = self.model.predict(frame, conf=self.conf, verbose=False)
        out: list[Detection] = []
        if not results:
            return out
        boxes = results[0].boxes
        if boxes is None:
            return out
        for b in boxes:
            cls_id = int(b.cls.item())
            if cls_id != PERSON_CLASS_ID:
                continue
            x1, y1, x2, y2 = b.xyxy[0].tolist()
            out.append(Detection(xyxy=(x1, y1, x2, y2), confidence=float(b.conf.item())))
        return out
