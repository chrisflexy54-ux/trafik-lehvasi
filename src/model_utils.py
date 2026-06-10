from __future__ import annotations

from ultralytics import YOLO

from config import MODEL_CANDIDATES

def load_model(preferred: str | None = None):

    if preferred:
        return YOLO(preferred), preferred

    last_error: Exception | None = None
    for name in MODEL_CANDIDATES:
        try:
            model = YOLO(name)
            print(f"[model] Modèle chargé : {name}")
            return model, name
        except Exception as exc:
            print(f"[model] Échec du chargement de {name} ({exc}). Essai suivant...")
            last_error = exc

    raise RuntimeError(
        "Aucun modèle YOLO n'a pu être chargé. Vérifiez votre connexion "
        f"internet et l'installation d'ultralytics. Dernière erreur : {last_error}"
    )
