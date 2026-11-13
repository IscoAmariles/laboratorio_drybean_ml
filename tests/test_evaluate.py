"""PB-05: evaluación, matriz de confusión y comparación de modelos."""
import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score, f1_score

from src.evaluate import (compare_models, cross_validate_model, evaluate_model,
                          plot_confusion_matrix)
from src.models import build_baseline

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
