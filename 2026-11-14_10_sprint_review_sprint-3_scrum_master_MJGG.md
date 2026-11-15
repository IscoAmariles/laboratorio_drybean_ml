# Bitácora 10 — Sprint Review | Sprint 3

**Proyecto:** Dry Bean ML  
**Fecha del documento:** 14 de noviembre de 2026  
**Preparado por:** Scrum Master (MJGG)  
**Tipo de registro:** síntesis documental de la revisión del incremento, con base en entregables técnicos y documentos del PO.

## 1. Objetivo

Presentar el incremento final del Sprint 3, contrastarlo con los criterios del Product Owner y dejar constancia de que el modelo recomendado, el modelo seleccionado y el modelo implementado en el repositorio corresponden a **Regresión Logística**.

## 2. Incremento final entregado

| Componente | Evidencia del proyecto | Estado |
|---|---|---|
| Datos limpios y split estratificado | `data/processed/`, notebook 01 y reportes de calidad | Completado |
| Modelos alternativos y evaluación | Notebook 02, `src/models.py`, `src/evaluate.py`, reportes y matrices | Completado |
| Elección del modelo final | Comparación de Accuracy, F1 macro, recall por clase, CV y criterios del PO | **Regresión Logística seleccionada** |
| Entrenamiento final reproducible | `src/train.py` | Implementado para Regresión Logística |
| Artefacto persistido | `outputs/models/modelo_final_drybean.joblib` y `modelo_final_metadata.json` | **Modelo final Regresión Logística** |
| Predicción local | `src/predict.py` y flujo de demostración en notebook | Implementada |
| Pruebas | Suite de pruebas automatizadas; reporte del ML Engineer documenta 73 aprobadas | Documentado |
| Reporte y seguimiento | `docs/reporte/`, `docs/bitacora/`, README y tablero MeisterTask | Documentados |

## 3. Resultado de evaluación del modelo seleccionado

| Métrica | Resultado Logistic Regression | Mínimo exigido por PO | Veredicto |
|---|---:|---:|---|
| Accuracy test | 0,9195 | Métrica informativa | Registrada |
| F1 macro test | **0,9306** | **0,92** | **Cumple** |
| Recall mínimo por clase (`SIRA`) | **0,886** | **0,85** | **Cumple** |
| F1 macro CV sobre train | 0,9365 ± 0,0037 | Complementaria | Registrada |

La Regresión Logística fue recomendada por el ML Engineer y seleccionada por el PO por su equilibrio entre rendimiento, interpretabilidad y facilidad de mantenimiento. Las alternativas Random Forest, SVM RBF y Gradient Boosting permanecen como antecedentes de la comparación experimental; su evaluación no modifica la decisión final.

## 4. Validaciones del Product Owner

- [PO 01 — Comprensión del negocio](01_comprension_del_negocio_PO.md): clasificación de siete variedades a partir de 16 características morfológicas.
- [PO 02 — Criterios](02_criterios_aceptacion_modelo_PO.md): F1 macro en test ≥ 0,92 y recall mínimo ≥ 0,85.
- [PO 03 — Aceptación Sprint 1](03_aceptacion_sprint_1_PO.md): aceptación funcional de los entregables de datos.
- [PO 04 — Decisión](04_decision_modelo_final_PO.md): selección expresa de Regresión Logística en el apartado 4.6.
- [PO 05 — Historia de usuario](05_validacion_historia_usuario_resultado_PO.md): explicación de los resultados aceptada y aprobación del docente registrada por el PO.

Estas evidencias confirman el **cumplimiento de los criterios numéricos** y la aceptación de la historia de explicación. El presente documento sintetiza el incremento técnico; no sustituye un acta adicional firmada de aceptación administrativa del Sprint 3.

## 5. Revisión de Definition of Done

| Elemento | Comprobación de cierre |
|---|---|
| Ingesta y preparación | Datos procesados y partición disponibles |
| Notebook(s) y evaluación | Modelos comparados y documentados |
| Métricas | Accuracy, F1 macro y recall por clase registrados |
| Matriz de confusión | Evidencia de errores por variedad disponible |
| Modelo final guardado | `.joblib` y metadata correspondientes a Regresión Logística |
| Prueba de predicción | Flujo local disponible en `src/predict.py` |
| Explicación del resultado | Historia de usuario aceptada por PO |
| Documentación Scrum y TDSP | Bitácoras, README y sección 7 incluidos |

## 6. Conclusión de la Sprint Review

El incremento final ofrece una solución local de clasificación multiclase con **Regresión Logística**. Los indicadores del modelo cumplen los umbrales definidos por el Product Owner; su elección técnica y de producto es consistente con la implementación documentada en GitHub. La solución es un prototipo académico y no constituye por sí sola una validación para operación comercial en condiciones distintas de las representadas por UCI.
