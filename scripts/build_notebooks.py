#!/usr/bin/env python3
"""Generate Colab notebooks from BUILD_PATH steps."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"

CLONE = """import os
REPO = 'cctv-anomaly-guard'
if not os.path.isdir(REPO):
    !git clone https://github.com/pranathigadhanki-alt/cctv-anomaly-guard.git
%cd cctv-anomaly-guard
!pip install -q -r requirements.txt
!python scripts/download_sample_data.py
!python scripts/check_setup.py"""

NOTEBOOKS_SPEC = [
    (
        "01_environment_and_stream",
        "Step 1 — Environment & video stream",
        [
            "## Goal\nConnect to MP4 (or RTSP) with OpenCV and inspect FPS/size.\n\nRead **docs/TOOLS_EXPLAINED.md** (OpenCV section).",
            CLONE,
            "from src.stream import FrameStream\nfrom pathlib import Path\nVIDEO = Path('data/samples/walking.mp4')\nwith FrameStream(VIDEO, max_frames=5) as s:\n    m = s.meta\n    print('FPS', m.fps, 'size', m.width, 'x', m.height)\n    for i, frame in s.frames():\n        print('frame', i, frame.shape)",
            "## Next\nNotebook **02** — run YOLO on these frames.",
        ],
    ),
    (
        "02_yolo_detection",
        "Step 2 — YOLOv8 person detection",
        [
            "## Goal\nDetect people with YOLOv8n. See **docs/TOOLS_EXPLAINED.md** (Ultralytics).\n\nRuntime → GPU optional.",
            CLONE,
            "import cv2\nfrom pathlib import Path\nfrom src.detector import PersonDetector\nfrom src.stream import FrameStream\nVIDEO = Path('data/samples/walking.mp4')\ndet = PersonDetector()\nwith FrameStream(VIDEO, max_frames=1) as s:\n    _, frame = next(s.frames())\n    boxes = det.detect(frame)\n    print('detections', len(boxes))\n    for b in boxes:\n        x1,y1,x2,y2 = map(int, b.xyxy)\n        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)\nfrom google.colab.patches import cv2_imshow\ncv2_imshow(frame)",
        ],
    ),
    (
        "03_tracking_zones",
        "Step 3 — Tracking & zones",
        [
            "## Goal\nTrack IDs + point-in-polygon for restricted areas (**Shapely** in TOOLS_EXPLAINED).",
            CLONE,
            "from src.zones import load_zones\nfrom src.tracker import SimpleTracker\nfrom src.detector import PersonDetector\nfrom src.stream import FrameStream\nfrom pathlib import Path\nzones = load_zones('configs/zones.example.json')\nprint([z.name for z in zones])\ntracker = SimpleTracker()\ndet = PersonDetector()\nVIDEO = Path('data/samples/walking.mp4')\nwith FrameStream(VIDEO, max_frames=30) as s:\n    for idx, frame in s.frames():\n        tracks = tracker.update(det.detect(frame))\n        if idx % 10 == 0:\n            print('frame', idx, 'tracks', [t.track_id for t in tracks])",
        ],
    ),
    (
        "04_anomaly_scoring",
        "Step 4 — Anomaly rules",
        [
            "## Goal\nIntrusion, loitering, fast motion — **src/anomaly.py**",
            CLONE,
            "from src.pipeline import run_pipeline\nfrom pathlib import Path\n# Short run; tune zones JSON to your video resolution\nn = run_pipeline('data/samples/walking.mp4', 'configs/zones.example.json', 'outputs/annotated.mp4', 'outputs/alert_log.csv', max_frames=120, detect_every=2)\nprint('alert events logged', n)",
        ],
    ),
    (
        "05_alerts_and_export",
        "Step 5 — Alerts & export",
        [
            "## Goal\nCSV log + annotated MP4. Optional webhook in **src/alerts.py**.",
            CLONE,
            "import pandas as pd\nfrom pathlib import Path\nfrom src.pipeline import run_pipeline\nrun_pipeline('data/samples/walking.mp4', 'configs/zones.example.json', 'outputs/annotated.mp4', 'outputs/alert_log.csv', max_frames=200)\ndisplay(pd.read_csv('outputs/alert_log.csv').head(10))\nfrom IPython.display import Video\nVideo('outputs/annotated.mp4', embed=True, width=640)",
        ],
    ),
    (
        "06_autoencoder_anomaly",
        "Step 6 (optional) — ConvLSTM autoencoder",
        [
            "## Goal\nOption B: train on **normal** clips only; flag high reconstruction error.\n\nDownload benchmarks via **docs/DATA_SETUP.md** (UCSD / ShanghaiTech / UCF-Crime).",
            CLONE,
            "# Skeleton — extract patches, train small conv autoencoder on normal frames\n# Compare reconstruction MSE distribution normal vs anomaly labeled segments\nprint('See docs/BUILD_PATH.md Step 6 — implement in this notebook for your benchmark clip paths')",
        ],
    ),
]


def cell(text: str, kind: str = "code") -> dict:
    if kind == "md":
        return {"cell_type": "markdown", "metadata": {}, "source": [text + "\n"]}
    lines = text.split("\n")
    src = [ln + "\n" for ln in lines]
    return {"cell_type": "code", "metadata": {}, "source": src, "outputs": [], "execution_count": None}


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    for fname, title, parts in NOTEBOOKS_SPEC:
        cells = [cell(f"# {title}\n", "md")]
        for part in parts:
            cells.append(cell(part, "md" if part.startswith("##") else "code"))
        nb = {
            "nbformat": 4,
            "nbformat_minor": 5,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "colab": {"provenance": []}},
            "cells": cells,
        }
        path = NOTEBOOKS / f"{fname}.ipynb"
        path.write_text(json.dumps(nb, indent=1))
        print("Wrote", path)


if __name__ == "__main__":
    main()
