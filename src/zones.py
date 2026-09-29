"""Polygon zones from JSON config."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from shapely.geometry import Point, Polygon


@dataclass
class Zone:
    name: str
    polygon: Polygon
    zone_type: str  # restricted | watch

    def contains(self, x: float, y: float) -> bool:
        return self.polygon.contains(Point(x, y))


def load_zones(path: str | Path) -> list[Zone]:
    data = json.loads(Path(path).read_text())
    zones: list[Zone] = []
    for z in data.get("zones", []):
        pts = z["points"]
        poly = Polygon(pts)
        zones.append(Zone(name=z["name"], polygon=poly, zone_type=z.get("type", "restricted")))
    return zones
