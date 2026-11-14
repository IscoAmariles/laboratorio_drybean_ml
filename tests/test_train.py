"""Sprint 3 · Paso 16: entrenamiento reproducible y guardado del modelo final."""
import json

import joblib
import pytest

from src.train import META_FILE, MODEL_FILE, main, train_final


def test_train_final_guarda_modelo_y_metadata(procesado_sintetico, tmp_path):
    destino = tmp_path / "models"
    meta = train_final("logreg", procesado_sintetico, destino, tune=False)

    assert (destino / MODEL_FILE).stat().st_size > 0
    guardada = json.loads((destino / META_FILE).read_text(encoding="utf8"))
    assert guardada == json.loads(json.dumps(meta, default=str))


def test_metadata_registra_lo_necesario_para_reproducir(procesado_sintetico, tmp_path):
    meta = train_final("logreg", procesado_sintetico, tmp_path / "m", tune=False)

    assert meta["model_name"] == "logreg"
    assert meta["random_state"] == 42
    assert meta["features"] == [f"f{i}" for i in range(6)]
    assert meta["classes"] == ["A", "B", "C"]
    assert meta["n_train"] == 300 and meta["n_test"] == 100
    assert {"python", "scikit_learn"} <= set(meta["versions"])
    assert {"accuracy", "f1_macro", "min_class_recall", "min_recall_class"} <= set(meta["metrics"])
    assert 0 <= meta["metrics"]["f1_macro"] <= 1
    assert set(meta["per_class"]) == {"A", "B", "C"}
    assert meta["trained_at"]


def test_se_guarda_el_pipeline_completo_no_solo_el_clasificador(procesado_sintetico, tmp_path):
    train_final("logreg", procesado_sintetico, tmp_path / "m", tune=False)
    modelo = joblib.load(tmp_path / "m" / MODEL_FILE)
    # sin el escalador la regresión logística predeciría con datos sin estandarizar
    assert [n for n, _ in modelo.steps] == ["scaler", "classifier"]


def test_modelo_cargado_predice_igual_que_el_de_memoria(procesado_sintetico, tmp_path):
    """Criterio de aceptación (Paso 17): el modelo se puede cargar y usar."""
    from src.models import build_model, load_train_test

    train_final("logreg", procesado_sintetico, tmp_path / "m", tune=False)
    X_train, X_test, y_train, _ = load_train_test(procesado_sintetico)
    en_memoria = build_model("logreg").fit(X_train, y_train).predict(X_test)
    cargado = joblib.load(tmp_path / "m" / MODEL_FILE).predict(X_test)
    assert list(cargado) == list(en_memoria)


def test_con_ajuste_guarda_el_mejor_pipeline_y_sus_parametros(procesado_sintetico, tmp_path):
    from sklearn.pipeline import Pipeline

    meta = train_final("svm", procesado_sintetico, tmp_path / "m", tune=True, inner_cv=3)
    assert meta["tuned"] is True
    assert set(meta["best_params"]) <= {"classifier__C", "classifier__gamma"}
    assert 0 <= meta["cv_f1_macro"] <= 1
    assert isinstance(joblib.load(tmp_path / "m" / MODEL_FILE), Pipeline)


def test_train_final_rechaza_modelos_desconocidos(procesado_sintetico, tmp_path):
    with pytest.raises(ValueError, match="desconocido"):
        train_final("xgboost", procesado_sintetico, tmp_path / "m")


def test_cli_entrena_y_devuelve_cero(procesado_sintetico, tmp_path):
    codigo = main(["--model", "logreg", "--no-tune",
                   "--processed-dir", str(procesado_sintetico),
                   "--models-dir", str(tmp_path / "m")])
    assert codigo == 0
    assert (tmp_path / "m" / MODEL_FILE).exists()
