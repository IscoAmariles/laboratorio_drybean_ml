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


def _iqr_bounds(features: pd.DataFrame, k: float = 1.5):
    q1 = features.quantile(0.25)
    q3 = features.quantile(0.75)
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr


def _count_outside(features: pd.DataFrame, lower: pd.Series, upper: pd.Series) -> pd.Series:
    return (features.lt(lower) | features.gt(upper)).sum()


def outlier_counts_iqr(features: pd.DataFrame, k: float = 1.5) -> pd.Series:
    """Cuenta outliers por columna con la regla del rango intercuartílico."""
    lower, upper = _iqr_bounds(features, k)
    return _count_outside(features, lower, upper)


def outlier_shift_breakdown(raw_features: pd.DataFrame, clean_features: pd.DataFrame,
                            k: float = 1.5) -> dict:
    """Explica por qué cambia el conteo de outliers IQR al eliminar duplicados.

    Supone ``clean_features = raw_features.drop_duplicates()``. El cambio neto
    (limpio - crudo) se descompone en dos efectos:

    * ``en_duplicados_eliminados``: outliers (con los límites del crudo) que
      estaban en las filas repetidas y se van con ellas.
    * ``efecto_recalcular_cuartiles``: outliers nuevos o perdidos porque, sin
      duplicados, Q1 y Q3 se mueven y con ellos los límites.
    """
    lower, upper = _iqr_bounds(raw_features, k)
    removed = raw_features[raw_features.duplicated(keep="first")]

    crudo = int(_count_outside(raw_features, lower, upper).sum())
    en_duplicados = int(_count_outside(removed, lower, upper).sum())
    limpio_limites_crudos = int(_count_outside(clean_features, lower, upper).sum())
    limpio = int(outlier_counts_iqr(clean_features, k).sum())

    return {
        "crudo": crudo,
        "en_duplicados_eliminados": en_duplicados,
        "limpio_con_limites_crudos": limpio_limites_crudos,
        "limpio": limpio,
        "efecto_recalcular_cuartiles": limpio - limpio_limites_crudos,
        "cambio_por_columna": outlier_counts_iqr(clean_features, k)
        - outlier_counts_iqr(raw_features, k),
    }
