"""Pipeline de datos: crudo -> limpio -> train/test en data/processed/."""
from pathlib import Path

import pandas as pd

from src.data_loader import load_raw_data
from src.preprocessing import TARGET_COL, clean_data, split_data

PROCESSED_DIR = Path("data/processed")


def build_datasets(df_raw: pd.DataFrame, processed_dir: Path = PROCESSED_DIR) -> dict:
    """Limpia, separa y guarda dry_bean_clean/train/test. Devuelve un resumen."""
    processed_dir = Path(processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)

    clean = clean_data(df_raw)
    X_train, X_test, y_train, y_test = split_data(clean)

    clean.to_csv(processed_dir / "dry_bean_clean.csv", index=False)
    X_train.assign(**{TARGET_COL: y_train}).to_csv(processed_dir / "train.csv", index=False)
    X_test.assign(**{TARGET_COL: y_test}).to_csv(processed_dir / "test.csv", index=False)

    return {
        "filas_crudas": len(df_raw),
        "duplicados_eliminados": len(df_raw) - len(clean),
        "filas_limpias": len(clean),
        "filas_train": len(X_train),
        "filas_test": len(X_test),
    }


if __name__ == "__main__":
    print(build_datasets(load_raw_data()))
