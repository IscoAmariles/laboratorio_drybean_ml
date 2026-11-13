"""PB-03 / PB-04: construcción de los modelos y carga de datos procesados."""
import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.models import build_baseline, build_random_forest, load_train_test

CLASES = ["A", "B", "C"]


@pytest.fixture
def datos():
    X, y = make_classification(
        n_samples=150, n_features=6, n_informative=4, n_redundant=0,
        n_classes=3, random_state=0,
    )
    X = pd.DataFrame(X, columns=[f"f{i}" for i in range(6)])
    y = pd.Series([CLASES[i] for i in y], name="Class")
    return X, y


def test_load_train_test_separa_features_y_objetivo(tmp_path, datos):
    X, y = datos
    df = X.assign(Class=y)
    df.iloc[:100].to_csv(tmp_path / "train.csv", index=False)
    df.iloc[100:].to_csv(tmp_path / "test.csv", index=False)

    X_train, X_test, y_train, y_test = load_train_test(tmp_path)

    assert "Class" not in X_train.columns and "Class" not in X_test.columns
    assert len(X_train) == len(y_train) == 100
    assert len(X_test) == len(y_test) == 50
    assert list(X_train.columns) == list(X.columns)
    assert y_train.name == "Class"


def test_load_train_test_con_datos_reales():
    X_train, X_test, y_train, y_test = load_train_test()
    assert X_train.shape == (10834, 16)
    assert X_test.shape == (2709, 16)
    assert set(y_train) == set(y_test)
    assert len(set(y_train)) == 7


def test_baseline_es_pipeline_con_scaler_y_regresion_logistica():
    modelo = build_baseline()
    assert isinstance(modelo, Pipeline)
    assert [n for n, _ in modelo.steps] == ["scaler", "classifier"]
    assert isinstance(modelo.named_steps["scaler"], StandardScaler)
    clf = modelo.named_steps["classifier"]
    assert isinstance(clf, LogisticRegression)
    assert clf.max_iter == 1000
    assert clf.random_state == 42


def test_random_forest_tiene_la_configuracion_del_laboratorio():
    modelo = build_random_forest()
    assert isinstance(modelo, Pipeline)
    clf = modelo.named_steps["classifier"]
    assert isinstance(clf, RandomForestClassifier)
    assert clf.n_estimators == 200
    assert clf.class_weight == "balanced"
    assert clf.random_state == 42


@pytest.mark.parametrize("builder", [build_baseline, build_random_forest])
def test_los_modelos_entrenan_y_predicen_etiquetas_validas(builder, datos):
    X, y = datos
    modelo = builder().fit(X, y)
    pred = modelo.predict(X)
    assert len(pred) == len(y)
    assert set(pred) <= set(CLASES)
