"""PB-05: evaluación de modelos, matriz de confusión y comparación."""
from pathlib import Path

import pandas as pd
from matplotlib.figure import Figure
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report, f1_score)
from sklearn.model_selection import StratifiedKFold, cross_val_score

from src.preprocessing import RANDOM_STATE


def evaluate_model(model, X_test, y_test) -> dict:
    """Predice sobre test y devuelve accuracy, F1 macro, reporte por clase y y_pred."""
    y_pred = model.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_macro": f1_score(y_test, y_pred, average="macro"),
        "report": classification_report(y_test, y_pred, output_dict=True,
                                        zero_division=0),
        "y_pred": y_pred,
    }


def plot_confusion_matrix(y_true, y_pred, title: str, path=None) -> Figure:
    """Dibuja la matriz de confusión y, si se da ``path``, la guarda como PNG."""
    fig = Figure(figsize=(8, 6))
    ax = fig.subplots()
    ConfusionMatrixDisplay.from_predictions(
        y_true, y_pred, xticks_rotation=45, ax=ax, colorbar=False
    )
    ax.set_title(title)
    fig.tight_layout()
    if path is not None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=150)
    return fig


def cross_validate_model(model, X, y, cv: int = 5) -> dict:
    """F1 macro por validación cruzada estratificada (media y desviación)."""
    folds = StratifiedKFold(n_splits=cv, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_val_score(model, X, y, cv=folds, scoring="f1_macro")
    return {"cv_f1_macro_mean": float(scores.mean()),
            "cv_f1_macro_std": float(scores.std())}


def compare_models(results: dict, path=None) -> pd.DataFrame:
    """Tabla comparativa: una fila por modelo. Si se da ``path``, la guarda en CSV.

    ``results`` es ``{nombre: {"accuracy": ..., "f1_macro": ..., ...}}``; las
    métricas extra (p. ej. las de validación cruzada) pasan como columnas.
    """
    tabla = pd.DataFrame(results).T.rename_axis("modelo").reset_index()
    if path is not None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        tabla.to_csv(path, index=False)
    return tabla
