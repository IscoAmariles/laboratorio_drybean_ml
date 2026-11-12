# Reporte de ejecución · Sprint 1 (Comprensión y preparación)

**Fecha:** 2026-11-11 · **Rol:** Data Engineer / Analyst · **Rama:** `feature/data-preparacion` · **Plan:** [bitácora 01](2026-11-11_01_plan-data-engineer.md)

## Método
Se trabajó con TDD: primero las pruebas (fase roja, fallaban por módulos inexistentes), luego el código mínimo que las pasa, y al final se verificó cada entregable contra su criterio de aceptación.

## Resultado por backlog

| ID | Historia | Criterio de aceptación | Evidencia | Estado |
|---|---|---|---|---|
| PB-01 | Descargar dataset Dry Bean | El dataframe carga sin errores | `tests/test_data_loader.py` (5 pruebas), forma 13.611 × 17, copia en `data/raw/` | Hecho |
| PB-02 | Analizar calidad de datos | Hay resumen de calidad | `outputs/reports/resumen_calidad_datos.csv`, `resumen_clases.csv`, notebook 01 | Hecho |

## Entregables del Sprint 1 (según plan de equipo)

| Entregable | Ubicación |
|---|---|
| Repositorio configurado | `requirements.txt` con versiones fijas, `.gitignore`, estructura TDSP, `pytest.ini` |
| Dataset limpio | `data/processed/dry_bean_clean.csv` (13.543 filas) |
| Separación train/test | `data/processed/train.csv` (10.834) y `test.csv` (2.709) |
| Pipeline de preprocesamiento | `src/preprocessing.py` (`clean_data`, `split_data`, `build_preprocessor`) |
| Notebook inicial ejecutado | `notebooks/01_comprension_preparacion_datos.ipynb` |
| Análisis exploratorio | 4 gráficas en `outputs/reports/` |
| Diccionario de datos | `docs/diccionario_datos.md` |
| README profesional (borrador) | `README.md` |

## Hallazgos
1. 13.611 filas, 17 columnas, 16 características numéricas, sin nulos.
2. 68 duplicados, **todos de la clase `HOROZ`** (1.928 → 1.860).
3. Clases desbalanceadas: `DERMASON` 3.546 vs. `BOMBAY` 522 (razón 6,8). Métrica principal: F1 macro.
4. Colinealidad muy alta entre variables de tamaño y entre `Compactness`–`ShapeFactor3`. No afecta a Random Forest; puede afectar a Regresión Logística.
5. Los outliers por IQR (7.139) son mediciones físicas reales. No se eliminan.
6. El split estratificado conserva las proporciones por clase (diferencia máxima < 0,1 pp).

## Decisiones técnicas

| Decisión | Motivo |
|---|---|
| Eliminar duplicados antes del split | Evita que el mismo grano quede en train y en test (fuga de datos) |
| `clean_data` falla si hay nulos | No imputar en silencio; hoy no hay nulos y un cambio de fuente se notaría |
| `load_raw_data` lee el CSV si existe | Reproducible y sin depender de internet |
| `build_preprocessor` solo devuelve el scaler | El ajuste debe hacerse dentro del `Pipeline` con train para no filtrar información del test |
| No eliminar outliers ni variables colineales | Son datos reales; la decisión sobre colinealidad es del modelado (Sprint 2) |
| `outputs/models/*.joblib` en `.gitignore` | Pendiente de acordar con el equipo si el modelo final se versiona |

## Verificación
- `python -m pytest`: 15 pruebas en verde.
- Notebook ejecutado de inicio a fin sin errores (`jupyter nbconvert --execute`), con `assert` de forma del dataset y de proporciones del split.
- Se corrigió un error del dato de prueba de `test_quality.py` (dos filas idénticas en el fixture); el código era correcto.

## Pendientes para el equipo
- **ML Engineer:** consumir `data/processed/train.csv` y `test.csv`; usar `build_preprocessor()` dentro del `Pipeline`.
- **Scrum Master:** decidir si el `.joblib` final se sube a Git; actualizar el tablero (PB-01 y PB-02 en Hecho).
- **Todo el equipo:** revisar el Pull Request de `feature/data-preparacion` antes del merge.
- **Sprint 2 (Data Engineer):** análisis de errores por clase y cruce de importancia de variables con el EDA.

## Retrospectiva (borrador, a completar en equipo)
- **Qué funcionó:** TDD detectó rápido un error de prueba; el CSV crudo evita depender de la red.
- **Qué no funcionó:** el primer intento de generar el notebook falló por un problema del shell, se resolvió creando el script con otra herramienta.
- **Qué mejorar:** definir antes la política de versionado del modelo y de los CSV procesados.
