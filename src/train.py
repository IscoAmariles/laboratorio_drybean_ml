"""Entrenamiento reproducible del modelo final (Paso 16 del laboratorio).

Uso: ``python -m src.train`` (modelo por defecto) o ``python -m src.train --model svm``.

Guarda el ``Pipeline`` **completo** (escalador + clasificador) en
``outputs/models/modelo_final_drybean.joblib`` y, junto a él, un JSON con todo lo
necesario para reproducir y auditar el modelo (TDSP).
"""
import argparse
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import GridSearchCV

from src.evaluate import evaluate_model, min_class_recall
from src.models import MODEL_BUILDERS, PROCESSED_DIR, build_model, load_train_test
from src.preprocessing import RANDOM_STATE

MODELS_DIR = Path("outputs/models")
MODEL_FILE = "modelo_final_drybean.joblib"
META_FILE = "modelo_final_metadata.json"
# Elegido en el notebook 04 con la regla del equipo (CV anidada, por pliegue).
# Alternativa interpretable: python -m src.train --model logreg
DEFAULT_MODEL = "svm"


def train_final(model_name: str = DEFAULT_MODEL, processed_dir: Path = PROCESSED_DIR,
                models_dir: Path = MODELS_DIR, tune: bool = True, inner_cv: int = 5,
                n_jobs=None) -> dict:
    """Entrena con train, evalúa una sola vez en test y guarda modelo y metadata.

    Con ``tune=True`` los hiperparámetros se eligen por validación cruzada
    **dentro de train**; el test solo se usa para informar el desempeño.
    Devuelve la metadata (la misma que se escribe en el JSON).
    """
    X_train, X_test, y_train, y_test = load_train_test(processed_dir)
    estimador = build_model(model_name, tune=tune, inner_cv=inner_cv, n_jobs=n_jobs)
    estimador.fit(X_train, y_train)

    ajustado = isinstance(estimador, GridSearchCV)
    modelo = estimador.best_estimator_ if ajustado else estimador

    resultado = evaluate_model(modelo, X_test, y_test)
    clases = sorted(y_train.unique())
    clase_min, recall_min = min_class_recall(y_test, resultado["y_pred"])

    meta = {
        "model_name": model_name,
        "tuned": ajustado,
        "params": modelo[-1].get_params(),
        "best_params": estimador.best_params_ if ajustado else None,
        "cv_f1_macro": float(estimador.best_score_) if ajustado else None,
        "metrics": {
            "accuracy": float(resultado["accuracy"]),
            "f1_macro": float(resultado["f1_macro"]),
            "min_class_recall": recall_min,
            "min_recall_class": clase_min,
        },
        "per_class": {c: {k: float(resultado["report"][c][k])
                          for k in ("precision", "recall", "f1-score", "support")}
                      for c in clases},
        "features": list(X_train.columns),
        "classes": clases,
        "random_state": RANDOM_STATE,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "versions": {
            "python": platform.python_version(),
            "scikit_learn": sklearn.__version__,
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "joblib": joblib.__version__,
        },
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    models_dir = Path(models_dir)
    models_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, models_dir / MODEL_FILE)
    (models_dir / META_FILE).write_text(
        json.dumps(meta, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf8")
    return meta


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Entrena y guarda el modelo final.")
    parser.add_argument("--model", default=DEFAULT_MODEL, choices=sorted(MODEL_BUILDERS))
    parser.add_argument("--no-tune", action="store_true",
                        help="usar los hiperparámetros por defecto, sin GridSearchCV")
    parser.add_argument("--inner-cv", type=int, default=5)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--models-dir", type=Path, default=MODELS_DIR)
    args = parser.parse_args(argv)

    meta = train_final(args.model, args.processed_dir, args.models_dir,
                       tune=not args.no_tune, inner_cv=args.inner_cv, n_jobs=-1)
    m = meta["metrics"]
    print(f"Modelo: {meta['model_name']} | accuracy {m['accuracy']:.4f} | "
          f"F1 macro {m['f1_macro']:.4f} | peor recall {m['min_class_recall']:.3f} "
          f"({m['min_recall_class']})")
    print(f"Guardado en {args.models_dir / MODEL_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
