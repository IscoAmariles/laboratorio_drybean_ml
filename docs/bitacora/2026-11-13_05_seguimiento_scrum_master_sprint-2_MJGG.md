# Bitácora 05 - Seguimiento Scrum Master | Sprint 2

**Proyecto:** Laboratorio Dry Bean ML  
**Fecha de elaboración:** 2026-11-13  
**Rol:** Scrum Master  
**Sprint actual:** Sprint 2 - Modelado y evaluación  
**Tablero:** MeisterTask - Dry Bean ML | Scrum - CRISP-DM + TDSP  
**Naturaleza del documento:** seguimiento elaborado a partir de las bitácoras técnicas y la revisión del Product Owner. **No es un acta de decisiones verbales confirmadas** de la reunión del 12/11/2026.

## 1. Objetivo del seguimiento

Consolidar el estado de avance de las historias PB-01 a PB-06, visibilizar entregables, PR y dependencias, evitar el cierre prematuro de tarjetas y preparar la revisión de Sprint 2 con el Product Owner.

## 2. Fuentes revisadas

- `2026-11-11_01_plan-data-engineer.md` - plan del Data Engineer.
- `2026-11-11_02_reporte-sprint-1.md` - reporte técnico del Sprint 1.
- `2026-11-12_03_plan-ml-engineer_JHE.md` - plan del ML Engineer.
- `2026-11-12_04_reporte-sprint-2.md` - reporte técnico del Sprint 2.
- `2026-11-13-01_primera_revision_data_engineer_sprint1_PO.md` - revisión parcial del Product Owner.

Los resultados técnicos se reproducen **según lo reportado** en estas fuentes; este documento no afirma que la Scrum Master haya ejecutado independientemente los notebooks ni verificado el estado real de los PR.

## 3. Estado general de los sprints

| Sprint | Estado de ejecución reportado | Estado de aceptación | Observación |
|---|---|---|---|
| Sprint 1 - Comprensión y preparación | Desarrollo del Data Engineer reportado como ejecutado | **En revisión por PO** | Evidencias y observaciones pendientes |
| Sprint 2 - Modelado y evaluación | ML Engineer reporta funcionalidades y métricas generadas | **En revisión de PR/PO** | Confirmar merge de `feature/modelado` y aceptación |
| Sprint 3 - Despliegue y documentación | Planificado | No iniciado formalmente según reportes | No declarar entregas de `joblib` completadas |

### Resultados relevantes del Sprint 1

- Datos originales: **13.611 registros**, 17 columnas, sin nulos.
- Duplicados eliminados: **68** (reportados en clase `HOROZ`); registros limpios: **13.543**.
- Entrenamiento: **10.834**; prueba: **2.709**, con partición estratificada 80/20 y `random_state=42`.
- **15 pruebas automatizadas aprobadas** según la revisión del PO.
- El PO solicita revisar el cambio de conteo IQR (**7.139 → 7.152**), la matriz de correlaciones, los gráficos, el notebook completo, los archivos del split y la compatibilidad de Python.

### Resultados relevantes del Sprint 2

| Modelo | Accuracy test | F1 macro test | F1 macro CV (train, 5 folds) |
|---|---:|---:|---:|
| Regresión logística | 0,9195 | 0,9306 | 0,9365 ± 0,0037 |
| Random Forest | 0,9195 | 0,9310 | 0,9343 ± 0,0047 |
| Random Forest ajustado | 0,9192 | 0,9308 | 0,9354 ± 0,0043 |

- El ML Engineer **recomienda Regresión Logística** por desempeño parecido y menor complejidad. La aceptación por el PO se considera pendiente hasta revisión.
- Principales confusiones reportadas: `DERMASON` ↔ `SIRA` (**94 de 218 errores** en regresión logística) y `BARBUNYA` ↔ `CALI`.
- Evidencias referidas: `notebooks/02_modelado_evaluacion.ipynb`, `outputs/reports/comparacion_modelos.csv`, `matriz_confusion_logreg.png`, `matriz_confusion_rf.png`.
- Pruebas: **21 en verde** al excluir cinco pruebas de `tests/test_data_loader.py` que requieren red y fallaron sin conexión (`ConnectionError`). No reportar como 26/26 aprobadas.
- Incidencia corregida en notebook 02: kernel de Anaconda con versión de scikit-learn diferente al entorno `.venv`. Pendiente estandarizar instrucciones para el equipo.

## 4. Tablero de Product Backlog

Regla de trabajo recomendada: **desarrollado ≠ aceptado**. La columna `En revisión` permite conservar el progreso técnico sin afirmar que el criterio de aceptación y la revisión por PR ya finalizaron.

| ID | Historia | Responsable | Sprint | Columna al 13/11 | Motivo |
|---|---|---|---|---|---|
| PB-01 | Descargar dataset / ingesta | Data Engineer | 1 | En revisión | Reportada como hecha; PO todavía no acepta Sprint 1 completamente |
| PB-02 | Calidad y análisis exploratorio | Data Engineer | 1 | En revisión | PO solicita evidencias de EDA, outliers y notebook |
| PB-03 | Logistic Regression | ML Engineer | 2 | En revisión | Métricas reportadas; falta constancia de PR mergeado y validación |
| PB-04 | Random Forest | ML Engineer | 2 | En revisión | Métricas reportadas; falta constancia de PR mergeado y validación |
| PB-05 | Comparar y seleccionar modelo | ML Engineer lidera / equipo | 2 | En revisión | Decisión documentada; PO debe revisar |
| PB-06 | README profesional | Scrum Master coordina / equipo contribuye | 3 (iniciado antes) | En progreso | Borrador existente; falta completar y alinear entorno |

