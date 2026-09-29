"""OpenCV frame stream from file or RTSP."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import cv2


@dataclass
class VideoMeta:
    width: int
    height: int
    fps: float
    frame_count: int


class FrameStream:
    """Read frames one at a time; use as context manager."""

    def __init__(self, source: str | Path, max_frames: int | None = None) -> None:
        self.source = str(source)
        self.max_frames = max_frames
        self._cap: cv2.VideoCapture | None = None

    def __enter__(self) -> FrameStream:
        self._cap = cv2.VideoCapture(self.source)
        if not self._cap.isOpened():
            raise FileNotFoundError(f"Cannot open video source: {self.source}")
        return self

    def __exit__(self, *args: object) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    @property
    def meta(self) -> VideoMeta:
        assert self._cap is not None
        w = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(self._cap.get(cv2.CAP_PROP_FPS) or 25.0)
        count = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        return VideoMeta(width=w, height=h, fps=fps, frame_count=count)

    def frames(self) -> Iterator[tuple[int, object]]:
        assert self._cap is not None
        idx = 0
        while True:
            if self.max_frames is not None and idx >= self.max_frames:
                break
            ok, frame = self._cap.read()
            if not ok:
                break
            yield idx, frame
            idx += 1
