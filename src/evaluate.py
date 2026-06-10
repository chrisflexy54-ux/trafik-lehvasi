from __future__ import annotations

import sys

from config import DATA_YAML, IMG_SIZE
from model_utils import load_model

def main() -> int:
    weights = sys.argv[1] if len(sys.argv) > 1 else None
    if not DATA_YAML.exists():
        print(f"[eval] data.yaml introuvable : {DATA_YAML}")
        return 1

    model, name = load_model(preferred=weights)
    print(f"[eval] Évaluation du modèle : {name}")

    metrics = model.val(data=str(DATA_YAML), imgsz=IMG_SIZE)

    box = metrics.box
    print("\n===== Métriques de détection =====")
    print(f"mAP50      : {box.map50:.4f}")
    print(f"mAP50-95   : {box.map:.4f}")
    print(f"Précision  : {box.mp:.4f}")
    print(f"Rappel     : {box.mr:.4f}")
    print("==================================\n")
    print("Courbes (PR, F1, matrice de confusion) générées dans le dossier de run.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
