from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS_DIR = PROJECT_ROOT / "configs"
SAMPLES_DIR = PROJECT_ROOT / "samples"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
RUNS_DIR = PROJECT_ROOT / "runs"
WEIGHTS_DIR = PROJECT_ROOT / "weights"
DATA_YAML = CONFIGS_DIR / "data.yaml"

for _d in (SAMPLES_DIR, OUTPUTS_DIR, WEIGHTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

MODEL_CANDIDATES = [
    "yolo26n.pt",
    "yolo11n.pt",
    "yolov8n.pt",
]

CONF_THRESHOLD = 0.35
IOU_THRESHOLD = 0.50
IMG_SIZE = 640

SAHI_SLICE_HEIGHT = 512
SAHI_SLICE_WIDTH = 512
SAHI_OVERLAP_RATIO = 0.2

TRAIN_EPOCHS = 100
TRAIN_BATCH = 16
TRAIN_PATIENCE = 20
TRAIN_OPTIMIZER = "auto"

COCO_TRAFFIC_CLASSES = {
    9: "traffic light",
    11: "stop sign",
}

def resolve_model_name() -> str:

    return MODEL_CANDIDATES[0]
