#!/usr/bin/env python3
"""Generate beginner-friendly Colab notebooks (what / why / run / expect)."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"

REPO = "https://github.com/pranathigadhanki-alt/-Users-pranathigadhanki-Projects-cctv-anomaly-guard.git"
VIDEO = "data/processed/clean_clip.mp4"

SETUP_MD = f"""## Setup cell — run this first every session

**Why:** Colab starts empty. This downloads the project, installs libraries, and makes sure your video file exists.

**You should see:** Lines ending with `All set` or `OK` from the check script."""

REPO_DIR = "-Users-pranathigadhanki-Projects-cctv-anomaly-guard"
SETUP_CODE = f"""import os
REPO_DIR = "{REPO_DIR}"
if not os.path.isdir(REPO_DIR):
    !git clone {REPO}
os.chdir(REPO_DIR)
!pip install -q -r requirements.txt
!python scripts/prepare_data.py"""

NOTEBOOKS_SPEC = [
    (
        "00_setup_data",
        "Step 0 — Download & clean your video",
        [
            (
                "md",
                """# Step 0 — Download & clean data

**Goal:** Have one small video file ready for the whole course.

**ML idea:** Models and OpenCV need **files on disk** in a predictable format. “Cleaning” here means: *trim*, *resize*, *skip bad frames* — not labeling by hand.""",
            ),
            ("md", SETUP_MD),
            ("code", SETUP_CODE),
            (
                "md",
                """## Check the manifest

**Why:** Proves how many frames and seconds you will process.""",
            ),
            (
                "code",
                """import json
from pathlib import Path
m = json.loads(Path('data/manifest.json').read_text())
m""",
            ),
            (
                "md",
                """## Set the path for later notebooks

**Why:** One variable — less copy-paste mistakes.""",
            ),
            (
                "code",
                f'VIDEO_PATH = "{VIDEO}"\nprint("Use this path in steps 1–5:", VIDEO_PATH)',
            ),
            (
                "md",
                "**Next notebook:** `01_environment_and_stream.ipynb` — open it from the repo `notebooks/` folder or Colab file browser.",
            ),
        ],
    ),
    (
        "01_environment_and_stream",
        "Step 1 — Read video frames (OpenCV)",
        [
            (
                "md",
                """# Step 1 — Video = many images

**Why OpenCV?** Cameras and MP4 files deliver **frames**. OpenCV opens the file and gives us one picture at a time in a loop.

**You are not training anything yet** — just proving the video opens.""",
            ),
            ("md", SETUP_MD),
            ("code", SETUP_CODE),
            (
                "md",
                """## Read 5 frames

**Run the cell below.**

**You should see:** FPS (frames per second), width × height, and `frame 0 … frame 4` with shape `(height, width, 3)` — the 3 is Red-Green-Blue colors.""",
            ),
            (
                "code",
                f"""from pathlib import Path
from src.stream import FrameStream

VIDEO_PATH = Path("{VIDEO}")
with FrameStream(VIDEO_PATH, max_frames=5) as stream:
    meta = stream.meta
    print("FPS:", meta.fps)
    print("Size:", meta.width, "x", meta.height)
    for i, frame in stream.frames():
        print("frame", i, "shape", frame.shape)""",
            ),
            (
                "md",
                "**Next:** Step 2 — YOLO finds *people* in each frame.",
            ),
        ],
    ),
    (
        "02_yolo_detection",
        "Step 2 — Find people (YOLOv8)",
        [
            (
                "md",
                """# Step 2 — Object detection

**What is YOLO?** A neural network already trained on millions of images. It draws **boxes** around objects (we only keep **person**).

**Why we use it:** Counting “bright pixels” fails. A detector knows **person vs background**.

**Inference only:** We download weights (`yolov8n.pt`); we do **not** train from scratch in this course.""",
            ),
            ("md", SETUP_MD),
            ("code", SETUP_CODE + "\n# Optional: Runtime → Change runtime type → GPU (faster)"),
            (
                "md",
                """## Detect on one frame

