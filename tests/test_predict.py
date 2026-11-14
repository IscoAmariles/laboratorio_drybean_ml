"""Sprint 3 · Pasos 17 y 18: cargar el modelo y predecir con datos nuevos."""
import json
import warnings

import pandas as pd
import pytest

from src.predict import (load_metadata, load_model, main, predict_bean_class,
                         predict_beans)
from src.train import META_FILE, MODEL_FILE, train_final


@pytest.fixture
def artefacto(procesado_sintetico, tmp_path):
    destino = tmp_path / "models"
    train_final("logreg", procesado_sintetico, destino, tune=False)
    test = pd.read_csv(procesado_sintetico / "test.csv")
    return destino / MODEL_FILE, test


def test_predict_bean_class_devuelve_una_clase_valida(artefacto):
    ruta, test = artefacto
    modelo = load_model(ruta)
    fila = test.drop(columns="Class").iloc[[0]]
    assert predict_bean_class(modelo, fila) in {"A", "B", "C"}


def test_predict_bean_class_acepta_dict_y_serie(artefacto):
    ruta, test = artefacto
    modelo = load_model(ruta)
    fila = test.drop(columns="Class").iloc[0]
    assert predict_bean_class(modelo, fila) == predict_bean_class(modelo, fila.to_dict())


def test_predict_beans_no_depende_del_orden_de_las_columnas(artefacto):
    ruta, test = artefacto
    modelo = load_model(ruta)
    X = test.drop(columns="Class")
    barajado = X[list(reversed(X.columns))]
    assert list(predict_beans(modelo, barajado)) == list(predict_beans(modelo, X))


def test_predict_beans_ignora_columnas_extra(artefacto):
    ruta, test = artefacto
    modelo = load_model(ruta)
    assert len(predict_beans(modelo, test)) == len(test)   # test trae también 'Class'


def test_falta_una_variable_da_un_error_que_la_nombra(artefacto):
    ruta, test = artefacto
    modelo = load_model(ruta)
    with pytest.raises(ValueError, match="f3"):
        predict_beans(modelo, test.drop(columns=["Class", "f3"]))


def test_valores_nulos_dan_error(artefacto):
    ruta, test = artefacto
    modelo = load_model(ruta)
    X = test.drop(columns="Class").copy()
    X.loc[X.index[0], "f1"] = None
    with pytest.raises(ValueError, match="nulos"):
        predict_beans(modelo, X)


def test_load_model_advierte_si_cambia_la_version_de_sklearn(artefacto):
    ruta, _ = artefacto
    meta_ruta = ruta.parent / META_FILE
    meta = json.loads(meta_ruta.read_text(encoding="utf8"))
    meta["versions"]["scikit_learn"] = "0.0.1"
    meta_ruta.write_text(json.dumps(meta), encoding="utf8")
    with pytest.warns(UserWarning, match="0.0.1"):
        load_model(ruta)


def test_load_model_sin_advertencia_si_las_versiones_coinciden(artefacto):
    ruta, _ = artefacto
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        load_model(ruta)


def test_load_metadata_lee_el_json(artefacto):
    ruta, _ = artefacto
    assert load_metadata(ruta)["model_name"] == "logreg"


def test_cli_escribe_un_csv_con_las_predicciones(artefacto, tmp_path):
    ruta, test = artefacto
    entrada = tmp_path / "nuevos.csv"
    salida = tmp_path / "pred.csv"
    test.drop(columns="Class").to_csv(entrada, index=False)

    assert main(["--input", str(entrada), "--output", str(salida), "--model", str(ruta)]) == 0

    resultado = pd.read_csv(salida)
    assert len(resultado) == len(test)
    assert "predicted_class" in resultado.columns
    assert set(resultado["predicted_class"]) <= {"A", "B", "C"}
