# Diagnóstico del repositorio y recomendaciones por rol

**Fecha:** 2026-11-14 · **Elaborado desde el rol:** Data Engineer / Analyst · **Base revisada:** `origin/main` (commit `9610221`, con los PR #1, #2 y #3 fusionados)
**Referencias:** [Lab1.pdf](../Lab1.pdf) (rúbrica de 100 puntos, Definition of Done, entregables) y [Plan_Equipos_ScrumML_DryBean.pdf](../Plan_Equipos_ScrumML_DryBean.pdf) (roles, backlog, sprints).

> **Alcance y límites.** Todo lo que sigue se verificó ejecutando el código y los datos de `main` en una copia limpia. No se pudo verificar el tablero de MeisterTask ni lo hablado en la reunión del 12/11 (no hay acta). Los estados "Cubierto / Parcial / Falta" son una lectura de la rúbrica, **no una nota**.

---

## 1. Resumen

El trabajo técnico de los sprints 1 y 2 está sólido y es reproducible. Lo que falta para cerrar bien está casi todo **fuera del código**: la comprensión del negocio, el reporte final, la evidencia Scrum, el modelo guardado y un error de reproducibilidad en el README.

| Criterio de la rúbrica | Pts | Estado | Lo que más pesa |
|---|---:|---|---|
| Aplica correctamente CRISP-DM | 20 | Parcial | Fases 2–5 cubiertas. **Falta la fase 1 (negocio) y la 6 (despliegue)** |
| Organiza con enfoque TDSP | 15 | Parcial | Estructura y trazabilidad bien. Falta política del modelo y reproducibilidad de entorno |
| Evidencia Scrum ML | 15 | Parcial | Backlog y seguimiento hay. Falta tablero exportado, dailies, retro consolidada |
| Código funcional y reproducible | 20 | Parcial | 26 pruebas y 2 notebooks en verde. **README con versión de Python incorrecta**, sin `train.py`/`predict.py` |
| Evaluación del modelo | 15 | Cubierto | Falta un criterio numérico de aceptación y el cruce de errores con el EDA |
| Interpretación y conclusiones | 15 | Parcial | **No existe el reporte breve de 7 secciones**; faltan las preguntas de reflexión 1–3 |

**Prioridad sugerida:** (1) corregir el README, (2) cerrar la aceptación del Sprint 1 con el PO, (3) fase 1 y reporte final, (4) `train.py`/`predict.py` y modelo guardado, (5) evidencia Scrum.

---

## 2. Verificación realizada

| Comprobación | Resultado |
|---|---|
| `python -m pytest` en `main` (con internet) | **26 de 26 en verde**. Sin internet fallan solo las 5 de `test_data_loader.py` (descargan de UCI) |
| Notebook 01 re-ejecutado de inicio a fin | Sin errores |
| Notebook 02 re-ejecutado de inicio a fin | Sin errores en las celdas. El log muestra avisos `KeyError` de limpieza de carpetas temporales de `joblib` al cerrar el `GridSearchCV` paralelo en Windows; son inocuos (código de salida 0 y resultados idénticos) |
| Reproducibilidad de artefactos | Tras re-ejecutar ambos notebooks, **ningún archivo versionado cambió** (datos procesados, CSV de reportes y comparación de modelos idénticos) |
| Métricas del PR #2 recalculadas por separado | Coinciden exactamente (accuracy, F1 macro y CV de los 3 modelos) |
| Datos | 13.611 × 17; 68 duplicados (todos HOROZ); 13.543 limpias; train 10.834 / test 2.709 |
| Python mínimo real | **3.12**: `numpy 2.5.4` exige `>=3.12`. El README dice "3.10 o superior" |

---

## 3. Respuesta a las observaciones del PO sobre el Sprint 1

Cada punto de la [primera revisión del PO](2026-11-13-01_primera_revision_data_engineer_sprint1_PO.md) tiene evidencia en el repo. Esto permite cerrar QA-S1-01, 02 y 03 del seguimiento del Scrum Master.

| # | Prioridad | Observación | Respuesta y evidencia |
|---|---|---|---|
| 1 | Alta | Explicar el cambio de outliers 7.139 → 7.152 | **Explicado abajo.** Falta dejarlo escrito en el notebook 01 |
| 2 | Alta | Matriz de correlación y su interpretación | `outputs/reports/matriz_correlacion.png` y notebook 01 §6 |
| 3 | Alta | Notebook completo sin errores | Re-ejecutado en `main` sin errores (ver §2) |
| 4 | Media | Gráficos de clases y outliers | `distribucion_clases.png`, `histogramas_variables.png`, `boxplots_por_clase.png` |
| 5 | Media | Train/test generados y estratificados | `data/processed/`; diferencia máxima de proporción entre train y test: 0,03 puntos porcentuales (notebook 01 §7) |
| 6 | Media | Alinear la versión de Python del README | **El PO tiene razón: es un error del README.** Debe decir 3.12 o superior |

### Por qué los outliers cambian de 7.139 a 7.152

El cambio neto de +13 es la suma de dos efectos opuestos:

| Paso | Outliers IQR |
|---|---:|
| Datos crudos | 7.139 |
| Se van con los 68 duplicados (35 de ellos eran outliers) | −35 |
| Datos limpios, **con los límites del crudo** | 7.104 |
| Los cuartiles se recalculan sin duplicados y los límites se estrechan | **+48** |
| Datos limpios, con sus propios límites (lo reportado) | **7.152** |

Las columnas que más suben son `Compactness` (+15) y `AspectRatio` (+12); bajan `Eccentricity` (−10) y `ShapeFactor4` (−7). Los 68 duplicados son todos HOROZ y estaban concentrados en la zona central de variables de forma; al quitarlos, `Q1` y `Q3` se mueven en el tercer decimal y algunos puntos quedan fuera. No es un error. Decisión vigente: los outliers **se conservan** porque son mediciones físicas reales de granos.

---

## 4. Lectura de las métricas

| Modelo | Accuracy test | F1 macro test | F1 macro CV (train) |
|---|---:|---:|---:|
| Regresión logística | 0,9195 | 0,9306 | 0,9365 ± 0,0037 |
| Random Forest | 0,9195 | 0,9310 | 0,9343 ± 0,0047 |
| Random Forest ajustado | 0,9192 | 0,9308 | 0,9354 ± 0,0043 |

**Por clase (regresión logística, 218 errores en 2.709):**

| Clase | Precisión | Recall | F1 |
|---|---:|---:|---:|
| BOMBAY | 1,000 | 1,000 | 1,000 |
| HOROZ | 0,964 | 0,944 | 0,954 |
| SEKER | 0,932 | 0,943 | 0,938 |
| CALI | 0,911 | 0,942 | 0,926 |
| DERMASON | 0,927 | 0,907 | 0,917 |
| BARBUNYA | 0,925 | 0,891 | 0,908 |
| **SIRA** | **0,858** | **0,886** | **0,872** |

**Hallazgos para el equipo:**

1. **Los errores no dependen del modelo.** DERMASON↔SIRA son 94 errores con regresión logística y 95 con Random Forest. El techo está en la superposición de las clases, no en el algoritmo ni en sus hiperparámetros.
2. **La confusión DERMASON↔SIRA es de tamaño, no de forma.** `AspectRatio` y `Solidity` son casi iguales en ambas. El 92 % de los DERMASON mal clasificados tiene un `Area` más cercana a la mediana de SIRA (mediana del grupo: 40.544 px² frente a 31.413 de los bien clasificados), y el 78 % de los SIRA mal clasificados está más cerca de la mediana de DERMASON (37.318 px² frente a 44.807).
3. **BARBUNYA→CALI es asimétrico:** 18 errores en un sentido y 8 en el otro (regresión logística; en Random Forest, 17 y 11). El reporte del Sprint 2 dice "17–19 por sentido", lo que no es exacto.
4. **El desbalance se ve en la matriz:** BOMBAY tiene 104 granos de prueba y DERMASON 709; una matriz normalizada por fila es más legible.
5. **Exploración rápida (no incluida en ningún PR):** con la misma validación cruzada sobre train, una **SVM RBF (C=10) da F1 macro 0,9436 ± 0,0049** y un **HistGradientBoosting 0,9421 ± 0,0027**, frente a 0,9365 ± 0,0037 de la regresión logística. La diferencia (+0,006 a +0,007) supera la desviación, así que **con la regla que usó el propio equipo ("diferencia menor que la mayor desviación = equivalentes") no serían equivalentes**. Es un hallazgo orientativo: no se ajustaron hiperparámetros ni se comparó por pliegue. Merece una prueba formal antes de dar por cerrada la elección de la regresión logística.

---

## 5. Entregables y Definition of Done

**Definition of Done del laboratorio (Lab1.pdf):**

| # | Criterio | Estado |
|---|---|---|
| 1 | El notebook corre de inicio a fin sin errores | Cubierto (01 y 02) |
| 2 | El dataset se descarga o carga correctamente | Cubierto |
| 3 | Se reportan nulos y duplicados | Cubierto |
| 4 | Baseline y modelo alternativo | Cubierto |
| 5 | Comparación con accuracy y F1 macro | Cubierto |
| 6 | Matriz de confusión | Cubierto |
| 7 | **Se guarda el modelo final** | **Falta** (Sprint 3) |
| 8 | Se explica el resultado en lenguaje comprensible | Parcial: está en los notebooks, no en un texto para el usuario final |
| 9 | **Se documenta la relación con CRISP-DM, TDSP y Scrum ML** | Parcial: no hay una sección que lo haga explícito |

**Entregables del Lab1.pdf:**

| Entregable | Estado | Pendiente |
|---|---|---|
| 1. Notebook ejecutado | Cubierto | Hay dos notebooks (01 y 02), que juntos cubren todo lo pedido |
| 2. Reporte breve (7 secciones) | **Falta** | Ver §6. Nadie lo ha empezado |
| 3. Evidencia Scrum ML | Parcial | Backlog y seguimiento hay; falta tablero exportado y retrospectiva consolidada |

Preguntas finales de reflexión del PDF: las 4 a 7 están respondidas en el notebook 02 (§10). **Las 1, 2 y 3 no se responden en ningún archivo** (fase más importante de CRISP-DM, ventaja de TDSP, cómo ayuda Scrum ML con resultados inciertos).

---

## 6. Lo que falta desde mi rol (Data Engineer / Analyst)

Ordenado por prioridad. Los puntos 1 a 4 se pueden hacer en una sola rama corta.

| # | Acción | Rúbrica | Esfuerzo |
|---|---|---|---|
| 1 | **Corregir el README:** "Python 3.12 o superior (verificado con 3.13)". Quitar el `.venv312/` duplicado del `.gitignore` | Código reproducible (20) | Minutos |
| 2 | **Añadir al notebook 01 la nota de outliers** de §3 y copiarla a la bitácora | Responde la alerta alta del PO | Minutos |
| 3 | **Pruebas sin internet:** que `test_data_loader.py` use una fixture o un marcador `@pytest.mark.network`, para que `pytest` quede en verde sin conexión (QA-S2-03) | Código reproducible (20) | Bajo |
| 4 | **Análisis de errores cruzado con el EDA** (QA-S2-02): convertir los hallazgos 1 a 4 de §4 en una sección del notebook 02 o en un notebook 03, con gráficas de `Area` por grupo de acierto y error | Evaluación (15), Interpretación (15) | Medio |
| 5 | **Prueba de reproducibilidad en limpio:** clonar en una carpeta nueva, crear el venv, `pytest` y `Restart & Run All`, y registrarlo en la bitácora | Código reproducible (20), TDSP (15) | Bajo |
| 6 | **Redactar las secciones 2 y 3 del reporte** (comprensión de datos y preparación), reutilizando el notebook 01 y el diccionario de datos | Interpretación (15), CRISP-DM (20) | Medio |
| 7 | **Láminas de datos para la presentación:** distribución de clases, calidad, correlaciones y hallazgo de errores | Interpretación (15) | Medio |
| 8 | Aportar a la retrospectiva y responder las preguntas 1 a 3 junto con el resto del equipo | Scrum (15), CRISP-DM (20) | Bajo |

---

## 7. Recomendaciones para los demás roles

### Product Owner
1. **Escribir la sección 1 del reporte (comprensión del negocio).** Hoy no existe en ningún archivo y es la fase 1 de CRISP-DM, que pesa 20 puntos. Debe incluir el problema (control de calidad de una empresa agrícola), el objetivo y los riesgos.
2. **Definir un criterio numérico de aceptación del modelo.** Los PDF piden "decidir si el modelo cumple el objetivo" pero no dan umbral. Propuesta de partida, a ajustar por el PO: F1 macro en test ≥ 0,92 **y** recall mínimo por clase ≥ 0,85. Hoy el modelo da 0,931 y el recall mínimo es 0,886 (SIRA).
3. **Cerrar la aceptación del Sprint 1** con la tabla de §3: todas las alertas tienen evidencia. Conviene que ejecute él mismo `Restart & Run All` con Python 3.12 o superior.
4. **Decidir el modelo final con el resultado de la prueba formal de SVM/Gradient Boosting** (ver ML Engineer). Es una decisión de valor, no solo técnica: +0,6 puntos de F1 a cambio de un modelo menos interpretable.
5. Validar la historia "Como usuario final, quiero entender el resultado": pedir un resumen en lenguaje llano en el reporte (DoD #8).

### Scrum Master
1. **Actualizar el tablero: los tres PR ya están fusionados** (#1 Sprint 1, #2 Sprint 2, #3 el seguimiento del propio Scrum Master). QA-S2-01 queda cerrado. El seguimiento dice "confirmar merge de `feature/modelado`"; ya está hecho.
2. **Corregir el dato de pruebas:** con internet son **26 de 26**; 21 es solo sin red. Ambos números son ciertos, conviene decir ambos.
3. **Preparar la evidencia del Entregable 3** (15 puntos): exportar o capturar el tablero en `Por hacer / En progreso / Hecho`, registrar al menos un daily con la plantilla, y consolidar **una** retrospectiva con los tres puntos pedidos (qué funcionó, qué no, qué mejorar). Hoy hay tres borradores sueltos en tres bitácoras.
4. **Fijar la política de entorno** y comunicarla: Python 3.12 o superior con `requirements.txt`, y ejecutar los notebooks solo con el kernel del `.venv`.
5. **Orden de la bitácora:** el archivo del PO se llama `2026-11-13-01_...` y rompe la convención `AAAA-MM-DD_NN_`. Renumerarlo y evitar colisión con los números 05 y 06.
6. **Política del `.joblib`** (SM-04): recomiendo **versionarlo si el modelo final es la regresión logística** (pesa pocos KB) y **cambiar el `.gitignore`**, que hoy lo excluye. Además, guardar las versiones de Python y scikit-learn junto al modelo, porque `joblib` es sensible a la versión. Si el modelo final fuera un bosque, mejor regenerarlo con `src/train.py`.
7. Completar la sección 7 del reporte (Scrum ML: backlog, sprint review y retrospectiva) y fijar con el equipo las fechas del Sprint 3. No hay fechas en ningún documento.

### ML Engineer
1. **Sprint 3:** `src/train.py`, `src/predict.py` y guardar el **`Pipeline` completo** (escalador más modelo), no solo el clasificador. Si el modelo es la regresión logística, guardar solo el clasificador rompería la predicción porque necesita el escalado.
2. **Probar SVM RBF y Gradient Boosting con el mismo protocolo** (CV sobre train, comparación por pliegue) y reportar el resultado, sea cual sea. Si no mejoran, la elección de la regresión logística queda mucho mejor justificada.
3. **Corregir la frase de BARBUNYA↔CALI** en el notebook 02 (§10) y en el reporte del Sprint 2 (18 y 8 con regresión logística; 17 y 11 con Random Forest).
4. **Exportar el reporte de clasificación por clase** a CSV en `outputs/reports/` y añadir una **matriz de confusión normalizada por fila**. Son las dos evidencias que necesita el PO para fijar umbrales por clase.
5. Probar el Paso 17 y 18 del laboratorio con el modelo cargado: que `predict` sobre una fila coincida con la del modelo en memoria.
6. Redactar las secciones 4 a 6 del reporte (modelado, evaluación y despliegue).

### Todo el equipo
- Responder en conjunto las preguntas finales 1, 2 y 3 del laboratorio.
- Revisar el reporte antes de entregar contra la rúbrica de la sección 1 de este documento.

---

## 8. Orden de ejecución propuesto para el Sprint 3

1. **Ya:** corregir README y `.gitignore` (DE), actualizar el tablero (SM), aceptar el Sprint 1 (PO).
2. **Primero:** `train.py`, `predict.py` y prueba formal SVM/GB (ML); fase 1 del negocio y criterio numérico (PO); pruebas sin red y análisis de errores (DE).
3. **Después:** modelo guardado y política del `.joblib`, y las secciones del reporte por rol (PO 1, DE 2–3, ML 4–6, SM 7).
4. **Al final:** presentación, retrospectiva consolidada, preguntas 1 a 3 y prueba de reproducibilidad en limpio.
