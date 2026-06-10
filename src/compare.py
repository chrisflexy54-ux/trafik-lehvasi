from __future__ import annotations

import sys

import cv2
import numpy as np

from config import OUTPUTS_DIR

def _label_bar(width: int, text: str, color=(40, 40, 40)) -> np.ndarray:
    bar = np.full((46, width, 3), color, dtype=np.uint8)
    cv2.putText(
        bar, text, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2
    )
    return bar

def make_comparison(stem: str) -> int:
    classic = OUTPUTS_DIR / f"classic_{stem}.jpg"
    sahi = OUTPUTS_DIR / f"sahi_{stem}.png"

    if not classic.exists() or not sahi.exists():
        print(f"[compare] Sorties manquantes pour '{stem}'. Lancez run_demo.py d'abord.")
        return 1

    img_a = cv2.imread(str(classic))
    img_b = cv2.imread(str(sahi))

    h = min(img_a.shape[0], img_b.shape[0])
    img_a = cv2.resize(img_a, (int(img_a.shape[1] * h / img_a.shape[0]), h))
    img_b = cv2.resize(img_b, (int(img_b.shape[1] * h / img_b.shape[0]), h))

    top_a = _label_bar(img_a.shape[1], "YOLO26 classique")
    top_b = _label_bar(img_b.shape[1], "YOLO26 + SAHI", color=(20, 90, 20))
    col_a = np.vstack([top_a, img_a])
    col_b = np.vstack([top_b, img_b])

    sep = np.full((col_a.shape[0], 6, 3), 255, dtype=np.uint8)
    combined = np.hstack([col_a, sep, col_b])

    out = OUTPUTS_DIR / f"comparaison_{stem}.jpg"
    cv2.imwrite(str(out), combined)
    print(f"[compare] Comparatif enregistré : {out}")
    return 0

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python src/compare.py <nom_image_sans_extension>")
        return 1
    return make_comparison(sys.argv[1])

if __name__ == "__main__":
    sys.exit(main())
