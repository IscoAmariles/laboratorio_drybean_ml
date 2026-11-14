"""PB-03 / PB-04: modelos del laboratorio y carga de los datos procesados."""
from pathlib import Path

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from src.preprocessing import RANDOM_STATE, TARGET_COL, build_preprocessor

PROCESSED_DIR = Path("data/processed")


def load_train_test(processed_dir: Path = PROCESSED_DIR):
    """Lee train.csv y test.csv y devuelve X_train, X_test, y_train, y_test."""
    processed_dir = Path(processed_dir)
    train = pd.read_csv(processed_dir / "train.csv")
    test = pd.read_csv(processed_dir / "test.csv")
    return (
        train.drop(columns=TARGET_COL),
        test.drop(columns=TARGET_COL),
        train[TARGET_COL],
        test[TARGET_COL],
    )


def build_baseline() -> Pipeline:
    """Baseline: StandardScaler + Regresión Logística multiclase."""
    return Pipeline(steps=[
        ("scaler", build_preprocessor()),
        ("classifier", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
    ])


def build_random_forest(**params) -> Pipeline:
    """Modelo mejorado: Random Forest (sin escalado; es invariante a la escala).

    Va dentro de un Pipeline para exponer la misma interfaz que el baseline.
    Los ``params`` sobrescriben los valores por defecto del laboratorio.
    """
    config = {"n_estimators": 200, "random_state": RANDOM_STATE,
              "class_weight": "balanced", **params}
    return Pipeline(steps=[("classifier", RandomForestClassifier(**config))])


def build_svm(**params) -> Pipeline:
    """SVM con kernel RBF (requiere escalado, por eso lleva el StandardScaler)."""
    config = {"kernel": "rbf", "C": 10.0, "random_state": RANDOM_STATE, **params}
    return Pipeline(steps=[
        ("scaler", build_preprocessor()),
        ("classifier", SVC(**config)),
    ])


def build_hist_gradient_boosting(**params) -> Pipeline:
    """Gradient Boosting basado en histogramas (invariante a la escala).

    ``early_stopping=False`` fijo: con ``"auto"`` se activaría solo con más de
    10.000 filas y cambiaría el protocolo entre la validación cruzada y el
    ajuste final.
    """
    config = {"random_state": RANDOM_STATE, "early_stopping": False, **params}
    return Pipeline(steps=[("classifier", HistGradientBoostingClassifier(**config))])


# Candidatos del proyecto. El orden de COMPLEXITY_ORDER (de más simple a más
# complejo) desempata cuando varios modelos son estadísticamente equivalentes.
MODEL_BUILDERS = {
    "logreg": build_baseline,
    "random_forest": build_random_forest,
    "svm": build_svm,
    "hist_gb": build_hist_gradient_boosting,
}
COMPLEXITY_ORDER = ["logreg", "svm", "random_forest", "hist_gb"]

# Grillas de hiperparámetros (la regresión logística no se ajusta).
PARAM_GRIDS = {
    "random_forest": {"classifier__n_estimators": [200, 400],
                      "classifier__max_depth": [None, 10, 20],
                      "classifier__min_samples_split": [2, 5, 10]},
    "svm": {"classifier__C": [1, 10, 100],
            "classifier__gamma": ["scale", 0.01]},
    "hist_gb": {"classifier__learning_rate": [0.05, 0.1],
                "classifier__max_iter": [100, 300]},
}


def build_model(name: str, tune: bool = False, inner_cv: int = 5, n_jobs=None):
    """Construye un candidato por nombre.

    Con ``tune=True`` devuelve un ``GridSearchCV`` (F1 macro, CV estratificada)
    si el modelo tiene grilla; si no, el ``Pipeline`` simple.
    """
    if name not in MODEL_BUILDERS:
        raise ValueError(f"Modelo desconocido: {name!r}. Opciones: {sorted(MODEL_BUILDERS)}")
    modelo = MODEL_BUILDERS[name]()
    if tune and name in PARAM_GRIDS:
        cv = StratifiedKFold(n_splits=inner_cv, shuffle=True, random_state=RANDOM_STATE)
        return GridSearchCV(modelo, PARAM_GRIDS[name], scoring="f1_macro", cv=cv,
                            n_jobs=n_jobs)
    return modelo
