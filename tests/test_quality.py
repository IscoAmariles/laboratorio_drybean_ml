"""Pruebas de PB-02: resumen de calidad de datos."""
import numpy as np
import pandas as pd

from src.quality import outlier_counts_iqr, quality_summary


def _df():
    return pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0, 4.0, 100.0, 2.5],
            "y": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            "Class": ["A", "A", "B", "B", "B", "A"],
        }
    )


def test_quality_summary_cuenta_filas_nulos_y_duplicados():
    df = _df()
    df.loc[0, "x"] = np.nan
    df = pd.concat([df, df.iloc[[1]]], ignore_index=True)
    s = quality_summary(df)
    assert s["filas"] == 7
    assert s["columnas"] == 3
    assert s["nulos_totales"] == 1
    assert s["duplicados"] == 1
    assert s["clases"] == {"A": 4, "B": 3}


def test_outliers_iqr_detecta_valor_extremo():
    out = outlier_counts_iqr(_df().drop(columns="Class"))
    assert out["x"] == 1
    assert out["y"] == 0
