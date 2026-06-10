from __future__ import annotations

import sys

from config import (
    DATA_YAML,
    IMG_SIZE,
    RUNS_DIR,
    TRAIN_BATCH,
    TRAIN_EPOCHS,
    TRAIN_OPTIMIZER,
    TRAIN_PATIENCE,
)
from model_utils import load_model

def main() -> int:
    if not DATA_YAML.exists():
        print(f"[train] data.yaml introuvable : {DATA_YAML}")
        return 1

    model, name = load_model()
    print(f"[train] Entraînement basé sur {name}")

    model.train(
        data=str(DATA_YAML),
        epochs=TRAIN_EPOCHS,
        batch=TRAIN_BATCH,
        imgsz=IMG_SIZE,
        optimizer=TRAIN_OPTIMIZER,
        patience=TRAIN_PATIENCE,
        project=str(RUNS_DIR),
        name="traffic_signs",
        plots=True,
    )

    print("[train] Entraînement terminé. Poids dans runs/traffic_signs/weights/")
    return 0

if __name__ == "__main__":
    sys.exit(main())
