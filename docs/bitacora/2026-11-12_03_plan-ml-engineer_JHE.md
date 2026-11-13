> **Bitácora 03 · 2026-11-12** · Plan de trabajo del rol ML Engineer (JHE).
> Estado: **Sprint 2 ejecutado** (rama `feature/modelado`), ver [reporte del Sprint 2](2026-11-12_04_reporte-sprint-2.md). El Sprint 3 queda pendiente.

# Plan de trabajo: ML Engineer, proyecto Dry Bean ML

## Contexto
- **Responsabilidad (plan de equipo):** entrenar y evaluar los modelos. **Entregables:** modelos entrenados y métricas.
- **Historias del backlog:** PB-03 (Logistic Regression, alta), PB-04 (Random Forest, media), PB-05 (comparar métricas, todo el equipo; lo lidera el ML Engineer). Del enunciado: matriz de confusión y reporte, y guardar el modelo con joblib.
- **Insumos del Sprint 1** ([reporte](2026-11-11_02_reporte-sprint-1.md)):
  - `data/processed/train.csv` (10.834 filas) y `test.csv` (2.709), estratificados 80/20 con semilla 42, sin duplicados.
  - `build_preprocessor()` en `src/preprocessing.py` (un `StandardScaler` para el `Pipeline`).
  - Clases desbalanceadas (DERMASON 3.546 frente a BOMBAY 522): la métrica principal es **F1 macro**.
  - Colinealidad muy alta (`Area`–`ConvexArea`, `Compactness`–`ShapeFactor3`): puede afectar a la regresión logística y a la lectura de la importancia de variables.

---

## SPRINT 2: Modelado y evaluación

### 0. Preparación
0.1. `git pull origin main` y `git checkout -b feature/modelado`.
0.2. Crear el venv, instalar `requirements.txt` y correr `python -m pytest` (15 pruebas del Sprint 1 en verde).
0.3. Tablero: PB-03 y PB-04 a "En progreso".
0.4. TDD: primero las pruebas en `tests/`, luego el código en `src/`.

### 1. Código reutilizable en `src/`
1.1. `src/models.py`: `build_baseline()` (Pipeline con `StandardScaler` y `LogisticRegression(max_iter=1000, random_state=42)`), `build_random_forest()` (`n_estimators=200`, `random_state=42`, `class_weight="balanced"`, dentro de un Pipeline) y `load_train_test()`.
1.2. `src/evaluate.py`: `evaluate_model()`, `plot_confusion_matrix()`, `compare_models()` y `cross_validate_model()`.
1.3. Pruebas: `tests/test_models.py` y `tests/test_evaluate.py` (modelos entrenan con datos pequeños, métricas entre 0 y 1, los archivos de salida se crean con `tmp_path`).

### 2. PB-03: baseline con Logistic Regression (pasos 9 y 10 del lab)
2.1. Notebook `notebooks/02_modelado_evaluacion.ipynb`, importando todo desde `src/`.
2.2. Entrenar con train, predecir sobre test, reportar accuracy, F1 macro y `classification_report` (criterio de aceptación).
2.3. Responder por qué F1 macro es más informativo que accuracy con clases desbalanceadas.

### 3. PB-04: Random Forest (pasos 11 y 12)
3.1. Entrenar y evaluar con las mismas métricas.
3.2. Documentar que no necesita escalado y que `class_weight="balanced"` compensa el desbalance.
3.3. Criterio de aceptación: comparación contra el baseline.

### 4. PB-05: comparación y decisión del modelo (pasos 13 y 14)
4.1. Tabla `outputs/reports/comparacion_modelos.csv` (accuracy, F1 macro, media y desviación de la validación cruzada).
4.2. Validación cruzada: `StratifiedKFold(5, shuffle=True, random_state=42)`, `scoring="f1_macro"`, solo sobre train.
4.3. Decisión del modelo final: priorizar F1 macro, revisar errores por clase y, si el desempeño es muy parecido, preferir el más simple. Dejarla justificada en el notebook.
4.4. Matrices de confusión (`matriz_confusion_logreg.png`, `matriz_confusion_rf.png`) y análisis de las clases que más se confunden (se espera SIRA↔DERMASON y BARBUNYA↔CALI), en coordinación con el Data Engineer.
4.5. Opcional: `GridSearchCV` sobre Random Forest (`n_estimators`, `max_depth`, `min_samples_split`) solo con train. El conjunto de test se usa una sola vez al final.

