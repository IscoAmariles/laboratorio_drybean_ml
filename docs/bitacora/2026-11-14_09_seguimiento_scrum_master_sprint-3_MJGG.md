# Bitácora 09 — Seguimiento Scrum Master | Sprint 3

**Proyecto:** Laboratorio de Machine Learning — Dry Bean Dataset  
**Fecha de corte:** 14 de noviembre de 2026  
**Rol responsable:** Scrum Master (MJGG)  
**Sprint:** 3 — Despliegue y documentación  
**Herramientas de seguimiento:** MeisterTask y GitHub  
**Estado del incremento:** desarrollo y documentación del Sprint 3 finalizados; modelo final: **Regresión Logística**.

## 1. Objetivo

Consolidar el estado de las historias y entregables al cierre del proyecto, documentar las contribuciones de los cuatro roles y relacionar el tablero Scrum con la evidencia técnica y los criterios definidos por el Product Owner (PO).

## 2. Responsabilidades del equipo

| Rol | Responsabilidad | Evidencia |
|---|---|---|
| Product Owner | Define el alcance y los criterios de aceptación; valida el resultado y selecciona el modelo final. | Documentos [PO 01–05](01_comprension_del_negocio_PO.md), especialmente [PO 02](02_criterios_aceptacion_modelo_PO.md), [PO 04](04_decision_modelo_final_PO.md) y [PO 05](05_validacion_historia_usuario_resultado_PO.md). |
| Scrum Master | Coordina los sprints, facilita seguimiento y revisiones, registra impedimentos y mantiene bitácoras/MeisterTask. | Bitácoras [05](2026-11-13_05_seguimiento_scrum_master_sprint-2_MJGG.md), 09, 10 y 11. |
| Data Engineer / Analyst | Ingesta, calidad, limpieza, EDA y soporte a interpretación de errores. | [Reporte Sprint 1](2026-11-11_02_reporte-sprint-1.md), [reporte Data Engineer Sprint 2](2026-11-14_07_reporte-data-engineer-sprint-2.md) y datos procesados. |
| ML Engineer | Modelado, evaluación, comparación de alternativas, entrenamiento final y predicción. | [Reporte Sprint 2](2026-11-12_04_reporte-sprint-2.md), módulos `src/`, notebooks y reporte técnico de Sprint 3. |

## 3. Avances acumulados por sprint

| Sprint | Objetivo | Resultado |
|---|---|---|
| **Sprint 1 — Datos** | Comprensión, calidad y preparación. | Dataset de 13.611 registros; 68 duplicados retirados; 13.543 registros limpios; partición estratificada 10.834 train / 2.709 test; EDA y notebook 01. Aceptación funcional del PO documentada en [PO 03](03_aceptacion_sprint_1_PO.md). |
| **Sprint 2 — Modelado** | Entrenar y comparar alternativas. | Regresión Logística, Random Forest y variantes; F1 macro y accuracy, matriz de confusión, validación cruzada y análisis por clase. Recomendación de **Regresión Logística**. |
| **Sprint 3 — Entrega** | Entrenar, guardar y utilizar el modelo final; documentar. | **Regresión Logística** integrada como modelo final en GitHub, pipeline guardado en `.joblib` con metadata, predicción local implementada, pruebas y documentación del proyecto. |

## 4. Seguimiento del Product Backlog

| ID | Entregable | Responsable de ejecución | Validación / estado |
|---|---|---|---|
| PB-01 | Ingesta del Dry Bean Dataset. | Data Engineer | Desarrollado; aceptación funcional PO Sprint 1. |
| PB-02 | Calidad, exploración y preparación. | Data Engineer | Desarrollado; aceptación funcional PO Sprint 1. |
| PB-03 | Baseline con Regresión Logística. | ML Engineer | Completado; base del modelo final. |
| PB-04 | Random Forest como alternativa. | ML Engineer | Completado y comparado. |
| PB-05 | Comparación, métricas y elección. | ML Engineer; decisión PO | Completado: **Regresión Logística**, alineada con la decisión PO. |
| PB-06 | README, informes y entrega. | Equipo; coordinación Scrum Master | Documentación del proyecto y sección Scrum ML consolidada. |
| S3-01 | Persistencia del modelo. | ML Engineer | **Regresión Logística** guardada como modelo final; metadata asociada. |
| S3-02 | Predicción local. | ML Engineer | Función de carga/predicción preparada para el modelo final. |
| SM-S3 | Seguimiento, review y retrospectiva. | Scrum Master | Documentadas en bitácoras 09–11 y [sección 7](../reporte/seccion_7_scrum_ml.md). |

## 5. Modelo final y criterios de aceptación

La recomendación del ML Engineer y la selección del Product Owner **coinciden en Regresión Logística**. La decisión prioriza un desempeño satisfactorio en las siete clases, facilidad de interpretación y mantenimiento, sin confundir mejora numérica marginal con valor operativo del producto.

| Métrica | Regresión Logística | Criterio PO | Resultado |
|---|---:|---:|---|
| Accuracy (test) | 0,9195 | Descriptivo | Reportado |
| **F1 macro (test)** | **0,9306** | **≥ 0,92** | **Cumple** |
| **Recall mínimo por clase (`SIRA`)** | **0,886** | **≥ 0,85** | **Cumple** |
| F1 macro CV (train) | 0,9365 ± 0,0037 | Complementario | Reportado |

Evidencia: [reporte de modelado Sprint 2](2026-11-12_04_reporte-sprint-2.md), [comparación de modelos](../../outputs/reports/comparacion_modelos.csv) y [métricas por clase de Regresión Logística](../../outputs/reports/metricas_por_clase_logreg.csv). La decisión del PO se recoge en [PO 04](04_decision_modelo_final_PO.md), y la explicación del resultado fue aceptada en [PO 05](05_validacion_historia_usuario_resultado_PO.md).

## 6. Gestión Scrum y Definition of Done

- **MeisterTask:** visualización de responsables, prioridades y estados `Por hacer`, `En progreso`, `En revisión` y `Hecho`.
- **GitHub:** trazabilidad técnica de notebooks, código, pruebas, reportes, bitácoras, ramas y Pull Requests.
- **Definition of Done:** dataset preparado, modelos evaluados, comparación documentada, matriz de confusión, modelo final persistido, predicción local y explicación comprensible del resultado.
- **Validación del PO:** los criterios de F1 macro y recall mínimo se cumplen; la historia de usuario de explicación de resultados fue aceptada por el PO.

## 7. Cierre de seguimiento

El **cierre técnico y documental del Sprint 3** presenta un único modelo final, **Regresión Logística**, consistente entre la recomendación del ML Engineer, la decisión de producto y el modelo entregado en GitHub. Se conservan los experimentos alternativos como parte de la trazabilidad del trabajo; no cambian la selección final. La [Sprint Review](2026-11-14_10_sprint_review_sprint-3_scrum_master_MJGG.md) y la [retrospectiva](2026-11-14_11_retrospectiva_sprint-3_scrum_master_MJGG.md) complementan este registro.
