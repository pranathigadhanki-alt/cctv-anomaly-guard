# Mentor teaching guide (ML beginners)

## Session flow (~2 hours)

| Time | You do |
|------|--------|
| 0:00 | Read [START_HERE.md](START_HERE.md) glossary out loud (5 min) |
| 0:05 | Everyone opens `00_setup_data.ipynb`, Run All |
| 0:25 | Notebook 01 — explain “video = loop of frames” |
| 0:45 | Notebook 02 — “YOLO is pretrained; we’re not training yet” |
| 1:05 | Break |
| 1:15 | Notebook 03 — draw a zone polygon on whiteboard |
| 1:35 | Notebooks 04–05 — run pipeline, open `alert_log.csv` |
| 1:55 | Ethics + “what would you add next?” |

## Phrases that help beginners

- **“We’re doing inference, not training”** for YOLO in week 1.  
- **“The model finds people; our code decides if that’s a problem.”**  
- **“Track ID = same person over time.”**

## Common scares

| Student fear | Answer |
|--------------|--------|
| “I don’t know calculus” | You’re calling libraries and reading outputs. |
| “Is this illegal?” | Only use authorized video; we’re learning on public sample. |
| “Nothing alerted” | Zones default to a box — resize JSON or use shorter clip with visible motion. |

## Homework policy

Suggest **optional**: re-run 05 with their own 20s MP4. Core path stays in-class.

## Check they finished

```bash
python scripts/prepare_data.py
python scripts/check_setup.py
ls outputs/alert_log.csv
```
