"""Rule-based anomaly scoring."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from src.tracker import Track
from src.zones import Zone


@dataclass
class AlertEvent:
    frame_idx: int
    track_id: int
    rule: str
    message: str
    severity: str = "medium"


@dataclass
class AnomalyConfig:
    loiter_seconds: float = 8.0
    speed_threshold_px: float = 80.0  # per second at ~25fps scaled in engine
    restricted_only: bool = True


class AnomalyEngine:
    def __init__(self, zones: list[Zone], config: AnomalyConfig | None = None) -> None:
        self.zones = zones
        self.config = config or AnomalyConfig()
        self._zone_enter_frame: dict[tuple[int, str], int] = {}
        self._fired: set[tuple[int, str]] = set()

    def _restricted_zones(self) -> list[Zone]:
        return [z for z in self.zones if z.zone_type == "restricted"]

    def update(self, track: Track, frame_idx: int, fps: float) -> list[AlertEvent]:
        events: list[AlertEvent] = []
        cx, cy = track.centroid
        restricted = self._restricted_zones()

        inside_any = False
        for zone in restricted:
            key = (track.track_id, zone.name)
            inside = zone.contains(cx, cy)
            if inside:
                inside_any = True
                if key not in self._zone_enter_frame:
                    self._zone_enter_frame[key] = frame_idx
                    if ("intrusion", track.track_id, zone.name) not in self._fired:
                        self._fired.add(("intrusion", track.track_id, zone.name))
                        events.append(
                            AlertEvent(
                                frame_idx=frame_idx,
                                track_id=track.track_id,
                                rule="intrusion",
                                message=f"Track {track.track_id} entered restricted zone '{zone.name}'",
                                severity="high",
                            )
                        )
                dwell_frames = frame_idx - self._zone_enter_frame[key]
                dwell_sec = dwell_frames / max(fps, 1e-3)
                if dwell_sec >= self.config.loiter_seconds:
                    loiter_key = ("loiter", track.track_id, zone.name)
                    if loiter_key not in self._fired:
                        self._fired.add(loiter_key)
                        events.append(
                            AlertEvent(
                                frame_idx=frame_idx,
                                track_id=track.track_id,
                                rule="loitering",
                                message=f"Track {track.track_id} loitering in '{zone.name}' ({dwell_sec:.1f}s)",
                                severity="medium",
                            )
                        )
            else:
                if key in self._zone_enter_frame:
                    del self._zone_enter_frame[key]

        if len(track.history) >= 3:
            x0, y0 = track.history[-3]
            x1, y1 = track.history[-1]
            dist = math.hypot(x1 - x0, y1 - y0)
            dt = 2 / max(fps, 1e-3)
            speed = dist / dt
            if speed >= self.config.speed_threshold_px:
                sk = ("speed", track.track_id, frame_idx // int(fps))
                if sk not in self._fired:
                    self._fired.add(sk)
                    events.append(
                        AlertEvent(
                            frame_idx=frame_idx,
                            track_id=track.track_id,
                            rule="chaotic_movement",
                            message=f"Track {track.track_id} high motion (speed≈{speed:.0f}px/s)",
                            severity="low",
                        )
                    )

        return events
