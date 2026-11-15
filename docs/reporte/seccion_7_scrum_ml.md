# Sección 7 — Scrum ML: backlog, Sprint Review y retrospectiva

**Responsable:** Scrum Master (MJGG)  
**Fecha de consolidación:** 14 de noviembre de 2026  
**Modelo final del proyecto:** **Regresión Logística**.

## 7.1 Aplicación de CRISP-DM, TDSP y Scrum ML

El proyecto desarrolla un prototipo para clasificar siete variedades de frijol seco con 16 características morfológicas. Se integraron tres metodologías complementarias:

- **CRISP-DM:** definió las fases de comprensión del negocio, comprensión de los datos, preparación, modelado, evaluación y despliegue local.
- **TDSP:** aportó la estructura del repositorio (`data/`, `notebooks/`, `src/`, `tests/`, `outputs/`, `docs/`), el control de versiones, el registro de experimentos y la reproducibilidad.
- **Scrum ML:** organizó roles, Product Backlog, sprints, revisiones, entregables y Definition of Done con seguimiento en MeisterTask y evidencias en GitHub.

## 7.2 Roles y responsabilidades

| Rol | Responsabilidad en el proyecto |
|---|---|
| **Product Owner** | Definió objetivo, alcance, umbrales cuantitativos; aceptó entregables de datos y la historia de explicación; seleccionó Regresión Logística. |
| **Scrum Master** | Coordinó el tablero y el seguimiento, facilitó la comunicación entre roles, registró avances, revisiones, riesgos y retrospectiva. |
| **Data Engineer / Analyst** | Cargó y depuró los datos, realizó EDA, preparó train/test y estudió errores y variables del dataset. |
| **ML Engineer** | Entrenó modelos alternativos, evaluó métricas, recomendó Regresión Logística, generó el modelo final y el flujo de predicción. |

## 7.3 Product Backlog y entregables

| Historia | Líder de ejecución | Evidencia / resultado |
|---|---|---|
| PB-01 — Descargar datos | Data Engineer | Fuente UCI, datos originales y módulo de carga. |
| PB-02 — Calidad y preparación | Data Engineer | Dataset limpio, EDA, split estratificado, notebook 01. |
| PB-03 — Entrenar Regresión Logística | ML Engineer | Baseline, métricas y modelo final seleccionado. |
| PB-04 — Entrenar Random Forest | ML Engineer | Modelo alternativo y comparación. |
| PB-05 — Comparar modelos | ML Engineer, con decisión PO | F1 macro, recall por clase, Accuracy, CV y matrices; **elección final: Regresión Logística**. |
| PB-06 — README y documentación | Equipo, coordinación Scrum Master | README, reporte por secciones, bitácoras y presentación. |
| Sprint 3 — Despliegue local | ML Engineer | `src/train.py`, `src/predict.py`, `.joblib` y metadata de **Regresión Logística**. |

## 7.4 Ejecución de los sprints

**Sprint 1 — Comprensión y preparación.** Se trabajó con las 13.611 observaciones originales (16 atributos y `Class`). Tras retirar 68 duplicados quedaron 13.543 registros; se preparó el split estratificado 80/20: 10.834 observaciones de entrenamiento y 2.709 de prueba. El PO documentó su aceptación funcional en [PO 03](../bitacora/03_aceptacion_sprint_1_PO.md).

**Sprint 2 — Modelado y evaluación.** Se entrenaron Regresión Logística y Random Forest; posteriormente se examinaron alternativas complementarias. Se compararon las métricas en test y validación cruzada sobre entrenamiento, y se interpretaron matrices de confusión. La recomendación de modelo final fue **Regresión Logística**.

**Sprint 3 — Despliegue y documentación.** Se implementó el entrenamiento reproducible, persistencia del pipeline con `joblib`, metadata del modelo, predicción local y pruebas. La versión final del repositorio entrega **Regresión Logística** como modelo seleccionado. El reporte técnico del Sprint 3 documentó una suite de 73 pruebas aprobadas, y el equipo integró el informe y las evidencias Scrum.

## 7.5 Criterios del Product Owner y selección del modelo

El PO estableció en [PO 02](../bitacora/02_criterios_aceptacion_modelo_PO.md) **F1 macro test ≥ 0,92** y **recall mínimo por clase ≥ 0,85**; en [PO 04](../bitacora/04_decision_modelo_final_PO.md), apartado 4.6, seleccionó Regresión Logística y en [PO 05](../bitacora/05_validacion_historia_usuario_resultado_PO.md) aceptó la historia de usuario relacionada con la explicación del resultado.

| Indicador | Resultado Regresión Logística | Criterio | Evaluación |
|---|---:|---:|---|
| Accuracy test | 0,9195 | Descriptivo | Reportado |
| **F1 macro test** | **0,9306** | **≥ 0,92** | **Cumple** |
| **Recall mínimo (`SIRA`)** | **0,886** | **≥ 0,85** | **Cumple** |
| F1 macro CV train | 0,9365 ± 0,0037 | Complementario | Reportado |

La decisión final equilibra desempeño, simplicidad, interpretabilidad y mantenimiento. Se conservaron las comparaciones con Random Forest, SVM RBF y Gradient Boosting como evidencia de experimentación. El hecho de que alguna alternativa alcanzara una puntuación superior no contradice la selección multicriterio realizada por los roles responsables.

## 7.6 Sprint Review y Definition of Done

La [Sprint Review](../bitacora/2026-11-14_10_sprint_review_sprint-3_scrum_master_MJGG.md) recoge el incremento final: datos preparados, notebook de modelado, métricas, matrices de confusión, pipeline de Regresión Logística persistido, predicción local, resultados interpretados y documentación. La historia de explicación de resultados fue aceptada por el PO.

La **Definition of Done** se abordó a través de código funcional, pruebas, reportes, comparación de alternativas, una predicción reproducible y documentación de CRISP-DM, TDSP y Scrum ML. El cierre descrito corresponde al incremento técnico y documental; las firmas o actas adicionales de reuniones se mantienen en sus fuentes originales cuando existen.

## 7.7 Retrospectiva

La [retrospectiva](../bitacora/2026-11-14_11_retrospectiva_sprint-3_scrum_master_MJGG.md) sintetiza fortalezas (pruebas, organización de datos, seguimiento por roles, criterios cuantitativos) y dificultades (entornos distintos, dependencia de internet, colinealidad y comparación de múltiples alternativas). Como mejoras se proponen automatizar pruebas en PR, validar desde un clon limpio, mantener una ficha única de modelo y enlazar cada tarjeta Scrum con su evidencia.

## 7.8 Conclusión

La combinación de **CRISP-DM, TDSP y Scrum ML** permitió producir un modelo de clasificación con trazabilidad desde el objetivo del producto hasta su ejecución local. El proyecto finaliza con **Regresión Logística** como recomendación del ML Engineer, selección del Product Owner y modelo implementado en GitHub, cumpliendo los dos criterios cuantitativos establecidos por el PO.
