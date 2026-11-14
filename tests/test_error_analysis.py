"""Análisis de errores del clasificador cruzado con el EDA."""
import numpy as np
import pandas as pd
import pytest

from src.error_analysis import (confusion_pairs, error_group_summary,
                                per_class_metrics, share_closer_to_other)


def test_confusion_pairs_cuenta_solo_errores_y_ordena():
    y_true = ["A", "A", "A", "B", "B", "C", "C"]
    y_pred = ["A", "B", "B", "A", "B", "C", "A"]
    pares = confusion_pairs(y_true, y_pred)

    assert list(pares.columns) == ["real", "predicho", "errores"]
    assert pares.iloc[0].tolist() == ["A", "B", 2]        # el más frecuente primero
    assert set(map(tuple, pares[["real", "predicho"]].values)) == {
        ("A", "B"), ("B", "A"), ("C", "A")}
    assert pares["errores"].sum() == 4                    # no cuenta los aciertos


def test_confusion_pairs_respeta_top():
    y_true = ["A", "A", "B", "C"]
    y_pred = ["B", "B", "A", "A"]
    assert len(confusion_pairs(y_true, y_pred, top=1)) == 1


def test_confusion_pairs_sin_errores_devuelve_tabla_vacia():
    pares = confusion_pairs(["A", "B"], ["A", "B"])
    assert pares.empty and list(pares.columns) == ["real", "predicho", "errores"]


def test_share_closer_to_other_calcula_la_proporcion():
    valores = pd.Series([1.0, 2.0, 9.0, 10.0])
    # medianas: propia 0, ajena 10 -> 9 y 10 están más cerca de la ajena
    assert share_closer_to_other(valores, own_median=0.0, other_median=10.0) == 0.5


def test_share_closer_to_other_empate_no_cuenta_y_vacio_es_nan():
    assert share_closer_to_other(pd.Series([5.0]), 0.0, 10.0) == 0.0   # equidistante
    assert np.isnan(share_closer_to_other(pd.Series([], dtype=float), 0.0, 10.0))


def _pred_df():
    return pd.DataFrame({
        "f": [1, 1, 3, 5, 4, 6, 9, 9],
        "g": [0, 0, 0, 1, 1, 1, 2, 2],
        "real_class": ["A", "A", "A", "A", "B", "B", "B", "B"],
        "predicted_class": ["A", "A", "A", "B", "A", "A", "B", "B"],
    })


def test_error_group_summary_medianas_por_grupo():
    res = error_group_summary(_pred_df(), features=["f", "g"], class_a="A", class_b="B")

    assert list(res.index) == ["f", "g"]
    assert list(res.columns) == ["A bien", "A→B", "B→A", "B bien"]
    assert res.loc["f", "A bien"] == 1      # [1, 1, 3]
    assert res.loc["f", "A→B"] == 5         # [5]
    assert res.loc["f", "B→A"] == 5         # [4, 6]
    assert res.loc["f", "B bien"] == 9      # [9, 9]


def test_per_class_metrics_coincide_con_un_caso_conocido():
    y_true = ["A", "A", "B", "B"]
    y_pred = ["A", "B", "B", "B"]
    m = per_class_metrics(y_true, y_pred)

    assert list(m.columns) == ["precision", "recall", "f1", "support"]
    assert m.loc["A", "precision"] == pytest.approx(1.0)
    assert m.loc["A", "recall"] == pytest.approx(0.5)
    assert m.loc["B", "precision"] == pytest.approx(2 / 3)
    assert m.loc["B", "support"] == 2
    assert "macro avg" in m.index
