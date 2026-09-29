# Every tool — what it is and why you need it

## Python

**What:** The language all notebooks and `src/` use.  
**Why:** Largest ecosystem for computer vision, Colab support, and hiring/teaching familiarity.

## Google Colab

**What:** Free cloud Jupyter notebooks with optional GPU.  
**Why:** No local CUDA setup; everyone opens the same link; good for workshops. You clone this repo in the first cell and run step-by-step.

## OpenCV (`cv2`)

**What:** Library to read video, resize frames, draw boxes/text, write output MP4.  
**Why:** RTSP and CCTV are **streams of images**. OpenCV is the standard way to `read()` frames in a loop. Without it you cannot connect to cameras or save annotated video.

## PyTorch

**What:** Deep learning framework (tensors, GPU, autograd).  
**Why:** YOLOv8 (Ultralytics) and optional ConvLSTM autoencoder run on PyTorch. Colab ships with it preinstalled.

## Ultralytics YOLOv8

**What:** Pretrained object detector — one call gives person bounding boxes per frame.  
**Why:** **Option A** anomaly pipeline needs “where are people?” before rules (zones, loitering, speed). Training from scratch is hard; YOLOv8n is small and fast for demos.

## NumPy / Pandas

**What:** Arrays and tables.  
**Why:** Box coordinates, speeds, and **alert logs** (CSV) are structured data. Pandas makes `alert_log.csv` easy to analyze.

## SciPy

**What:** Scientific utilities (distance, etc.).  
**Why:** Centroid distance between frames → **speed** for “chaotic movement” heuristics.

## Shapely

**What:** Geometry library (point-in-polygon).  
**Why:** **Restricted zones** are polygons. You must know if a person’s foot point is **inside** a zone — Shapely is clearer than hand-rolled math.

## Simple IoU tracker (in `src/tracker.py`)

**What:** Lightweight multi-object tracking without full DeepSORT.  
**Why:** **Loitering** = same track ID in a zone for N seconds. SORT/DeepSORT are ideal for production; IoU matching is **easier to teach** and runs everywhere. Notebook 03 explains upgrading to DeepSORT.

## YAML + JSON configs

**What:** Files describing zone polygons and thresholds.  
**Why:** Security staff should change zones **without editing Python**. `configs/zones.example.json` is the template.

## Matplotlib

**What:** Plotting.  
**Why:** EDA on datasets (UCSD, etc.) and reconstruction-error curves for the autoencoder notebook.

## Optional: SMTP / webhooks (`src/alerts.py`)

**What:** Send email or HTTP POST when an alert fires.  
**Why:** Automated monitoring means **notify someone**; stubs show where secrets go (never commit passwords).

## Optional: ConvLSTM autoencoder (notebook 06)

**What:** Neural net trained only on **normal** video; flags high reconstruction error.  
**Why:** **Option B** when you cannot define zones/rules — useful for research benchmarks (ShanghaiTech, UCF-Crime). Harder than YOLO + rules; kept as advanced path.

## What we deliberately skip for “easy”

| Tool | Why skipped at first |
|------|----------------------|
| Tkinter desktop UI | Colab + saved MP4 is enough; Tkinter is painful on Colab |
| Full DeepSORT | Extra deps + tuning; IoU tracker first |
| Kubernetes / RTSP server | Out of scope; OpenCV URL string is enough |
