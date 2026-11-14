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


# --- Descomposición del cambio de outliers al eliminar duplicados -------------
from src.quality import outlier_shift_breakdown  # noqa: E402


def _con_duplicado_extremo():
    base = list(range(10, 20)) + [100]
    raw = pd.DataFrame({"x": base + [100]})  # el 100 se repite
    return raw, raw.drop_duplicates().reset_index(drop=True)


def test_outlier_shift_caso_calculado_a_mano():
    raw, clean = _con_duplicado_extremo()
    r = outlier_shift_breakdown(raw, clean)
    assert r["crudo"] == 2
    assert r["en_duplicados_eliminados"] == 1
    assert r["limpio_con_limites_crudos"] == 1
    assert r["limpio"] == 1
    assert r["efecto_recalcular_cuartiles"] == 0


def test_outlier_shift_cumple_las_identidades_con_datos_aleatorios():
    rng = np.random.default_rng(7)
    raw = pd.DataFrame(rng.normal(size=(400, 3)), columns=list("abc"))
    raw = pd.concat([raw, raw.iloc[:60]], ignore_index=True)  # 60 duplicados
    clean = raw.drop_duplicates().reset_index(drop=True)
    r = outlier_shift_breakdown(raw, clean)

    assert r["crudo"] == int(outlier_counts_iqr(raw).sum())
    assert r["limpio"] == int(outlier_counts_iqr(clean).sum())
    assert r["crudo"] - r["en_duplicados_eliminados"] == r["limpio_con_limites_crudos"]
    assert r["limpio"] - r["limpio_con_limites_crudos"] == r["efecto_recalcular_cuartiles"]
    assert (r["limpio"] - r["crudo"]) == (
        r["efecto_recalcular_cuartiles"] - r["en_duplicados_eliminados"]
    )


def test_outlier_shift_por_columna_es_limpio_menos_crudo():
    raw, clean = _con_duplicado_extremo()
    r = outlier_shift_breakdown(raw, clean)
    esperado = outlier_counts_iqr(clean) - outlier_counts_iqr(raw)
    pd.testing.assert_series_equal(r["cambio_por_columna"], esperado)
