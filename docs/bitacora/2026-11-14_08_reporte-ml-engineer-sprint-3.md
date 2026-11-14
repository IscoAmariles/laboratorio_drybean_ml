# Reporte de ejecución · Sprint 3 (ML Engineer): despliegue y documentación

**Fecha:** 2026-11-14 · **Rol:** ML Engineer (JHE) · **Rama:** `feature/despliegue-sprint3` · **Plan:** [bitácora 03](2026-11-12_03_plan-ml-engineer_JHE.md) (secciones 7 a 9) · **Recomendaciones atendidas:** [bitácora 06](2026-11-14_06_diagnostico-y-recomendaciones-por-rol.md), sección "ML Engineer"

## Método
TDD: primero las pruebas (fase roja: 5 módulos de prueba fallaban por funciones y módulos inexistentes), luego el código mínimo hasta ponerlas en verde, y al final se ejecutó de inicio a fin el notebook 04 con el kernel del `.venv` (scikit-learn 1.9.1). Las decisiones se toman con validación cruzada sobre train; el test solo informa.

## Recomendaciones del diagnóstico para el ML Engineer

| # | Recomendación | Resultado | Evidencia |
|---|---|---|---|
| 1 | `train.py`, `predict.py` y guardar el `Pipeline` completo | Hecho | `src/train.py`, `src/predict.py`, `tests/test_train.py`, `tests/test_predict.py` |
| 2 | Prueba formal de SVM y Gradient Boosting con el mismo protocolo | Hecho. **Cambia la elección del modelo** | Notebook 04 §2–3, `outputs/reports/comparacion_ampliada*.csv/png` |
| 3 | Corregir la frase de BARBUNYA↔CALI | Hecho | Notebook 02 §10 y [reporte del Sprint 2](2026-11-12_04_reporte-sprint-2.md) |
| 4 | Reporte por clase y matriz normalizada | Hecho para el modelo final (el Data Engineer ya los tenía para la regresión logística) | `metricas_por_clase_modelo_final.csv`, `matriz_confusion_normalizada_modelo_final.png` |
| 5 | Pasos 17 y 18 con el modelo cargado | Hecho | Notebook 04 §6–7; `test_modelo_cargado_predice_igual_que_el_de_memoria` |
| 6 | Secciones 4 a 6 del reporte | Borrador hecho | [`docs/reporte/`](../reporte/) |

## Resultado por backlog

| ID | Historia | Criterio de aceptación | Evidencia | Estado |
|---|---|---|---|---|
| PB-05 | Comparar métricas | Tabla comparativa | `comparacion_ampliada.csv` (4 modelos, por pliegue y anidada) | Hecho |
| — | Como equipo técnico, quiero reproducibilidad: guardar el modelo con `joblib` | El modelo se puede cargar y usar | `outputs/models/modelo_final_drybean.joblib` + metadata; prueba de aceptación sobre `test.csv` | Hecho |

## Decisión del modelo final: cambia de regresión logística a SVM

| Modelo | F1 macro CV (anidada, 5 pliegues) | Diferencia vs. logreg | Pliegues ganados |
|---|---|---|---|
| Regresión logística | 0,9365 ± 0,0037 | — | — |
| Random Forest | 0,9343 ± 0,0047 | −0,0022 | 1 de 5 |
| **SVM RBF** | **0,9432 ± 0,0049** | **+0,0068** | **5 de 5** |
| Gradient Boosting | 0,9405 ± 0,0033 | +0,0041 | 5 de 5 |

Con la regla del equipo (equivalentes si la diferencia de medias no supera la mayor desviación; entre ellos, el más simple), la regresión logística deja de ser equivalente al mejor. Gradient Boosting sí lo es y se elige la SVM por simplicidad. Hiperparámetros: `C=100`, `gamma=0,01`.

**Modelo final en test:** accuracy 0,9232, F1 macro 0,9342, peor recall 0,871 (`SIRA`). Cumple el criterio propuesto (F1 macro ≥ 0,92 y recall mínimo ≥ 0,85). La regresión logística daba 0,9195, 0,9306 y 0,886.

