#!/usr/bin/env python3
"""
Step 0 for beginners: download sample video, clean it, verify setup.

Run once at the start of the course:
  python scripts/prepare_data.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print(">>", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)


def main() -> None:
    print("=== Step A: Download sample MP4 ===")
    print("Why: You need a small video file to practice before using CCTV or benchmarks.\n")
    run([sys.executable, "scripts/download_sample_data.py"])

    raw = ROOT / "data/samples/walking.mp4"
    if not raw.exists():
        raise SystemExit("Download failed — check internet or docs/DATA_FOR_BEGINNERS.md")

    print("\n=== Step B: Clean / trim / resize ===")
    print("Why: Shorter, smaller videos train and demo faster in Colab.\n")
    run(
        [
            sys.executable,
            "scripts/clean_video.py",
            "--in",
            str(raw),
            "--out",
            str(ROOT / "data/processed/clean_clip.mp4"),
            "--max-seconds",
            "45",
            "--max-width",
            "960",
        ]
    )

    print("\n=== Step C: Check Python packages ===")
    run([sys.executable, "scripts/check_setup.py"])

    print("\nAll set. Use this path in every notebook:")
    print("  VIDEO_PATH = 'data/processed/clean_clip.mp4'")


if __name__ == "__main__":
    main()
