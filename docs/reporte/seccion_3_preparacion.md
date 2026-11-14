# Sección 3 · Preparación de los datos

*Borrador del Data Engineer / Analyst · Fase 3 de CRISP-DM. Código: [`src/preprocessing.py`](../../src/preprocessing.py) y [`src/make_dataset.py`](../../src/make_dataset.py), con pruebas en [`tests/`](../../tests/).*

## 3.1 Transformaciones realizadas

| Paso | Qué se hizo | Por qué | Resultado |
|---|---|---|---|
| 1. Ingesta | Descarga de UCI y copia sin modificar en `data/raw/` | El dato original queda intacto y el proyecto no depende de internet después | 13.611 × 17 |
| 2. Validar nulos | La limpieza **falla con error** si hay nulos, en vez de imputarlos en silencio | Hoy no hay; si cambiara la fuente, se notaría | 0 nulos |
| 3. Eliminar duplicados | `drop_duplicates()` | Un grano repetido podría quedar en train y en test e inflar las métricas | −68 filas → **13.543** |
| 4. División train/test | 80 % / 20 %, `random_state=42`, estratificada por `Class` | Reproducible y con las mismas proporciones de variedad en ambos conjuntos | 10.834 y 2.709 filas |
| 5. Escalado | `StandardScaler`, dentro del `Pipeline` del modelo y ajustado solo con train | Variables en escalas muy distintas (`Area` ≈ 10⁴, `Extent` ≈ 0,7); ajustar con test filtraría información | Listo en `build_preprocessor()` |

## 3.2 Qué no se hizo, y por qué

- **No se imputaron valores:** no hay nulos.
- **No se eliminaron valores atípicos:** son mediciones reales de granos, no errores de captura.
- **No se quitaron variables correlacionadas:** no afecta a los árboles y la decisión corresponde al modelado.
- **No se escaló antes de dividir:** habría usado información del test.

## 3.3 Verificación

- La división conserva las proporciones: la mayor diferencia entre train y test en cualquier variedad es de **0,03 puntos porcentuales**.
- Pruebas automáticas de la limpieza, la división (tamaño, ausencia de fuga, reproducibilidad, estratificación) y el escalador.
- El notebook 01 se ejecuta de inicio a fin sin errores y los archivos generados son idénticos entre ejecuciones.

## 3.4 Archivos resultantes

| Archivo | Contenido | Filas |
|---|---|---:|
| `data/raw/dry_bean_raw.csv` | Dato original | 13.611 |
| `data/processed/dry_bean_clean.csv` | Sin duplicados | 13.543 |
| `data/processed/train.csv` | Entrenamiento | 10.834 |
| `data/processed/test.csv` | Prueba | 2.709 |

Para regenerarlos: `python -m src.make_dataset`.
