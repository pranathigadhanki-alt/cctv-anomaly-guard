# Project overview

## Core objective

Detect and flag **abnormal activities** — loitering, intrusion into restricted zones, sudden chaotic movement — **without** a human watching every frame.

| | |
|--|--|
| **Input** | Live **RTSP** or pre-recorded **CCTV / MP4** |
| **Output** | Annotated video, **alert_log.csv**, optional webhook |

## Architecture (Option A — recommended)

```text
Video (OpenCV) → YOLOv8 persons → Tracker (IDs) → Zone rules → Alerts + MP4
```

## Architecture (Option B — advanced)

```text
Video clips → ConvLSTM autoencoder (train on normal only) → high reconstruction error = anomaly
```

Use Option A for workshops; Option B for benchmark writeups (UCSD, ShanghaiTech, UCF-Crime).

## Implementation map

See **[BUILD_PATH.md](BUILD_PATH.md)** — six Colab notebooks, code in **`src/`**.

## Ethics

Monitor only systems you are **allowed** to record. Inform people where required by law/policy.
