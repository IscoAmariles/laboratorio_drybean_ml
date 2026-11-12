"""Pruebas de la preparación de datos (limpieza, split, scaler)."""
import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler

from src.preprocessing import build_preprocessor, clean_data, split_data


@pytest.fixture
def df_pequeno():
    rng = np.random.default_rng(0)
    n = 200
    df = pd.DataFrame(
        {
            "Area": rng.normal(100, 10, n),
            "Perimeter": rng.normal(50, 5, n),
            "Class": rng.choice(["A", "B", "C"], size=n, p=[0.6, 0.3, 0.1]),
        }
    )
    return df


def test_clean_data_elimina_duplicados(df_pequeno):
    sucio = pd.concat([df_pequeno, df_pequeno.iloc[:5]], ignore_index=True)
    limpio = clean_data(sucio)
    assert len(limpio) == len(df_pequeno)
    assert not limpio.duplicated().any()


def test_clean_data_no_modifica_el_original(df_pequeno):
    sucio = pd.concat([df_pequeno, df_pequeno.iloc[:5]], ignore_index=True)
    n_antes = len(sucio)
    clean_data(sucio)
    assert len(sucio) == n_antes


def test_clean_data_falla_si_hay_nulos(df_pequeno):
    df_pequeno.loc[0, "Area"] = np.nan
    with pytest.raises(ValueError, match="nulos"):
        clean_data(df_pequeno)


def test_split_20_porciento_y_sin_fuga(df_pequeno):
    X_tr, X_te, y_tr, y_te = split_data(df_pequeno)
    assert len(X_te) == pytest.approx(0.2 * len(df_pequeno), abs=1)
    assert len(X_tr) + len(X_te) == len(df_pequeno)
    assert set(X_tr.index).isdisjoint(X_te.index)
    assert "Class" not in X_tr.columns


def test_split_estratificado_conserva_proporciones(df_pequeno):
    _, _, y_tr, y_te = split_data(df_pequeno)
    prop_tr = y_tr.value_counts(normalize=True)
    prop_te = y_te.value_counts(normalize=True)
    for clase in prop_tr.index:
        assert prop_tr[clase] == pytest.approx(prop_te[clase], abs=0.03)


def test_split_es_reproducible(df_pequeno):
    a = split_data(df_pequeno)
    b = split_data(df_pequeno)
    pd.testing.assert_frame_equal(a[0], b[0])
    pd.testing.assert_series_equal(a[3], b[3])


def test_build_preprocessor_devuelve_standard_scaler():
    assert isinstance(build_preprocessor(), StandardScaler)
