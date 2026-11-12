"""Pruebas de PB-01: ingesta del Dry Bean Dataset."""
import pandas as pd
import pytest

from src.data_loader import TARGET_COL, load_raw_data

N_ROWS, N_COLS, N_CLASSES = 13611, 17, 7


@pytest.fixture(scope="module")
def raw_df(tmp_path_factory):
    path = tmp_path_factory.mktemp("raw") / "dry_bean_raw.csv"
    return load_raw_data(raw_path=path), path


def test_carga_sin_errores_y_forma_esperada(raw_df):
    df, _ = raw_df
    assert df.shape == (N_ROWS, N_COLS)


def test_variable_objetivo_presente_con_7_clases(raw_df):
    df, _ = raw_df
    assert TARGET_COL == "Class"
    assert df[TARGET_COL].nunique() == N_CLASSES


def test_features_son_numericas(raw_df):
    df, _ = raw_df
    features = df.drop(columns=TARGET_COL)
    assert features.shape[1] == 16
    assert all(pd.api.types.is_numeric_dtype(t) for t in features.dtypes)


def test_guarda_copia_cruda_en_disco(raw_df):
    _, path = raw_df
    assert path.exists()


def test_segunda_carga_lee_de_disco_sin_internet(raw_df, monkeypatch):
    df, path = raw_df

    def sin_red(*args, **kwargs):
        raise AssertionError("No debe descargar si el CSV ya existe")

    monkeypatch.setattr("src.data_loader.fetch_ucirepo", sin_red)
    df2 = load_raw_data(raw_path=path)
    pd.testing.assert_frame_equal(df, df2)
