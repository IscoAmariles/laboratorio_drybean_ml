"""Preparación de datos: limpieza, split train/test y escalado."""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

TARGET_COL = "Class"
RANDOM_STATE = 42
TEST_SIZE = 0.2


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas duplicadas y valida que no haya nulos.

    No modifica el dataframe original.
    """
    n_nulos = int(df.isna().sum().sum())
    if n_nulos:
        raise ValueError(f"El dataset contiene {n_nulos} valores nulos")
    return df.drop_duplicates().reset_index(drop=True)


def split_data(df: pd.DataFrame, test_size: float = TEST_SIZE,
               random_state: int = RANDOM_STATE):
    """Separa X/y y hace el split estratificado y reproducible."""
    X = df.drop(columns=TARGET_COL)
    y = df[TARGET_COL]
    return train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )


def build_preprocessor() -> StandardScaler:
    """Escalador para encadenar en el Pipeline del ML Engineer."""
    return StandardScaler()
