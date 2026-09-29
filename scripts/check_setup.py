#!/usr/bin/env python3
"""Verify imports and optional sample video."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> None:
    ok = True
    try:
        import cv2  # noqa: F401
        print("OK  opencv")
    except ImportError:
        print("FAIL opencv — pip install -r requirements.txt")
        ok = False
    try:
        from ultralytics import YOLO  # noqa: F401
        print("OK  ultralytics")
    except ImportError:
        print("FAIL ultralytics")
        ok = False
    for mod in ("stream", "detector", "tracker", "zones", "anomaly", "pipeline"):
        try:
            __import__(f"src.{mod}")
            print(f"OK  src.{mod}")
        except Exception as e:
            print(f"FAIL src.{mod}: {e}")
            ok = False
    sample = ROOT / "data/samples/walking.mp4"
    if sample.exists():
        print(f"OK  sample video {sample}")
    else:
        print("WARN no sample video — run scripts/download_sample_data.py")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
