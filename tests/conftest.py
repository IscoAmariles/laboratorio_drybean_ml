"""Configuración común de pytest.

Las pruebas marcadas ``@pytest.mark.network`` necesitan descargar de UCI. Si UCI
no es accesible (sin internet, proxy caído) o se define ``DRYBEAN_SKIP_NETWORK=1``,
se omiten con un motivo visible en vez de fallar, y el resto de la suite sigue
en verde.
"""
import os
import urllib.error
import urllib.request

import pytest

UCI_URL = "https://archive.ics.uci.edu"


def uci_reachable(timeout: float = 3.0) -> bool:
    if os.environ.get("DRYBEAN_SKIP_NETWORK") == "1":
        return False
    try:
        urllib.request.urlopen(urllib.request.Request(UCI_URL, method="HEAD"),
                               timeout=timeout).close()
        return True
    except urllib.error.HTTPError:
        return True                      # el servidor respondió: hay conexión
    except Exception:
        return False


def pytest_collection_modifyitems(config, items):
    network_items = [i for i in items if "network" in i.keywords]
    if not network_items or uci_reachable():
        return
    skip = pytest.mark.skip(reason="UCI no es accesible (sin internet o DRYBEAN_SKIP_NETWORK=1)")
    for item in network_items:
        item.add_marker(skip)


# --- Datos sintéticos pequeños para probar entrenamiento y predicción sin los datos reales ---
@pytest.fixture
def procesado_sintetico(tmp_path):
    """Carpeta con train.csv y test.csv sintéticos (3 clases, 6 variables)."""
    import pandas as pd
    from sklearn.datasets import make_classification

    X, y = make_classification(n_samples=400, n_features=6, n_informative=4,
                               n_redundant=0, n_classes=3, random_state=0)
    df = pd.DataFrame(X, columns=[f"f{i}" for i in range(6)])
    df["Class"] = [["A", "B", "C"][i] for i in y]
    carpeta = tmp_path / "processed"
    carpeta.mkdir()
    df.iloc[:300].to_csv(carpeta / "train.csv", index=False)
    df.iloc[300:].to_csv(carpeta / "test.csv", index=False)
    return carpeta
