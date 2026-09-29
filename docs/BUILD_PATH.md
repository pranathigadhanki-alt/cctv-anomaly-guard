# Step-by-step build path

Follow **one notebook per step**. Each step adds one layer; by notebook **05** you have a full **Option A** pipeline.

| Step | Notebook | You implement / run | Outcome |
|------|----------|---------------------|---------|
| 1 | `01_environment_and_stream` | OpenCV read loop, save frames | Video loads, FPS known |
| 2 | `02_yolo_detection` | YOLOv8 on each frame | Person boxes drawn |
| 3 | `03_tracking_zones` | Tracker + polygon zones | Track IDs, inside/outside zone |
| 4 | `04_anomaly_scoring` | Loiter / intrusion / speed rules | Alert scores per track |
| 5 | `05_alerts_and_export` | CSV log + annotated MP4 | Deliverable demo |
| 6 (opt) | `06_autoencoder_anomaly` | ConvLSTM on normal clips | Option B benchmark |

Code lives in **`src/`** — notebooks call it so Colab stays thin.

---

## Step 1 — Environment & stream

**Goal:** Prove you can read the source.

- Use `src/stream.py` → `FrameStream`  
- Print frame count, resolution, FPS  
- Write 1 annotated still to `outputs/`

**Why:** Everything else depends on a stable frame loop.

---

## Step 2 — Detection

**Goal:** Person bounding boxes.

- `src/detector.py` → `PersonDetector` (YOLOv8n, class person COCO id 0)  
- Draw boxes on one frame; then every Nth frame for speed in Colab

**Why:** Rules need positions; pixels alone are too noisy.

---

## Step 3 — Tracking & zones

**Goal:** Same person keeps an ID; know if they are in a forbidden polygon.

- `src/tracker.py` → match boxes frame-to-frame  
- `src/zones.py` → load JSON polygons, `point_in_zone(x, y)`  
- Color box red if inside **restricted** zone

**Why:** Loitering and intrusion are **over time** and **over space**.

---

## Step 4 — Anomaly scoring

**Goal:** Turn geometry into events.

| Rule | Idea |
|------|------|
| **Intrusion** | Track enters restricted zone |
| **Loitering** | Track stays in zone > `loiter_seconds` |
| **Chaotic movement** | Speed or direction change above threshold |

`src/anomaly.py` → `AnomalyEngine.update(track, frame_idx, fps)`

**Why:** This is your “ML + logic” product — detectors don’t know your site rules.

---

## Step 5 — Alerts & export

**Goal:** Something a security desk can use.

- `src/alerts.py` → append rows to `outputs/alert_log.csv`  
- `src/pipeline.py` → wire stream → detect → track → score → draw  
- Optional: `notify_webhook()` stub

**Why:** Annotated video + log = auditable system.

---

## Step 6 (optional) — Autoencoder

**Goal:** Unsupervised flag on benchmarks.

- Train on normal patches only; flag high loss  
- Compare to rule-based on same clip

**Why:** Shows second architecture from your project overview (Option B).

---

## Check progress

```bash
python scripts/check_setup.py
```

---

## GitHub / team workflow

- One branch per notebook step  
- Do **not** commit `data/raw`, API keys, or private CCTV  
- Cursor or other AI tools: use as helper; **you** remain author on commits
