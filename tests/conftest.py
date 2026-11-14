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