**You should see:** A number `detections` (may be 0 on a cartoon clip — that's OK) and an image with green boxes if people exist.""",
            ),
            (
                "code",
                """import cv2
from pathlib import Path
from src.detector import PersonDetector
from src.stream import FrameStream

VIDEO_PATH = Path('"""
                + VIDEO
                + """')
det = PersonDetector()
with FrameStream(VIDEO_PATH, max_frames=1) as s:
    _, frame = next(s.frames())
    boxes = det.detect(frame)
    print('Number of people detected:', len(boxes))
    for b in boxes:
        x1,y1,x2,y2 = map(int, b.xyxy)
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
from google.colab.patches import cv2_imshow
cv2_imshow(frame)""",
            ),
        ],
    ),
    (
        "03_tracking_zones",
        "Step 3 — Track IDs & restricted zones",
        [
            (
                "md",
                """# Step 3 — Tracking + zones

**Tracking (simple English):** Match boxes frame-to-frame so **Person 3** stays **Person 3**.

**Zones:** A **polygon** on the ground plan — if a person's center enters a **restricted** zone, that's a candidate **intrusion**.

**Why Shapely?** Reliable math for "point inside polygon".""",
            ),
            ("md", SETUP_MD),
            ("code", SETUP_CODE),
            (
                "md",
                """## Run 30 frames

**You should see:** Printed track IDs changing over time; zone names from the JSON file.""",
            ),
            (
                "code",
                f"""from pathlib import Path
from src.zones import load_zones
from src.tracker import SimpleTracker
from src.detector import PersonDetector
from src.stream import FrameStream

zones = load_zones('configs/zones.example.json')
print('Zones loaded:', [z.name for z in zones])

tracker = SimpleTracker()
det = PersonDetector()
VIDEO_PATH = Path('{VIDEO}')

with FrameStream(VIDEO_PATH, max_frames=30) as s:
    for idx, frame in s.frames():
        tracks = tracker.update(det.detect(frame))
        if idx % 10 == 0:
            print('frame', idx, 'active IDs', [t.track_id for t in tracks])""",
            ),
        ],
    ),
    (
        "04_anomaly_scoring",
        "Step 4 — Turn rules into alerts",
        [
            (
                "md",
                """# Step 4 — Anomaly scoring (rules)

This is where **your security logic** lives:

| Rule | Plain English |
|------|----------------|
| **Intrusion** | Entered a restricted zone |
| **Loitering** | Stayed too long in that zone |
| **Chaotic movement** | Moved unusually fast |

**ML note:** YOLO gives location; **rules** decide if it's an incident.""",
            ),
            ("md", SETUP_MD),
            ("code", SETUP_CODE),
            (
                "md",
                """## Run short pipeline

**Why `max_frames=120`?** Keeps Colab fast for class.

**You should see:** A number `alert events logged` (0 is possible if no person hits a zone — try editing `configs/zones.example.json`).""",
            ),
            (
                "code",
                f"""from src.pipeline import run_pipeline

n = run_pipeline(
    '{VIDEO}',
    'configs/zones.example.json',
    'outputs/annotated.mp4',
    'outputs/alert_log.csv',
    max_frames=120,
    detect_every=2,
)
print('Alert events logged:', n)""",
            ),
        ],
    ),
    (
        "05_alerts_and_export",
        "Step 5 — CSV log & annotated video",
        [
            (
                "md",
                """# Step 5 — Outputs a human can use

**CSV log:** Spreadsheet of *when*, *which track*, *which rule*.

**Annotated MP4:** Video with boxes and zones drawn — good for demos and debugging.""",
            ),
            ("md", SETUP_MD),
            ("code", SETUP_CODE),
            (
                "md",
                """## Full demo run + preview

**You should see:** Table of alerts (maybe empty) and a playable video in the notebook.""",
            ),
            (
                "code",
                f"""import pandas as pd
from src.pipeline import run_pipeline

run_pipeline(
    '{VIDEO}',
    'configs/zones.example.json',
    'outputs/annotated.mp4',
    'outputs/alert_log.csv',
    max_frames=200,
    detect_every=2,
)
display(pd.read_csv('outputs/alert_log.csv'))
from IPython.display import Video
Video('outputs/annotated.mp4', embed=True, width=640)""",
            ),
        ],
    ),
    (
        "06_autoencoder_anomaly",
        "Step 6 (optional) — Unsupervised anomalies",
        [
            (
                "md",
                """# Step 6 (optional) — Autoencoder path

**For students who finished 0–5 early.**

**Idea:** Train on **normal** video only. When reconstruction error spikes → possible anomaly.

**Data:** UCSD / ShanghaiTech / UCF-Crime — see `docs/DATA_FOR_BEGINNERS.md` Path C.

This notebook is a **outline**; your mentor helps pick one benchmark clip.""",
            ),
            ("md", SETUP_MD),
            ("code", SETUP_CODE),
            (
                "code",
                """# Placeholder: load normal clips from Drive, train small conv autoencoder, plot error over time
print('Discuss with mentor: which benchmark clip and how many normal training frames.')""",
            ),
        ],
    ),
]


def to_cell(kind: str, text: str) -> dict:
    if kind == "md":
        return {"cell_type": "markdown", "metadata": {}, "source": [text + "\n"]}
    lines = text.split("\n")
    src = [ln + "\n" for ln in lines]
    return {"cell_type": "code", "metadata": {}, "source": src, "outputs": [], "execution_count": None}


def main() -> None:
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    for fname, title, parts in NOTEBOOKS_SPEC:
        cells = [to_cell("md", f"# {title}\n")]
        for kind, text in parts:
            cells.append(to_cell(kind, text))
        nb = {
            "nbformat": 4,
            "nbformat_minor": 5,
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "colab": {"provenance": [], "name": title[:60]},
            },
            "cells": cells,
        }
        path = NOTEBOOKS / f"{fname}.ipynb"
        path.write_text(json.dumps(nb, indent=1))
        print("Wrote", path)


if __name__ == "__main__":
    main()
