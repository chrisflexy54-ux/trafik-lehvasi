from __future__ import annotations

import sys
import time
from pathlib import Path

import cv2

from config import CONF_THRESHOLD, IMG_SIZE, IOU_THRESHOLD, OUTPUTS_DIR
from model_utils import load_model

def main() -> int:
    cam_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    weights = sys.argv[2] if len(sys.argv) > 2 else None

    model, name = load_model(preferred=weights)
    print(f"[camera] Modèle {name} — ouverture de la caméra {cam_index}...")

    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(
            f"[camera] Impossible d'ouvrir la caméra {cam_index}. "
            "Vérifiez la connexion / les autorisations macOS."
        )
        return 1

    prev_t = time.time()
    print("[camera] 'q' pour quitter, 's' pour sauvegarder une capture.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("[camera] Lecture du flux interrompue.")
            break

        results = model.predict(
            source=frame,
            conf=CONF_THRESHOLD,
            iou=IOU_THRESHOLD,
            imgsz=IMG_SIZE,
            verbose=False,
        )
        annotated = results[0].plot()

        now = time.time()
        fps = 1.0 / max(now - prev_t, 1e-6)
        prev_t = now
        cv2.putText(
            annotated,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Trafik Levhasi Tespiti - YOLO26", annotated)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("s"):
            out = OUTPUTS_DIR / f"camera_{int(now)}.jpg"
            cv2.imwrite(str(out), annotated)
            print(f"[camera] Capture enregistrée : {out}")

    cap.release()
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    sys.exit(main())