## Hallazgos
1. **La conclusión del Sprint 2 se corrige.** Comparar solo tres modelos dejó fuera una mejora real (+0,0068 en CV, 5 de 5 pliegues). El diagnóstico acertó al pedir la prueba formal.
2. **La mejora es pequeña** y en test es menor (+0,0036 de F1 macro). Un solo split no la confirma por sí solo.
3. **No toca el punto débil:** `DERMASON` ↔ `SIRA` sigue con 95 errores (94 con la regresión logística) y el recall de `SIRA` baja de 0,886 a 0,871. Mejoran otras clases (`BARBUNYA`: 0,891 → 0,913).
4. **`C=100` está en el borde superior de la grilla.** Podría haber algo de margen; no se amplió para no seguir buscando sobre los mismos datos.
5. **La SVM guardada no tiene `predict_proba`**, así que no hay confianza por predicción. La regresión logística sí.

## Decisiones técnicas

| Decisión | Motivo |
|---|---|
| Guardar el `Pipeline` completo y un JSON de metadata | El escalador debe viajar con el modelo; la metadata deja versiones, hiperparámetros y variables para auditar (TDSP) |
| Versionar el `.joblib` y quitarlo del `.gitignore` | Pesa 413 KB. Es la política recomendada en la bitácora 06 (SM-04) para un modelo pequeño. **Sigue siendo decisión del Scrum Master**; reversible |
| `load_model` avisa si cambia la versión de scikit-learn | `joblib` es sensible a la versión |
| Validación cruzada anidada para SVM y Gradient Boosting | Ajustar y reportar con la misma validación sería optimista |
| Orden de complejidad `logreg` < `svm` < `random_forest` < `hist_gb` | Desempata entre equivalentes. Es un criterio explícito en `src/models.py` y discutible |
| `early_stopping=False` en Gradient Boosting | Con `auto` se activa solo con más de 10.000 filas y cambiaría el protocolo |
| `predict` ignora columnas extra pero rechaza faltantes y nulos | Un CSV con la columna `Class` no debe fallar; un dato incompleto no debe predecirse en silencio |

## Verificación
- `python -m pytest`: **73 pruebas en verde**, 0 omitidas (la suite no necesita red si UCI no responde: las pruebas marcadas `network` se omiten solas).
- Notebook 04 ejecutado de inicio a fin sin errores con scikit-learn 1.9.1. El log muestra el aviso inocuo de limpieza de carpetas temporales de `loky` en Windows, ya descrito en la bitácora 06.
- `python -m src.train` de punta a punta: reproduce **las mismas métricas e hiperparámetros** que el notebook.
- `python -m src.predict` sobre un CSV de prueba: devuelve las clases esperadas.
- **No se hizo** la prueba de reproducibilidad en un clon limpio (clonar, crear el venv y correr todo desde cero).

## Pendientes
- **Product Owner:** validar la elección de la SVM frente a la regresión logística (≈ 0,7 puntos de F1 en CV a cambio de interpretabilidad y de probabilidades) y fijar el criterio numérico de aceptación. `python -m src.train --model logreg` revierte la decisión sin cambiar nada más.
- **Scrum Master:** confirmar que el `.joblib` se versiona; sección 7 del reporte; tablero, dailies y retrospectiva consolidada para el Entregable 3.
- **Todo el equipo:** presentación (láminas de modelado y despliegue), prueba de reproducibilidad en limpio y respuestas a las preguntas 1 a 3.
- **ML Engineer:** adaptar la presentación a la decisión nueva (SVM).

## Retrospectiva (borrador, a completar en equipo)
- **Qué funcionó:** la recomendación del diagnóstico de probar más modelos encontró una mejora que el Sprint 2 no vio; TDD dejó `train` y `predict` cubiertos y el modelo versionado tiene su propia prueba de aceptación.
- **Qué no funcionó:** la mejora real es pequeña y no resuelve `SIRA`; la grilla de la SVM quedó pegada al borde.
- **Qué mejorar:** registrar el criterio de selección *antes* de ver los resultados (aquí ya estaba escrito en el Sprint 2), repetir la comparación con más de un split y definir con el PO el umbral de aceptación desde el principio.
