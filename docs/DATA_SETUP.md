# Data — sample video and benchmark datasets

## For the tutorials (start here)

### A. Bundled download script (easiest)

In Colab or locally, after cloning the repo:

```bash
python scripts/download_sample_data.py
```

This fetches a **short public sample MP4** into `data/samples/` (small file, safe to commit a placeholder; video is gitignored).

### B. Your own CCTV / phone video

1. Export 10–60 seconds as **MP4** (H.264).  
2. Upload to Colab: `files.upload()` or Drive → copy path.  
3. Pass path to `--video` or the notebook `VIDEO_PATH` variable.

**Do not** commit private footage to GitHub.

### C. RTSP stream (later step)

```python
VIDEO_PATH = "rtsp://user:pass@192.168.1.100:554/stream1"
```

Use only on networks you own. Colab often **cannot** reach your home RTSP; test locally with `python -m src.cli`.

---

## Benchmark datasets (for reports & Option B)

Use these to **cite numbers** in a writeup — not required for the basic YOLO + zones pipeline.

| Dataset | Use case | Get it |
|---------|----------|--------|
| **UCSD Pedestrian** | Classic abnormal pedestrian clips | [UCSD Anomaly Detection](http://www.svcl.ucsd.edu/projects/anomaly/dataset.htm) — request / academic mirrors; see links on their page |
| **ShanghaiTech Campus** | Campus CCTV anomalies | Search “ShanghaiTech Campus dataset anomaly detection”; often via university hosting or Kaggle mirrors |
| **UCF-Crime** | Long surveillance anomalies | [CRCV UCF-Crime](https://www.crcv.ucf.edu/projects/real-world/) — fill form; clips labeled by crime type |

### Practical Colab workflow for benchmarks

1. Download on your laptop or Drive (many are **multi-GB**).  
2. Mount Drive in Colab (`docs/COLAB_SETUP.md`).  
3. Point `VIDEO_PATH` or dataloader to ` /content/drive/MyDrive/CCTV-Data/... `  
4. Never commit raw benchmark zips to git.

### Train/test split idea (autoencoder notebook)

- **Train:** only “normal” clips from UCSD/Peds2 etc.  
- **Test:** mix normal + labeled anomaly segments → plot reconstruction error.

---

## Folder layout

```text
data/
  samples/          ← short MP4 for exercises (download script)
  raw/              ← your full downloads (gitignored)
  processed/        ← clips, manifests (gitignored)
outputs/
  annotated.mp4     ← run output
  alert_log.csv     ← timestamps + rule name
```
