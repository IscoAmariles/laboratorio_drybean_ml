"""PB-03 / PB-04: modelos del laboratorio y carga de los datos procesados."""
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

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
