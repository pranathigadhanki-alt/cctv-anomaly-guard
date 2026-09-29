"""Alert logging and optional notifications."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any
from urllib import request

from src.anomaly import AlertEvent


class AlertLogger:
    def __init__(self, csv_path: str | Path) -> None:
        self.path = Path(csv_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            with self.path.open("w", newline="") as f:
                csv.writer(f).writerow(["frame_idx", "track_id", "rule", "severity", "message"])

    def log(self, event: AlertEvent) -> None:
        with self.path.open("a", newline="") as f:
            csv.writer(f).writerow(
                [event.frame_idx, event.track_id, event.rule, event.severity, event.message]
            )


def notify_webhook(url: str, payload: dict[str, Any]) -> None:
    """Optional: POST JSON to Slack/Discord/custom endpoint. No-op if url empty."""
    if not url:
        return
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req, timeout=10):  # noqa: S310 — user-supplied URL
        pass
