from __future__ import annotations

import sys
from pathlib import Path

import cv2

from config import CONF_THRESHOLD, IMG_SIZE, IOU_THRESHOLD, OUTPUTS_DIR
from model_utils import load_model

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python src/predict_image.py <image> [poids.pt]")
        return 1

    image_path = Path(sys.argv[1])
    weights = sys.argv[2] if len(sys.argv) > 2 else None

    if not image_path.exists():
        print(f"[predict] Image introuvable : {image_path}")
        return 1

    model, name = load_model(preferred=weights)
    print(f"[predict] Détection avec {name} sur {image_path.name}")

    results = model.predict(
        source=str(image_path),
        conf=CONF_THRESHOLD,
        iou=IOU_THRESHOLD,
        imgsz=IMG_SIZE,
        verbose=False,
    )

    annotated = results[0].plot()
    out_path = OUTPUTS_DIR / f"pred_{image_path.stem}.jpg"
    cv2.imwrite(str(out_path), annotated)

    n = len(results[0].boxes)
    print(f"[predict] {n} objet(s) détecté(s). Résultat : {out_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
