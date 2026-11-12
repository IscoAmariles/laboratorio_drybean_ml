"""Prueba de integración: el pipeline escribe los CSV procesados."""
import numpy as np
import pandas as pd

from src.make_dataset import build_datasets


def test_build_datasets_escribe_csv_consistentes(tmp_path):
    rng = np.random.default_rng(1)
    n = 300
    df = pd.DataFrame(
        {"a": rng.normal(size=n), "b": rng.normal(size=n),
         "Class": rng.choice(["X", "Y", "Z"], size=n)}
    )
    df = pd.concat([df, df.iloc[:10]], ignore_index=True)  # 10 duplicados

    info = build_datasets(df, processed_dir=tmp_path)

    clean = pd.read_csv(tmp_path / "dry_bean_clean.csv")
    train = pd.read_csv(tmp_path / "train.csv")
    test = pd.read_csv(tmp_path / "test.csv")
    assert info["duplicados_eliminados"] == 10
    assert len(clean) == n
    assert len(train) + len(test) == len(clean)
    assert "Class" in train.columns and "Class" in test.columns
