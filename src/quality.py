"""PB-02: métricas de calidad de datos."""
import pandas as pd

TARGET_COL = "Class"


def quality_summary(df: pd.DataFrame) -> dict:
    """Resumen de calidad: tamaño, nulos, duplicados y distribución de clases."""
    return {
        "filas": int(len(df)),
        "columnas": int(df.shape[1]),
        "nulos_totales": int(df.isna().sum().sum()),
        "duplicados": int(df.duplicated().sum()),
        "clases": df[TARGET_COL].value_counts().to_dict(),
    }


def outlier_counts_iqr(features: pd.DataFrame, k: float = 1.5) -> pd.Series:
    """Cuenta outliers por columna con la regla del rango intercuartílico."""
    q1 = features.quantile(0.25)
    q3 = features.quantile(0.75)
    iqr = q3 - q1
    mask = features.lt(q1 - k * iqr) | features.gt(q3 + k * iqr)
    return mask.sum()
