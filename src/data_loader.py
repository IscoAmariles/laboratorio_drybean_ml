"""PB-01: ingesta del Dry Bean Dataset (UCI id=602)."""
from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo

UCI_ID = 602
TARGET_COL = "Class"
DEFAULT_RAW_PATH = Path("data/raw/dry_bean_raw.csv")


def load_raw_data(raw_path: Path = DEFAULT_RAW_PATH) -> pd.DataFrame:
    """Devuelve el dataset crudo (features + Class).

    Si ``raw_path`` existe lo lee de disco (reproducible, sin internet).
    Si no, lo descarga de UCI y guarda una copia sin modificar.
    """
    raw_path = Path(raw_path)
    if raw_path.exists():
        return pd.read_csv(raw_path)

    dry_bean = fetch_ucirepo(id=UCI_ID)
    df = pd.concat([dry_bean.data.features, dry_bean.data.targets], axis=1)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(raw_path, index=False)
    return df
