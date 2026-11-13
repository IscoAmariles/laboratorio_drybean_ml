# Reporte de ejecución · Sprint 2 (Modelado y evaluación)

**Fecha:** 2026-11-12 · **Rol:** ML Engineer (JHE) · **Rama:** `feature/modelado` · **Plan:** [bitácora 03](2026-11-12_03_plan-ml-engineer_JHE.md)

## Método
TDD: primero `tests/test_models.py` y `tests/test_evaluate.py` (fase roja: `ModuleNotFoundError` por módulos inexistentes), luego el código mínimo en `src/models.py` y `src/evaluate.py` hasta ponerlas en verde, y al final el notebook `02_modelado_evaluacion.ipynb` ejecutado de inicio a fin. Las decisiones se toman con validación cruzada **solo sobre train**; el test solo informa el desempeño.

## Resultado por backlog

| ID | Historia | Criterio de aceptación | Evidencia | Estado |
|---|---|---|---|---|
| PB-03 | Entrenar Logistic Regression | Se reporta accuracy y F1 macro | Notebook 02 §2: accuracy 0,9195, F1 macro 0,9306 | Hecho |
| PB-04 | Entrenar Random Forest | Se compara contra el baseline | Notebook 02 §3–5: accuracy 0,9195, F1 macro 0,9310 | Hecho |
| PB-05 | Comparar métricas | Tabla comparativa | `outputs/reports/comparacion_modelos.csv` | Hecho |
| — | Matriz de confusión y reporte | Se documentan hallazgos | `matriz_confusion_logreg.png`, `matriz_confusion_rf.png`, notebook §7 y §10 | Hecho |
| — | Guardar modelo con joblib | El modelo se puede cargar y usar | Planificado para el Sprint 3 | Pendiente |

## Comparación de modelos

| Modelo | Accuracy (test) | F1 macro (test) | F1 macro CV (train, 5 pliegues) |
|---|---|---|---|
| Logistic Regression | 0,9195 | 0,9306 | 0,9365 ± 0,0037 |
| Random Forest | 0,9195 | 0,9310 | 0,9343 ± 0,0047 |
| Random Forest ajustado (`max_depth=20`, `min_samples_split=2`, `n_estimators=400`) | 0,9192 | 0,9308 | 0,9354 ± 0,0043 |

## Hallazgos
1. **Los tres modelos son equivalentes.** La diferencia en test es de 0,0004 de F1 macro y en CV de 0,002, menor que la desviación entre pliegues (≈ 0,004).
2. **Modelo elegido: Regresión Logística** (criterio del laboratorio: ante desempeño parecido, el más simple). Ni el ajuste de hiperparámetros hace que Random Forest supere al baseline.
3. **Errores concentrados en DERMASON ↔ SIRA:** 94 de los 218 errores de la regresión logística (43 %). Forma casi idéntica (relación de aspecto mediana 1,48 vs 1,56; solidez 0,989 en ambas) y diferencia sobre todo de tamaño, con solapamiento. `SIRA` tiene el peor F1 (0,87).
4. **BARBUNYA ↔ CALI** es el segundo par (≈ 17–19 errores por sentido); `BOMBAY` no tiene errores (F1 = 1,00).
5. **Importancia de variables:** por impureza se reparte entre variables colineales; por permutación destaca `Roundness` (0,084), muy por encima del resto. Las variables de tamaño gemelas no pierden al permutarse porque se reemplazan entre sí.

## Decisiones técnicas

| Decisión | Motivo |
|---|---|
| Decidir el modelo con CV sobre train, no con test | Evita elegir mirando el conjunto de prueba |
| Equivalencia = diferencia de medias CV menor que la mayor desviación | Regla explícita y reproducible en el notebook |
| Random Forest dentro de un `Pipeline` sin scaler | Misma interfaz que el baseline |
| `plot_confusion_matrix` usa `matplotlib.figure.Figure` sin `pyplot` | No cambia el backend del notebook y guarda el PNG sin ventana |
| Modelo final no guardado en este sprint | Va en el Sprint 3 (`src/train.py`, `Pipeline` completo + metadata) |

## Incidencia de reproducibilidad (resuelta)
La primera ejecución del notebook con `jupyter nbconvert` usó el kernel `python3` de **Anaconda** (scikit-learn 1.6.1) y no el `.venv` (scikit-learn 1.9.1 fijado en `requirements.txt`). Los números de Random Forest diferían en 3 milésimas y el ajuste eligió otros hiperparámetros. Se corrigió ejecutando con `PATH` y `JUPYTER_PATH` apuntando al `.venv`, y el notebook ahora imprime las versiones de Python y scikit-learn en su primera celda. **Cómo ejecutarlo** (PowerShell, desde la raíz):

```powershell
.venv\Scripts\Activate.ps1
$env:JUPYTER_PATH = "$PWD\.venv\share\jupyter"
jupyter nbconvert --to notebook --execute --inplace notebooks/02_modelado_evaluacion.ipynb
```

## Verificación
- `python -m pytest --deselect tests/test_data_loader.py` con `.venv`: 21 pruebas en verde (11 nuevas en `test_models.py` y `test_evaluate.py`, más las 10 de `test_preprocessing`, `test_quality` y `test_make_dataset`).
- `tests/test_data_loader.py` (5 pruebas del Sprint 1) **fallan en este entorno sin red** con `ConnectionError`: descargan de UCI. No se relacionan con este sprint; deben correrse con internet.
- Notebook 02 ejecutado de inicio a fin sin errores con scikit-learn 1.9.1.

## Pendientes
- **Sprint 3 (ML Engineer):** `src/train.py` y `src/predict.py`, guardar el `Pipeline` en `.joblib` con metadata, reporte final (secciones 4–6) y README.
- **Scrum Master:** decidir si el `.joblib` se versiona; mover PB-03, PB-04 y PB-05 a Hecho.
- **Data Engineer:** análisis de errores DERMASON↔SIRA con el EDA (`outputs/reports/predicciones_drybean.csv`).
- **Todo el equipo:** revisar el PR de `feature/modelado`.

## Retrospectiva (borrador, a completar en equipo)
- **Qué funcionó:** la comparación con CV evitó vender una mejora que era ruido; TDD dejó `src/` probado.
- **Qué no funcionó:** el kernel de Jupyter apuntaba a otro Python y alteró los resultados sin avisar; la instalación del entorno tardó más de 10 minutos.
- **Qué mejorar:** registrar la versión de librerías en cada notebook y probar los tests de red con un fixture que no descargue.
