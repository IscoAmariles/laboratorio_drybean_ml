"""PB-05: evaluación de modelos, matriz de confusión y comparación."""
from pathlib import Path

import pandas as pd
from matplotlib.figure import Figure
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report, f1_score, recall_score)
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


def paired_cv_scores(models: dict, X, y, cv: int = 5, n_jobs=None) -> pd.DataFrame:
    """F1 macro por pliegue de cada modelo, sobre **los mismos** pliegues.

    Permite comparar por pliegue (diferencias emparejadas). Los modelos pueden
    ser ``GridSearchCV``: la validación cruzada resulta anidada (el ajuste de
    hiperparámetros ocurre solo dentro de cada pliegue de entrenamiento).
    """
    folds = StratifiedKFold(n_splits=cv, shuffle=True, random_state=RANDOM_STATE)
    columnas = {nombre: cross_val_score(modelo, X, y, cv=folds, scoring="f1_macro",
                                        n_jobs=n_jobs)
                for nombre, modelo in models.items()}
    return pd.DataFrame(columnas).rename_axis("pliegue")


def compare_to_reference(scores: pd.DataFrame, reference: str) -> pd.DataFrame:
    """Resume los puntajes por pliegue y los compara contra un modelo de referencia.

    Devuelve una fila por modelo con la media y desviación (ddof=0, igual que
    ``cross_validate_model``), la diferencia media contra la referencia, su
    desviación y en cuántos pliegues el modelo supera a la referencia.
    """
    ref = scores[reference]
    filas = {}
    for nombre in scores.columns:
        diff = scores[nombre] - ref
        filas[nombre] = {
            "cv_f1_macro_mean": scores[nombre].mean(),
            "cv_f1_macro_std": scores[nombre].std(ddof=0),
            "diff_media": diff.mean(),
            "diff_std": diff.std(ddof=0),
            "pliegues_ganados": int((diff > 1e-12).sum()),
            "n_pliegues": len(scores),
        }
    return pd.DataFrame(filas).T.astype({"pliegues_ganados": int, "n_pliegues": int})         .rename_axis("modelo")


def choose_simplest_equivalent(table: pd.DataFrame, order: list) -> tuple:
    """Elige el modelo final: el más simple entre los equivalentes al mejor.

    Dos modelos son equivalentes si la diferencia de sus medias de CV no supera
    la mayor de sus dos desviaciones. ``order`` va de más simple a más complejo.
    Devuelve ``(elegido, equivalentes)``.
    """
    t = table.set_index("modelo") if "modelo" in table.columns else table
    sin_orden = [m for m in t.index if m not in order]
    if sin_orden:
        raise ValueError(f"Sin orden de complejidad para: {sin_orden}")
    mejor = t["cv_f1_macro_mean"].idxmax()
    media_mejor, std_mejor = t.loc[mejor, "cv_f1_macro_mean"], t.loc[mejor, "cv_f1_macro_std"]
    equivalentes = [
        m for m in order if m in t.index
        and media_mejor - t.loc[m, "cv_f1_macro_mean"]
        <= max(std_mejor, t.loc[m, "cv_f1_macro_std"])
    ]
    return equivalentes[0], equivalentes


def min_class_recall(y_true, y_pred) -> tuple:
    """Clase con peor recall y su valor (criterio de aceptación por clase)."""
    clases = sorted(pd.Series(y_true).unique())
    recalls = recall_score(y_true, y_pred, labels=clases, average=None, zero_division=0)
    i = int(recalls.argmin())
    return clases[i], float(recalls[i])
