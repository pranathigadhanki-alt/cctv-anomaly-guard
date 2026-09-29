# CCTV Anomaly Guard

Detect **loitering**, **restricted-zone intrusion**, and **sudden chaotic movement** from RTSP or file video — without watching every frame yourself.

| | |
|--|--|
| **Run in Google Colab** | Start at [`notebooks/01_environment_and_stream.ipynb`](notebooks/01_environment_and_stream.ipynb) |
| **Step-by-step plan** | [`docs/BUILD_PATH.md`](docs/BUILD_PATH.md) |
| **Why each tool?** | [`docs/TOOLS_EXPLAINED.md`](docs/TOOLS_EXPLAINED.md) |
| **Get datasets / sample video** | [`docs/DATA_SETUP.md`](docs/DATA_SETUP.md) |

## What you build

1. **Ingest** — OpenCV reads RTSP or MP4 frame-by-frame.  
2. **Detect** — YOLOv8 finds people (and optional objects).  
3. **Track** — Simple tracker links boxes across frames.  
4. **Zones** — Polygons mark “restricted” or “watch” areas.  
5. **Score** — Rules flag loitering, intrusion, fast/erratic motion.  
6. **Alert** — Annotated frames, CSV log, optional webhook stub.

**Option B (advanced notebook):** ConvLSTM autoencoder on “normal only” clips — high reconstruction error = anomaly.

## Quick start (Colab)

Open the notebook link above, or:

```text
https://colab.research.google.com/github/pranathigadhanki-alt/cctv-anomaly-guard/blob/main/notebooks/01_environment_and_stream.ipynb
```

See [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md) if you fork under another username.

## Local (optional)

```bash
pip install -r requirements.txt
python scripts/download_sample_data.py
python -m src.cli --video data/samples/walking.mp4 --zones configs/zones.example.json
```

## Ethics & deployment

Use only on systems you are **authorized** to monitor. This repo is for **learning and benchmarking** on public datasets — not covert surveillance.

## License

MIT — see [LICENSE](LICENSE).
