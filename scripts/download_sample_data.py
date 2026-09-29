#!/usr/bin/env python3
"""Download a small sample MP4 for tutorials (public test video)."""

from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "samples" / "walking.mp4"

# Short clip — Big Buck Bunny excerpt mirror commonly used for OpenCV demos (replace if link breaks)
URL = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists() and OUT.stat().st_size > 10_000:
        print(f"Already have {OUT} ({OUT.stat().st_size} bytes)")
        return
    print(f"Downloading sample to {OUT} ...")
    urllib.request.urlretrieve(URL, OUT)  # noqa: S310
    print("Done. Use VIDEO_PATH =", OUT)


if __name__ == "__main__":
    main()
