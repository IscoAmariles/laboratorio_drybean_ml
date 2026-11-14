"""Análisis de errores del clasificador, para cruzarlo con el EDA."""
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report

REAL_COL = "real_class"
PRED_COL = "predicted_class"


def confusion_pairs(y_true, y_pred, top: int | None = None) -> pd.DataFrame:
    """Pares (real -> predicho) mal clasificados, del más al menos frecuente."""
    df = pd.DataFrame({"real": list(y_true), "predicho": list(y_pred)})
    errores = df[df["real"] != df["predicho"]]
    pares = (errores.groupby(["real", "predicho"]).size()
             .rename("errores").reset_index()
             .sort_values("errores", ascending=False, kind="stable")
             .reset_index(drop=True))
    return pares if top is None else pares.head(top)


def share_closer_to_other(values: pd.Series, own_median: float,
                          other_median: float) -> float:
    """Proporción de ``values`` más cercana a la mediana ajena que a la propia.

    Los empates no cuentan. Devuelve NaN si no hay valores.
    """
    if len(values) == 0:
        return float("nan")
    mas_cerca_de_la_otra = (values - other_median).abs() < (values - own_median).abs()
    return float(mas_cerca_de_la_otra.mean())


def error_group_summary(pred_df: pd.DataFrame, features: list[str],
                        class_a: str, class_b: str,
                        real_col: str = REAL_COL, pred_col: str = PRED_COL) -> pd.DataFrame:
    """Mediana de cada variable en los cuatro grupos de un par de clases.

    Columnas: ``A bien``, ``A→B`` (A predicha como B), ``B→A`` y ``B bien``.
    """
    def grupo(real, pred):
        return pred_df[(pred_df[real_col] == real) & (pred_df[pred_col] == pred)]

    grupos = {
        f"{class_a} bien": grupo(class_a, class_a),
        f"{class_a}→{class_b}": grupo(class_a, class_b),
        f"{class_b}→{class_a}": grupo(class_b, class_a),
        f"{class_b} bien": grupo(class_b, class_b),
    }
    return pd.DataFrame({nombre: g[features].median() for nombre, g in grupos.items()})


def per_class_metrics(y_true, y_pred) -> pd.DataFrame:
    """Precisión, recall, F1 y soporte por clase (incluye el promedio macro)."""
    rep = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    tabla = pd.DataFrame(rep).T.rename(columns={"f1-score": "f1"})
    tabla = tabla.drop(index="accuracy", errors="ignore")
    tabla["support"] = tabla["support"].astype(int)
    return tabla[["precision", "recall", "f1", "support"]]
