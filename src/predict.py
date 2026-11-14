"""Mini despliegue (Pasos 17 y 18 del laboratorio): cargar el modelo y predecir.

Uso desde la terminal::

    python -m src.predict --input nuevos_granos.csv --output predicciones.csv

El CSV de entrada debe traer las 16 variables del dataset (en cualquier orden;
las columnas extra se ignoran).
"""
import argparse
import json
import warnings
from collections.abc import Mapping
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn

from src.train import META_FILE, MODEL_FILE, MODELS_DIR

DEFAULT_MODEL_PATH = Path(MODELS_DIR) / MODEL_FILE
PRED_COL = "predicted_class"


def load_metadata(model_path: Path = DEFAULT_MODEL_PATH) -> dict:
    """Lee el JSON de metadata que se guardó junto al modelo."""
    ruta = Path(model_path).with_name(META_FILE)
    return json.loads(ruta.read_text(encoding="utf8"))


def load_model(path: Path = DEFAULT_MODEL_PATH):
    """Carga el ``Pipeline`` guardado y avisa si cambió la versión de scikit-learn.

    ``joblib`` no garantiza que un modelo guardado con otra versión se comporte
    igual, por eso la versión de entrenamiento viaja en la metadata.
    """
    path = Path(path)
    modelo = joblib.load(path)
    if path.with_name(META_FILE).exists():
        entrenado = load_metadata(path)["versions"]["scikit_learn"]
        if entrenado != sklearn.__version__:
            warnings.warn(
                f"El modelo se entrenó con scikit-learn {entrenado} y este entorno tiene "
                f"{sklearn.__version__}; reentrenar con `python -m src.train`.",
                UserWarning, stacklevel=2)
    return modelo


def prepare_input(model, data) -> pd.DataFrame:
    """Valida y ordena la entrada según las variables con las que se entrenó el modelo."""
    if isinstance(data, pd.Series):
        df = data.to_frame().T
    elif isinstance(data, Mapping):
        df = pd.DataFrame([data])
    else:
        df = pd.DataFrame(data)

    esperadas = list(model.feature_names_in_)
    faltan = [c for c in esperadas if c not in df.columns]
    if faltan:
        raise ValueError(f"Faltan variables en la entrada: {faltan}")
    X = df[esperadas]
    con_nulos = [c for c in esperadas if X[c].isna().any()]
    if con_nulos:
        raise ValueError(f"La entrada tiene valores nulos en: {con_nulos}")
    return X.astype(float)


def predict_beans(model, data) -> np.ndarray:
    """Predice la variedad de cada fila de ``data``."""
    return model.predict(prepare_input(model, data))


def predict_bean_class(model, input_data) -> str:
    """Predice la variedad de **un** grano (fila de DataFrame, Series o dict)."""
    pred = predict_beans(model, input_data)
    if len(pred) != 1:
        raise ValueError(f"predict_bean_class espera una sola fila, recibió {len(pred)}")
    return str(pred[0])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Predice la variedad de frijol de un CSV.")
    parser.add_argument("--input", type=Path, required=True, help="CSV con las 16 variables")
    parser.add_argument("--output", type=Path, default=None,
                        help="CSV de salida (por defecto <entrada>_predicciones.csv)")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL_PATH)
    args = parser.parse_args(argv)

    modelo = load_model(args.model)
    datos = pd.read_csv(args.input)
    X = prepare_input(modelo, datos)

    salida = datos.copy()
    salida[PRED_COL] = modelo.predict(X)
    if hasattr(modelo, "predict_proba"):
        salida["confidence"] = modelo.predict_proba(X).max(axis=1)

    destino = args.output or args.input.with_name(args.input.stem + "_predicciones.csv")
    salida.to_csv(destino, index=False)
    print(f"{len(salida)} predicciones guardadas en {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
