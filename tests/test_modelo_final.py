"""Aceptación del modelo final versionado (DoD #7: se guarda el modelo final).

Se omite solo si el artefacto no existe (``python -m src.train`` lo regenera).
Los umbrales son la propuesta del diagnóstico (bitácora 06) para el criterio
numérico de aceptación; el Product Owner puede ajustarlos.
"""
from pathlib import Path

import pandas as pd
import pytest
from sklearn.metrics import f1_score

from src.evaluate import min_class_recall
from src.predict import load_metadata, load_model, predict_beans
from src.train import MODEL_FILE, MODELS_DIR

RUTA = Path(MODELS_DIR) / MODEL_FILE
UMBRAL_F1_MACRO = 0.92
UMBRAL_RECALL_MINIMO = 0.85

pytestmark = pytest.mark.skipif(not RUTA.exists(),
                                reason="falta el modelo; ejecutar python -m src.train")


@pytest.fixture(scope="module")
def prediccion():
    test = pd.read_csv("data/processed/test.csv")
    modelo = load_model(RUTA)
    return test["Class"], predict_beans(modelo, test)


def test_el_modelo_versionado_cumple_el_criterio_de_aceptacion(prediccion):
    y_true, y_pred = prediccion
    assert f1_score(y_true, y_pred, average="macro") >= UMBRAL_F1_MACRO
    _, recall = min_class_recall(y_true, y_pred)
    assert recall >= UMBRAL_RECALL_MINIMO


def test_la_metadata_coincide_con_la_evaluacion_real(prediccion):
    y_true, y_pred = prediccion
    meta = load_metadata(RUTA)
    assert meta["metrics"]["f1_macro"] == pytest.approx(
        f1_score(y_true, y_pred, average="macro"))
    assert meta["classes"] == sorted(y_true.unique())
    assert len(meta["features"]) == 16


def test_el_modelo_usa_las_mismas_versiones_que_el_entorno():
    import sklearn
    assert load_metadata(RUTA)["versions"]["scikit_learn"] == sklearn.__version__
