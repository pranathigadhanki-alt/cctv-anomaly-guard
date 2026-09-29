"""End-to-end processing pipeline."""

from __future__ import annotations

from pathlib import Path

import cv2

from src.alerts import AlertLogger
from src.anomaly import AnomalyEngine
from src.detector import PersonDetector
from src.draw import draw_tracks, draw_zones
from src.stream import FrameStream
from src.tracker import SimpleTracker
from src.zones import load_zones


def run_pipeline(
    video_path: str | Path,
    zones_path: str | Path,
    output_video: str | Path,
    alert_csv: str | Path,
    max_frames: int | None = 300,
    detect_every: int = 1,
) -> int:
    zones = load_zones(zones_path)
    detector = PersonDetector()
    tracker = SimpleTracker()
    engine = AnomalyEngine(zones)
    logger = AlertLogger(alert_csv)
    alert_track_ids: set[int] = set()
    n_alerts = 0

    out_path = Path(output_video)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with FrameStream(video_path, max_frames=max_frames) as stream:
        meta = stream.meta
        writer = cv2.VideoWriter(
            str(out_path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            meta.fps,
            (meta.width, meta.height),
        )
        try:
            for frame_idx, frame in stream.frames():
                if frame_idx % detect_every == 0:
                    dets = detector.detect(frame)
                    tracks = tracker.update(dets)
                else:
                    tracks = tracker.update([])

                frame_events = []
                for tr in tracks:
                    frame_events.extend(engine.update(tr, frame_idx, meta.fps))
                for ev in frame_events:
                    logger.log(ev)
                    alert_track_ids.add(ev.track_id)
                    n_alerts += 1

                draw_zones(frame, zones)
                draw_tracks(frame, tracks, alert_track_ids)
                writer.write(frame)
        finally:
            writer.release()

    return n_alerts