### 5. Interpretación del modelo (paso 15)
5.1. Top 10 de `feature_importances_` (`importancia_variables.csv` y `.png`).
5.2. `permutation_importance` sobre test: con variables colineales la importancia por impureza se reparte entre las gemelas. Aclarar que importancia no implica causalidad.
5.3. Si se elige la regresión logística, interpretar sus coeficientes estandarizados.
5.4. Extensión C: `outputs/reports/predicciones_drybean.csv` con `real_class` y `predicted_class`.

### 6. Cierre del Sprint 2
6.1. Notebook 02 ejecutado de inicio a fin sin errores y `pytest` en verde.
6.2. PR de `feature/modelado` hacia `main` con revisión.
6.3. Reporte del sprint en la bitácora (métricas, decisión del modelo, pendientes).
6.4. Sprint review: tabla comparativa y matriz de confusión; el Product Owner valida contra el objetivo de negocio.

**Entregables Sprint 2:** modelo baseline, modelo mejorado, comparación de métricas, matrices de confusión e importancia de variables.

---

## SPRINT 3: Despliegue y documentación (pendiente)

### 7. Guardar el modelo (pasos 16 y 17)
7.1. `src/train.py` (`python -m src.train`): entrena el modelo final, evalúa y guarda el **Pipeline completo** en `outputs/models/modelo_final_drybean.joblib`.
7.2. `outputs/models/modelo_final_metadata.json`: nombre, hiperparámetros, métricas en test, versión de scikit-learn, fecha, variables en orden y clases.
7.3. Decidir con el Scrum Master si el `.joblib` se sube a Git (hoy `.gitignore` lo excluye). Si no se sube, `python -m src.train` debe regenerarlo.
7.4. Prueba que cargue el modelo, prediga una fila de test y devuelva una clase válida.

### 8. Mini despliegue (paso 18, fase Despliegue de CRISP-DM)
8.1. `src/predict.py`: `load_model(path)` y `predict_bean_class(model, input_data)` con validación de las 16 columnas.
8.2. Opcional: CLI `python -m src.predict --input nuevos_granos.csv`.
8.3. Demostración en notebook: cargar, predecir una muestra y compararla con el valor real.

### 9. Documentación y entrega
9.1. Reporte final (Entregable 2): secciones 4 (Modelado), 5 (Evaluación) y 6 (Despliegue).
9.2. Aportes al README: entrenamiento, resultados (tabla y matriz), uso del modelo y estado del proyecto.
9.3. Preguntas de reflexión: baseline, métrica elegida, qué hacer si una clase falla más, qué falta para producción (drift, calibración de cámara, umbrales de confianza).
9.4. Láminas: comparación de modelos, matriz de confusión, importancia de variables y demo.
9.5. Reproducibilidad: clonar en carpeta limpia y correr `src.make_dataset`, `src.train`, `pytest` y notebooks.
9.6. Retrospectiva.

---

## Scrum: actividades continuas
- Daily: qué hice, qué haré, qué bloqueos tengo.
- PB-03, PB-04 y PB-05 se cierran solo con su criterio de aceptación cumplido y mergeados en `main` por PR.
- Dependencias: del Data Engineer, análisis de errores y cruce con el EDA; al Scrum Master, secciones del README y decisión sobre el `.joblib`; el Product Owner valida al final.

## Archivos que corresponden al ML Engineer
| Archivo | Propósito |
|---|---|
| `src/models.py`, `src/evaluate.py` | Construir y evaluar los modelos |
| `src/train.py`, `src/predict.py` | Entrenamiento reproducible y despliegue (Sprint 3) |
| `tests/test_models.py`, `test_evaluate.py`, `test_predict.py` | Pruebas |
| `notebooks/02_modelado_evaluacion.ipynb` | Pasos 9–18 ejecutados y documentados |
| `outputs/reports/comparacion_modelos.csv`, `matriz_confusion_*.png`, `importancia_variables.*`, `predicciones_drybean.csv` | Evidencia de la evaluación |
| `outputs/models/modelo_final_drybean.joblib` + metadata | Modelo final |

## Definition of Done (parte del ML Engineer)
1. El notebook 02 corre de inicio a fin sin errores.
2. Baseline y modelo alternativo comparados con accuracy, F1 macro y validación cruzada.
3. Matrices de confusión y análisis de las clases confundidas.
4. Modelo final guardado, cargable y cubierto por una prueba.
5. Resultados explicados en lenguaje claro y conectados con CRISP-DM.
6. PR revisado y mergeado en `main`.
