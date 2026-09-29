# Google Colab setup

## Open Session 1 in one click

After the repo is on GitHub, share:

```text
https://colab.research.google.com/github/<your-username>/cctv-anomaly-guard/blob/main/notebooks/01_environment_and_stream.ipynb
```

Students: **File → Save a copy in Drive**.

## Standard first cells (every notebook)

```python
# GPU optional for YOLO (Runtime → Change runtime type → T4)
!git clone https://github.com/<your-username>/cctv-anomaly-guard.git
%cd cctv-anomaly-guard
!pip install -q -r requirements.txt
!python scripts/download_sample_data.py
```

Re-run safe clone:

```python
import os
REPO = "cctv-anomaly-guard"
if not os.path.isdir(REPO):
    !git clone https://github.com/<your-username>/cctv-anomaly-guard.git
%cd cctv-anomaly-guard
```

## Paths on Colab

| Path | Meaning |
|------|---------|
| `/content/cctv-anomaly-guard/` | Repo root |
| `data/samples/` | Short test video |
| `configs/zones.example.json` | Zone polygons |
| `outputs/` | Annotated video + CSV (create if missing) |

## Drive for large datasets

```python
from google.colab import drive
drive.mount("/content/drive")
VIDEO_PATH = "/content/drive/MyDrive/CCTV-Data/my_clip.mp4"
```

## Secrets (webhooks / SMTP)

```python
import os
WEBHOOK_URL = os.environ.get("ALERT_WEBHOOK_URL")  # set in Colab secrets, not in git
```

See `src/alerts.py` — never paste tokens into notebooks you commit.
