# CCTV Anomaly Guard

Learn **video anomaly detection** step-by-step in **Google Colab** — written for people **new to ML**.

| Start here | Link |
|------------|------|
| **Students** | [docs/START_HERE.md](docs/START_HERE.md) |
| **Download & clean data** | [docs/DATA_FOR_BEGINNERS.md](docs/DATA_FOR_BEGINNERS.md) |
| **Mentors** | [docs/TEACHING_GUIDE.md](docs/TEACHING_GUIDE.md) |
| **Why each tool?** | [docs/TOOLS_EXPLAINED.md](docs/TOOLS_EXPLAINED.md) |

## Colab — notebook 0 (run this first)

```text
https://colab.research.google.com/github/pranathigadhanki-alt/cctv-anomaly-guard/blob/main/notebooks/00_setup_data.ipynb
```

Then do **01 → 05** in order. All code is ready in **`src/`**; notebooks explain **what** to run and **why** in plain English.

## One-command data prep (local or Colab)

```bash
python scripts/prepare_data.py
```

Uses: download sample → clean/trim → `data/processed/clean_clip.mp4` → `data/manifest.json`.

## What you build

1. Open video (OpenCV)  
2. Detect people (YOLOv8, pretrained)  
3. Track IDs + restricted zones  
4. Score intrusions / loitering / fast motion  
5. Export **alert_log.csv** + annotated MP4  

## Ethics

Use only video you are **authorized** to process. Not a replacement for professional security or legal advice.

## License

MIT — [LICENSE](LICENSE)
