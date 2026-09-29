"""Command-line entry: python -m src.cli"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.pipeline import run_pipeline

REPO = Path(__file__).resolve().parents[1]


def main() -> None:
    p = argparse.ArgumentParser(description="CCTV Anomaly Guard — YOLO + zones + alerts")
    p.add_argument("--video", type=Path, default=REPO / "data/samples/walking.mp4")
    p.add_argument("--zones", type=Path, default=REPO / "configs/zones.example.json")
    p.add_argument("--out", type=Path, default=REPO / "outputs/annotated.mp4")
    p.add_argument("--alerts", type=Path, default=REPO / "outputs/alert_log.csv")
    p.add_argument("--max-frames", type=int, default=300)
    p.add_argument("--detect-every", type=int, default=2, help="Run YOLO every N frames (speed)")
    args = p.parse_args()

    n = run_pipeline(
        args.video,
        args.zones,
        args.out,
        args.alerts,
        max_frames=args.max_frames,
        detect_every=args.detect_every,
    )
    print(f"Done. Alerts: {n}. Video: {args.out}. Log: {args.alerts}")


if __name__ == "__main__":
    main()
