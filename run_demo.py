from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import cv2

from config import (
    CONF_THRESHOLD,
    IMG_SIZE,
    IOU_THRESHOLD,
    OUTPUTS_DIR,
    SAHI_OVERLAP_RATIO,
    SAHI_SLICE_HEIGHT,
    SAHI_SLICE_WIDTH,
    SAMPLES_DIR,
)
from model_utils import load_model

SAMPLE_URLS = {
    "rue_stop.jpg": "https://ultralytics.com/images/bus.jpg",
    "intersection.jpg": "https://raw.githubusercontent.com/ultralytics/assets/main/im/image-classification.jpg",
}

def ensure_samples() -> list[Path]:

    existing = sorted(
        p for p in SAMPLES_DIR.glob("*")
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )
    if existing:
        print(f"[demo] {len(existing)} image(s) trouvée(s) dans samples/")
        return existing

    downloaded: list[Path] = []
    for name, url in SAMPLE_URLS.items():
        dest = SAMPLES_DIR / name
        try:
            print(f"[demo] Téléchargement de {name}...")
            urllib.request.urlretrieve(url, dest)
            downloaded.append(dest)
        except Exception as exc:
            print(f"[demo] Échec du téléchargement de {name} : {exc}")
    return downloaded

def run_classic(model, image: Path) -> int:

    results = model.predict(
        source=str(image),
        conf=CONF_THRESHOLD,
        iou=IOU_THRESHOLD,
        imgsz=IMG_SIZE,
        verbose=False,
    )
    annotated = results[0].plot()
    out = OUTPUTS_DIR / f"classic_{image.stem}.jpg"
    cv2.imwrite(str(out), annotated)
    n = len(results[0].boxes)
    print(f"[demo] Classique : {n} objet(s) -> {out.name}")
    return n

def run_sahi(weights: str, image: Path) -> int:

    try:
        from sahi import AutoDetectionModel
        from sahi.predict import get_sliced_prediction
    except ImportError:
        print("[demo] SAHI non installé (pip install sahi) — étape ignorée.")
        return -1

    detection_model = AutoDetectionModel.from_pretrained(
        model_type="ultralytics",
        model_path=weights,
        confidence_threshold=CONF_THRESHOLD,
        device="cpu",
    )
    result = get_sliced_prediction(
        str(image),
        detection_model,
        slice_height=SAHI_SLICE_HEIGHT,
        slice_width=SAHI_SLICE_WIDTH,
        overlap_height_ratio=SAHI_OVERLAP_RATIO,
        overlap_width_ratio=SAHI_OVERLAP_RATIO,
    )
    result.export_visuals(export_dir=str(OUTPUTS_DIR), file_name=f"sahi_{image.stem}")
    n = len(result.object_prediction_list)
    print(f"[demo] SAHI : {n} objet(s) -> sahi_{image.stem}.png")
    return n

def main() -> int:
    print("=" * 60)
    print(" DÉMO — Détection de panneaux (YOLO26 + SAHI)")
    print("=" * 60)

    model, name = load_model()
    images = ensure_samples()
    if not images:
        print("[demo] Aucune image disponible. Placez des images dans samples/.")
        return 1

    for image in images:
        print(f"\n--- {image.name} ---")
        run_classic(model, image)
        run_sahi(name, image)

    print(f"\n[demo] Terminé. Visuels dans : {OUTPUTS_DIR}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
