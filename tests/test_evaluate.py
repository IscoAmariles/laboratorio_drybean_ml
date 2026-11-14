"""PB-05: evaluación, matriz de confusión y comparación de modelos."""
import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, f1_score

from src.evaluate import (choose_simplest_equivalent, compare_models,
                          compare_to_reference, cross_validate_model, evaluate_model,
                          min_class_recall, paired_cv_scores, plot_confusion_matrix)
from src.models import build_baseline, build_random_forest

CLASES = ["A", "B", "C"]


@pytest.fixture
def datos():
    X, y = make_classification(
        n_samples=200, n_features=6, n_informative=4, n_redundant=0,
        n_classes=3, random_state=0,
    )
    X = pd.DataFrame(X, columns=[f"f{i}" for i in range(6)])
    y = pd.Series([CLASES[i] for i in y], name="Class")
    return X, y


def test_evaluate_model_devuelve_metricas_coherentes(datos):
    X, y = datos
    modelo = build_baseline().fit(X, y)
    res = evaluate_model(modelo, X, y)
    pred = modelo.predict(X)

    assert 0 <= res["accuracy"] <= 1
    assert 0 <= res["f1_macro"] <= 1
    assert res["accuracy"] == pytest.approx(accuracy_score(y, pred))
    assert res["f1_macro"] == pytest.approx(f1_score(y, pred, average="macro"))
    assert set(CLASES) <= set(res["report"])
    assert list(res["y_pred"]) == list(pred)


def test_plot_confusion_matrix_guarda_un_png(tmp_path, datos):
    X, y = datos
    pred = build_baseline().fit(X, y).predict(X)
    destino = tmp_path / "sub" / "matriz.png"

    plot_confusion_matrix(y, pred, "Matriz de prueba", destino)

    assert destino.exists() and destino.stat().st_size > 0


def test_compare_models_arma_tabla_y_la_guarda(tmp_path):
    resultados = {
        "Logistic Regression": {"accuracy": 0.90, "f1_macro": 0.91},
        "Random Forest": {"accuracy": 0.92, "f1_macro": 0.93},
    }
    destino = tmp_path / "comparacion.csv"

    tabla = compare_models(resultados, destino)

    assert list(tabla.columns[:3]) == ["modelo", "accuracy", "f1_macro"]
    assert list(tabla["modelo"]) == ["Logistic Regression", "Random Forest"]
    leido = pd.read_csv(destino)
    assert leido["f1_macro"].tolist() == pytest.approx([0.91, 0.93])


def test_compare_models_incluye_columnas_extra(tmp_path):
    resultados = {"M": {"accuracy": 0.9, "f1_macro": 0.9, "cv_f1_macro_mean": 0.88,
                        "cv_f1_macro_std": 0.01}}
    tabla = compare_models(resultados)
    assert {"cv_f1_macro_mean", "cv_f1_macro_std"} <= set(tabla.columns)


def test_cross_validate_model_devuelve_media_y_desviacion(datos):
    X, y = datos
    res = cross_validate_model(build_baseline(), X, y, cv=3)
    assert 0 <= res["cv_f1_macro_mean"] <= 1
    assert res["cv_f1_macro_std"] >= 0


# --- Sprint 3: comparación por pliegue y regla de decisión ---

def test_paired_cv_scores_usa_los_mismos_pliegues_para_todos(datos):
    X, y = datos
    modelos = {"LogReg": build_baseline(), "RF": build_random_forest(n_estimators=20)}
    puntajes = paired_cv_scores(modelos, X, y, cv=4)

    assert puntajes.shape == (4, 2)
    assert list(puntajes.columns) == ["LogReg", "RF"]
    assert puntajes.to_numpy().min() >= 0 and puntajes.to_numpy().max() <= 1
    repetido = paired_cv_scores(modelos, X, y, cv=4)
    pd.testing.assert_frame_equal(puntajes, repetido)


def test_compare_to_reference_cuenta_pliegues_ganados():
    puntajes = pd.DataFrame({
        "base": [0.90, 0.91, 0.92, 0.93, 0.94],
        "mejor": [0.91, 0.92, 0.93, 0.94, 0.95],
        "mixto": [0.89, 0.92, 0.91, 0.94, 0.94],
    })
    tabla = compare_to_reference(puntajes, "base")

    assert tabla.loc["mejor", "diff_media"] == pytest.approx(0.01)
    assert tabla.loc["mejor", "diff_std"] == pytest.approx(0.0, abs=1e-12)
    assert tabla.loc["mejor", "pliegues_ganados"] == 5
    assert tabla.loc["mixto", "pliegues_ganados"] == 2    # gana en 2 de 5; empata 1
    assert tabla.loc["base", "diff_media"] == 0 and tabla.loc["base", "pliegues_ganados"] == 0
    assert tabla.loc["mejor", "n_pliegues"] == 5


def _tabla_cv(filas):
    return pd.DataFrame(filas, columns=["modelo", "cv_f1_macro_mean", "cv_f1_macro_std"])


def test_choose_simplest_equivalent_elige_el_mas_simple_si_empatan():
    tabla = _tabla_cv([("A", 0.9365, 0.0037), ("B", 0.9343, 0.0047), ("C", 0.9354, 0.0043)])
    elegido, equivalentes = choose_simplest_equivalent(tabla, ["A", "B", "C"])
    assert elegido == "A"
    assert equivalentes == ["A", "B", "C"]


def test_choose_simplest_equivalent_elige_al_claramente_mejor():
    tabla = _tabla_cv([("A", 0.9365, 0.0037), ("B", 0.9436, 0.0049)])
    elegido, equivalentes = choose_simplest_equivalent(tabla, ["A", "B"])
    assert elegido == "B"
    assert equivalentes == ["B"]


def test_choose_simplest_equivalent_respeta_el_orden_de_complejidad():
    tabla = _tabla_cv([("A", 0.9300, 0.0100), ("B", 0.9310, 0.0100)])
    assert choose_simplest_equivalent(tabla, ["B", "A"])[0] == "B"
    assert choose_simplest_equivalent(tabla, ["A", "B"])[0] == "A"


def test_choose_simplest_equivalent_rechaza_modelos_sin_orden():
    tabla = _tabla_cv([("A", 0.93, 0.01), ("Z", 0.94, 0.01)])
    with pytest.raises(ValueError, match="Z"):
        choose_simplest_equivalent(tabla, ["A"])


def test_min_class_recall_devuelve_la_peor_clase():
    y_true = ["A", "A", "A", "A", "B", "B", "C", "C"]
    y_pred = ["A", "A", "A", "B", "B", "A", "C", "C"]
    clase, valor = min_class_recall(y_true, y_pred)
    assert (clase, valor) == ("B", 0.5)
