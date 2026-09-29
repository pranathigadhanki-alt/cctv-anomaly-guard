#!/usr/bin/env python3
"""
Make a video safe and fast for learning: check it opens, optionally trim and resize.

Why: Phone/CCTV files can be huge or odd-sized. Smaller clips run faster in Colab.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2


def clean_video(
    input_path: Path,
    output_path: Path,
    max_seconds: float | None = 60.0,
    max_width: int = 1280,
) -> dict:
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {input_path}")

    fps = float(cap.get(cv2.CAP_PROP_FPS) or 25.0)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    max_frames = int(max_seconds * fps) if max_seconds else None

    if w > max_width:
        scale = max_width / w
        out_w, out_h = max_width, int(h * scale)
    else:
        out_w, out_h = w, h

    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (out_w, out_h),
    )

    kept = 0
    bad_reads = 0
    while True:
        if max_frames is not None and kept >= max_frames:
            break
        ok, frame = cap.read()
        if not ok:
            break
        if frame is None or frame.size == 0:
            bad_reads += 1
            continue
        if (out_w, out_h) != (w, h):
            frame = cv2.resize(frame, (out_w, out_h))
        writer.write(frame)
        kept += 1

    cap.release()
    writer.release()

    return {
        "input": str(input_path),
        "output": str(output_path),
        "frames_kept": kept,
        "bad_reads": bad_reads,
        "fps": fps,
        "width": out_w,
        "height": out_h,
        "seconds_approx": round(kept / max(fps, 1e-3), 2),
    }


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser(description="Clean/trim/resize video for the tutorial pipeline")
    p.add_argument("--in", dest="inp", type=Path, default=root / "data/samples/walking.mp4")
    p.add_argument("--out", type=Path, default=root / "data/processed/clean_clip.mp4")
    p.add_argument("--max-seconds", type=float, default=45.0)
    p.add_argument("--max-width", type=int, default=960)
    args = p.parse_args()

    stats = clean_video(args.inp, args.out, max_seconds=args.max_seconds, max_width=args.max_width)
    manifest = root / "data/manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({"video_for_project": stats}, indent=2))
    print("Clean video saved:", stats["output"])
    print("Frames:", stats["frames_kept"], "| ~seconds:", stats["seconds_approx"])
    print("Manifest:", manifest)


if __name__ == "__main__":
    main()
