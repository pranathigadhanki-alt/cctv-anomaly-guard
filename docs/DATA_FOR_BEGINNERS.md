# Data — download and clean (simple steps)

## Path A — Class demo (easiest, no Kaggle)

**What you do:** Run one script.  
**Why:** Everyone gets the same small video; no one uploads private CCTV on day 1.

### In Colab (after clone)

```python
!python scripts/prepare_data.py
```

### What this does (plain English)

1. **Download** a short public MP4 into `data/samples/walking.mp4`  
2. **Clean** it → `data/processed/clean_clip.mp4`  
   - Trims to ~45 seconds (faster runs)  
   - Shrinks width if too large (Colab speed)  
   - Skips broken frames if any  
3. **Writes** `data/manifest.json` — a small report of frame count and size  
4. **Checks** that OpenCV and YOLO libraries import correctly  

### What you use in every later notebook

```python
VIDEO_PATH = "data/processed/clean_clip.mp4"
```

---

## Path B — Your own phone / MP4

**Why:** Makes the demo feel real.

1. Export 15–60 seconds as **MP4**.  
2. In Colab:

```python
from google.colab import files
uploaded = files.upload()  # pick your .mp4
```

3. Move and clean:

```python
!mkdir -p data/samples
!mv your_file.mp4 data/samples/my_clip.mp4
!python scripts/clean_video.py --in data/samples/my_clip.mp4 --out data/processed/clean_clip.mp4
```

4. Set `VIDEO_PATH = "data/processed/clean_clip.mp4"`.

**Do not** commit personal video to GitHub.

---

## Path C — Research datasets (later / optional)

For slides and Option B autoencoder — **not** required for notebooks 01–05.

| Dataset | What it is | How people get it |
|---------|------------|-------------------|
| UCSD Pedestrian | Classic “normal vs odd” pedestrian clips | University page — see [DATA_SETUP.md](DATA_SETUP.md) |
| ShanghaiTech | Campus CCTV anomalies | Academic mirrors / search dataset name |
| UCF-Crime | Long surveillance events | UCF site — often form + download |

**Cleaning for benchmarks:** unzip on Drive, pick **one short clip**, run the same `clean_video.py` on it so Colab does not choke on 4K hours of footage.

---

## “Cleaning” does NOT mean (for this project)

- We do **not** label every pixel by hand in week 1.  
- We do **not** require you to **train** YOLO from scratch.  
- We **do** trim, resize, and verify the file plays — that **is** your data prep.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Cannot open video` | Wrong path; run `!ls data/processed` |
| Download URL dead | See `scripts/download_sample_data.py` URL or upload your own MP4 |
| YOLO slow | Runtime → GPU; or raise `detect_every=3` in pipeline |
| No alerts | Zones JSON is in wrong place — edit `configs/zones.example.json` to match video size |
