"""Pruebas de PB-01: ingesta del Dry Bean Dataset.

Las pruebas unitarias usan un UCI simulado y corren sin internet. La prueba que
descarga el dataset real lleva el marcador ``network``: se omite sola si UCI no
es accesible (ver ``tests/conftest.py``).
"""
from types import SimpleNamespace

import pandas as pd
import pytest

from src.data_loader import TARGET_COL, UCI_ID, load_raw_data


class _FakeUCI:
    """Imita la respuesta de ``fetch_ucirepo`` y registra las llamadas."""

    def __init__(self):
        self.calls = []
        self.features = pd.DataFrame({"Area": [10, 20, 30], "Perimeter": [1.5, 2.5, 3.5]})
        self.targets = pd.DataFrame({"Class": ["A", "B", "A"]})

    def __call__(self, id):
        self.calls.append(id)
        return SimpleNamespace(data=SimpleNamespace(features=self.features,
                                                    targets=self.targets))


@pytest.fixture
def fake_uci(monkeypatch):
    fake = _FakeUCI()
    monkeypatch.setattr("src.data_loader.fetch_ucirepo", fake)
    return fake


def test_une_features_y_objetivo_en_un_solo_dataframe(tmp_path, fake_uci):
    df = load_raw_data(raw_path=tmp_path / "raw.csv")
    assert list(df.columns) == ["Area", "Perimeter", TARGET_COL]
    assert df.shape == (3, 3)


def test_descarga_el_dataset_602_de_uci(tmp_path, fake_uci):
    load_raw_data(raw_path=tmp_path / "raw.csv")
    assert fake_uci.calls == [UCI_ID] == [602]


def test_guarda_copia_cruda_y_crea_las_carpetas(tmp_path, fake_uci):
    destino = tmp_path / "data" / "raw" / "dry_bean_raw.csv"
    df = load_raw_data(raw_path=destino)
    assert destino.exists()
    pd.testing.assert_frame_equal(pd.read_csv(destino), df)


def test_segunda_carga_lee_de_disco_sin_descargar(tmp_path, fake_uci):
    destino = tmp_path / "raw.csv"
    primera = load_raw_data(raw_path=destino)
    segunda = load_raw_data(raw_path=destino)
    assert fake_uci.calls == [602]            # solo una descarga
    pd.testing.assert_frame_equal(primera, segunda)


@pytest.mark.network
def test_dataset_real_de_uci_tiene_la_forma_esperada(tmp_path):
    df = load_raw_data(raw_path=tmp_path / "dry_bean_raw.csv")
    assert df.shape == (13611, 17)
    assert TARGET_COL == "Class" and df[TARGET_COL].nunique() == 7
    features = df.drop(columns=TARGET_COL)
    assert features.shape[1] == 16
    assert all(pd.api.types.is_numeric_dtype(t) for t in features.dtypes)
