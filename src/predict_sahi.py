from __future__ import annotations

import sys
from pathlib import Path

from config import (
    CONF_THRESHOLD,
    MODEL_CANDIDATES,
    OUTPUTS_DIR,
    SAHI_OVERLAP_RATIO,
    SAHI_SLICE_HEIGHT,
    SAHI_SLICE_WIDTH,
)

def _resolve_weights(weights: str | None) -> str:

    if weights:
        return weights

    return MODEL_CANDIDATES[0]

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python src/predict_sahi.py <image> [poids.pt]")
        return 1

    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(f"[sahi] Image introuvable : {image_path}")
        return 1

    try:
        from sahi import AutoDetectionModel
        from sahi.predict import get_sliced_prediction
    except ImportError:
        print("[sahi] Le paquet 'sahi' n'est pas installé : pip install sahi")
        return 1

    weights = _resolve_weights(sys.argv[2] if len(sys.argv) > 2 else None)
    print(f"[sahi] Modèle : {weights}")

    detection_model = AutoDetectionModel.from_pretrained(
        model_type="ultralytics",
        model_path=weights,
        confidence_threshold=CONF_THRESHOLD,
        device="cpu",
    )

    result = get_sliced_prediction(
        str(image_path),
        detection_model,
        slice_height=SAHI_SLICE_HEIGHT,
        slice_width=SAHI_SLICE_WIDTH,
        overlap_height_ratio=SAHI_OVERLAP_RATIO,
        overlap_width_ratio=SAHI_OVERLAP_RATIO,
    )

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    result.export_visuals(
        export_dir=str(OUTPUTS_DIR),
        file_name=f"sahi_{image_path.stem}",
    )

    n = len(result.object_prediction_list)
    print(f"[sahi] {n} objet(s) détecté(s) via slicing.")
    print(f"[sahi] Résultat : {OUTPUTS_DIR / ('sahi_' + image_path.stem + '.png')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
