from __future__ import annotations

import os
import sys

from config import PROJECT_ROOT

ROBOFLOW_DATASETS = [

    ("roboflow-universe-projects", "traffic-signs-detection", 1),
]

DATASET_DIR = PROJECT_ROOT / "dataset"

def main() -> int:
    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if not api_key:
        print(
            "[data] Aucune clé ROBOFLOW_API_KEY trouvée.\n"
            "       1. Créez un compte gratuit sur https://roboflow.com\n"
            "       2. Récupérez votre clé API dans les paramètres du compte\n"
            "       3. export ROBOFLOW_API_KEY=\"votre_cle\"\n"
            "       Puis relancez : python src/prepare_data.py"
        )
        return 1

    try:
        from roboflow import Roboflow
    except ImportError:
        print(
            "[data] Le paquet 'roboflow' n'est pas installé.\n"
            "       Installez-le : pip install roboflow"
        )
        return 1

    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    rf = Roboflow(api_key=api_key)

    for workspace, project, version in ROBOFLOW_DATASETS:
        print(f"[data] Téléchargement de {workspace}/{project} v{version}...")
        proj = rf.workspace(workspace).project(project)

        proj.version(version).download("yolov8", location=str(DATASET_DIR))

    print(f"[data] Dataset prêt dans : {DATASET_DIR}")
    print("[data] Vérifiez/ajustez configs/data.yaml puis lancez src/train.py")
    return 0

if __name__ == "__main__":
    sys.exit(main())