**Importante:** los reportes individuales etiquetan PB-01/PB-02 y PB-03/PB-04/PB-05 como "Hecho" desde la perspectiva de desarrollo. El tablero de coordinación las mantiene "En revisión" por las verificaciones y PR que todavía no constan como cerrados. Ajustar el estado cuando lleguen evidencias de aceptación/merge.

## 5. Bloqueos, riesgos y acciones de seguimiento

| ID seguimiento | Acción | Responsable propuesto | Prioridad | Evidencia para cerrar |
|---|---|---|---|---|
| QA-S1-01 | Explicar conteo de outliers IQR antes y después | Data Engineer | Alta | Nota técnica revisada por PO |
| QA-S1-02 | Mostrar EDA completo y ejecutar notebook 01 | Data Engineer / PO | Alta | Gráficos e interpretación revisados; `Restart & Run All` verificado |
| QA-S1-03 | Verificar la estratificación de train/test y artefactos | Data Engineer / PO | Media | Conjunto train/test aceptado |
| QA-ENV-01 | Armonizar versiones Python, librerías y kernels | DE + ML Engineer; coordina SM | Alta | README e instalación reproducibles |
| QA-S2-01 | Revisar y fusionar PR `feature/modelado` | Equipo; coordina SM | Alta | PR aprobado/mergeado a `main` |
| QA-S2-02 | Cruzar errores por clase con el EDA | Data Engineer | Media | Interpretación documentada |
| QA-S2-03 | Verificar tests UCI con red o fixtures adecuados | Data Engineer + ML Engineer | Media | Ejecución documentada y explicación de pruebas dependientes de red |
| SM-04 | Acordar versionado del `.joblib` | SM coordina; decisión colectiva | Media | Acuerdo y README/.gitignore actualizados |

**Fechas límite:** por acordar con el equipo. No se fijan fechas ficticias en esta bitácora.

## 6. Decisiones pendientes de aprobación

1. Aceptación definitiva de PB-01 y PB-02 por el PO una vez vistas todas las evidencias.
2. Revisión y merge de `feature/modelado` antes de cerrar PB-03, PB-04 y PB-05.
3. Aprobación de la elección de Regresión Logística como modelo final.
4. Entorno Python/scikit-learn de referencia para todo el equipo.
5. Política de inclusión de `.joblib` en GitHub, o regeneración por `src/train.py`.
6. Fecha de la revisión final del Sprint 2 y planificación de Sprint 3.

## 7. Acuerdos/acciones para validar tras reunión del 12/11/2026

**Advertencia:** se informó que hubo reunión el 12/11, pero no se aportaron notas literales ni lista de asistentes. Los siguientes puntos son **propuestas para confirmar**, no acuerdos ya tomados.

- [ ] Pedir al PO requisitos exactos para cerrar PB-01/PB-02.
- [ ] Solicitar al equipo revisión de PR `feature/modelado`.
- [ ] Confirmar si el ML Engineer ya completó todos los artefactos mencionados en el reporte del Sprint 2.
- [ ] Solicitar al Data Engineer análisis de confusiones por clase e integración con EDA.
- [ ] Definir política de versión Python y dependencias para la instalación común.
- [ ] Completar asistencia, acuerdos, responsables y fechas de la reunión.

## 8. Sprint review - lista de comprobación para la Scrum Master

- [ ] El PO revisó criterios de PB-01 y PB-02.
- [ ] El PR del Data Engineer está revisado y mergeado en main (verificar).
- [ ] El notebook 02 abre y corre de principio a fin en el entorno declarado.
- [ ] Se muestran Accuracy, F1 macro y CV sobre train para los tres modelos.
- [ ] El equipo explica por qué selecciona regresión logística.
- [ ] Se revisan matrices de confusión y principales errores por clase.
- [ ] Se registra la revisión y merge del PR del ML Engineer.
- [ ] Se actualizan estados de MeisterTask con enlaces de evidencia.
- [ ] Se acuerda cuándo inicia/cierra Sprint 3.

## 9. Retrospectiva del Sprint 2 (borrador a debatir)

### Qué funcionó (hallazgos técnicos reportados)
- La CV sobre train permitió comparar modelos sin basar la selección en diferencias mínimas del test.
- El enfoque TDD dejó pruebas de `src/models.py` y `src/evaluate.py`.
- La preparación del Sprint 1 proporcionó archivos train/test reutilizables.

### Dificultades reportadas
- Diferencia entre kernel de Anaconda y `.venv` produjo métricas diferentes.
- Pruebas de descarga de UCI requieren conexión a internet.
- El PO solicita evidencias adicionales para aprobar plenamente el Sprint 1.

### Propuestas de mejora (a validar en equipo)
- Congelar/registrar versiones de Python y dependencias en notebooks y README.
- Separar claramente en MeisterTask `En revisión` y `Hecho`.
- Adjuntar en cada tarjeta enlace al PR y al archivo de evidencia.
- Decidir cómo probar carga de datos sin depender de internet.

## 10. Plan inmediato de la Scrum Master

1. Importar `meistertask_drybean_sprints_1_2_3.csv` en MeisterTask; asignar responsables manualmente y comprobar cada tarjeta.
2. Compartir el tablero y solicitar a cada responsable que verifique estado/evidencia.
3. Convertir los puntos pendientes de Sprint 1 en tareas específicas sin ocultarlos bajo PB-01/PB-02.
4. Coordinar revisión del PR `feature/modelado` y aceptación del PO.
5. Actualizar esta bitácora tras confirmar el acta y las decisiones, y añadir enlaces reales a las tarjetas.

---

**Control de cambios:** versión inicial elaborada el 2026-11-13 a partir de los cinco archivos recibidos; registrar a continuación fecha, persona y resumen de cada corrección posterior.
