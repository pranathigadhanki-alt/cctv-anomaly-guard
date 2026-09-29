# Start here (new to ML)

You do **not** need ML experience. You **do** need Google Colab and a GitHub account (optional for reading only).

## Big picture in one paragraph

A camera gives **many pictures per second** (video). We use a **pretrained detector** (YOLO) to find **people**, give each person an **ID** across frames, check if they enter **forbidden zones**, and **log alerts**. That is “ML + simple rules” — not magic, not a movie hacker scene.

## Order of work (do not skip)

| Step | Notebook | Minutes | You learn |
|------|----------|---------|-----------|
| 0 | `00_setup_data.ipynb` | 15 | Install tools, download & **clean** video |
| 1 | `01_environment_and_stream.ipynb` | 20 | What a “frame” is |
| 2 | `02_yolo_detection.ipynb` | 30 | What object detection is |
| 3 | `03_tracking_zones.ipynb` | 30 | IDs + map zones |
| 4 | `04_anomaly_scoring.ipynb` | 25 | When to alert |
| 5 | `05_alerts_and_export.ipynb` | 25 | CSV + video output |

Optional: `06_autoencoder_anomaly.ipynb` (harder, for research datasets).

## Colab link

Open notebook **00** from GitHub:

```text
https://colab.research.google.com/github/pranathigadhanki-alt/-Users-pranathigadhanki-Projects-cctv-anomaly-guard/blob/main/notebooks/00_setup_data.ipynb
```

**File → Save a copy in Drive** before you edit.

## Words we use (mini glossary)

| Word | Simple meaning |
|------|----------------|
| **Frame** | One image from the video |
| **Model** | Program that learned patterns from lots of data (YOLO already trained) |
| **Detection** | “Person is in this box on this frame” |
| **Track** | Same person, same ID, many frames |
| **Feature** | A number we compute (speed, time in zone) — not always “deep learning” |
| **Anomaly** | Something our rules say is unusual (intrusion, loitering, fast motion) |
| **Inference** | Running the model on new video |

## Where the code lives

- **`src/`** — real project code (already written for you in this course repo).
- **Notebooks** — you **run** cells; they call `src/` and explain **why**.

## Ethics

Only use video you are **allowed** to use. Tell people where your school/org requires it.

Next read: **[DATA_FOR_BEGINNERS.md](DATA_FOR_BEGINNERS.md)** for download & cleaning details.
