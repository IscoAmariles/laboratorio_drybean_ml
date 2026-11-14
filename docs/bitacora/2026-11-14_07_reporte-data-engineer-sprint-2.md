# Reporte de ejecución · Data Engineer / Analyst · Sprint 2

**Fecha:** 2026-11-14 · **Rama:** `feature/data-sprint2` · **Plan ejecutado:** [bitácora 06, sección 6](2026-11-14_06_diagnostico-y-recomendaciones-por-rol.md) · **PR:** [#4](https://github.com/IscoAmariles/laboratorio_drybean_ml/pull/4)

## Método
Se fijaron metas con criterio de aceptación verificable (G1 a G6) y el código nuevo se hizo con TDD: primero las pruebas (fase roja), después el mínimo código que las pasa (fase verde). Cada cifra que aparece en un texto está protegida por un `assert` en el notebook que la calcula.

## Resultado por meta

| Meta | Criterio de aceptación | Evidencia | Estado |
|---|---|---|---|
| G1 README correcto | Dice Python ≥ 3.12; sin línea duplicada en `.gitignore` | `README.md`, `.gitignore` | Hecho |
| G2 Outliers explicados | Función probada y sección que reproduce 7.139 → 7.152 | `src/quality.py` (`outlier_shift_breakdown`), notebook 01 §5.1 | Hecho |
| G3 Pruebas sin internet | `pytest` en verde con la red apagada | 35 pruebas en verde y 1 omitida con motivo visible; con internet, 36 | Hecho |
| G4 Análisis de errores | Módulo probado y notebook con gráficas | `src/error_analysis.py`, `notebooks/03_analisis_errores.ipynb`, 4 gráficas y 4 CSV nuevos en `outputs/reports/` | Hecho |
| G5 Reproducible en limpio | Clon nuevo, venv nuevo, pruebas y notebooks en verde | Clon nuevo desde GitHub (commit `1e35517`), venv nuevo con Python 3.13.14 y `pip install -r requirements.txt` sin errores. 36 pruebas en verde con internet; 35 en verde y 1 omitida sin internet. Notebooks 01 (14 celdas), 02 (12) y 03 (8) ejecutados sin errores con el kernel del venv del clon (scikit-learn 1.9.1). **Ningún archivo versionado cambió** tras ejecutarlos. El log del 02 repite los avisos `KeyError` de limpieza de `joblib` ya documentados en la bitácora 06, inocuos | Hecho |
| G6 Reporte y láminas | Secciones 2 y 3, guion de láminas, este reporte | `docs/reporte/`, `docs/presentacion/laminas_datos.md` | Hecho (borradores) |

## Ciclos TDD

| Ciclo | Rojo | Verde |
|---|---|---|
| Descomposición de outliers | `ImportError`: la función no existía | 3 pruebas nuevas; sobre los datos reales reproduce 7.139 → −35 → 7.104 → +48 → 7.152 |
| Análisis de errores | `ModuleNotFoundError` | 7 pruebas nuevas (pares de confusión, cercanía a la mediana, medianas por grupo, métricas por clase) |
| Pruebas sin internet | Con un proxy muerto la prueba real **fallaba** (1 fallo) y el marcador `network` no estaba registrado | `tests/conftest.py` y marcador en `pytest.ini`: 35 en verde y 1 omitida |

Total: **36 pruebas** (26 anteriores + 10 nuevas). La reescritura de `test_data_loader.py` (UCI simulado más una prueba real marcada `network`) mantiene el mismo número de pruebas.

## Hallazgos nuevos

1. **Regresión Logística y Random Forest cometen exactamente los mismos 218 errores** (8,0 % de 2.709) y con el mismo reparto por pares (DERMASON↔SIRA: 94 y 95). Pasar de un modelo lineal a un bosque no cambia el panorama.
2. **Cada par de confusión tiene su propia variable**, medida como la proporción de errores más cercana a la mediana de la clase equivocada: tamaño para DERMASON↔SIRA y DERMASON→SEKER (≥ 78 %), redondez para BARBUNYA→CALI (94 %; el tamaño no ayuda: 44 %), alargamiento para HOROZ→CALI (91 %). SEKER→BARBUNYA no se explica por una sola variable.
3. **Riesgo operativo (inferencia a validar):** el tamaño en píxeles es lo que separa a la pareja más difícil; un cambio de cámara, distancia o resolución degradaría justo esa pareja.
4. **Tres clases quedan por debajo de 0,92 de F1** (DERMASON 0,917, BARBUNYA 0,908, SIRA 0,872), algo que el promedio macro (0,931) oculta.
5. Control de calidad de las gráficas: al revisar visualmente la primera versión se encontró que en `errores_dermason_sira_area.png` las medianas estaban pintadas con los colores cambiados respecto de las curvas (seaborn asignó los colores en otro orden). Se corrigió fijando los colores explícitamente y se volvió a verificar la imagen.

## Respuesta a las acciones de seguimiento

| ID | Acción | Estado |
|---|---|---|
| QA-S1-01 | Explicar el conteo de outliers IQR | Cerrada: notebook 01 §5.1 y sección 2.4 del reporte |
| QA-S1-02 | Mostrar el EDA y ejecutar el notebook 01 | Cerrada: los tres notebooks se ejecutan sin errores (ver G5) |
| QA-S1-03 | Verificar estratificación de train y test | Cerrada: diferencia máxima de proporción 0,03 puntos porcentuales (notebook 01 §7) |
| QA-ENV-01 | Armonizar versiones de Python y kernels | Parcial: README corregido a Python ≥ 3.12. Solo se verificó con 3.13; falta probar con 3.12 |
| QA-S2-02 | Cruzar errores por clase con el EDA | Cerrada: notebook 03 |
| QA-S2-03 | Pruebas de UCI sin depender de internet | Cerrada: marcador `network` y UCI simulado |

## Decisiones técnicas

| Decisión | Motivo |
|---|---|
| Notebook 03 aparte, sin tocar el 02 | El 02 es del ML Engineer; evita conflictos de merge |
| Una sección por archivo en `docs/reporte/` | Cada rol redacta la suya sin conflictos; se consolida al final |
| La prueba de red se omite sola, no se elimina | Sigue verificando el dato real cuando hay internet; `pytest -m network` la ejecuta aparte |
| Guion de láminas en Markdown, no un `.pptx` | El formato final y la plantilla los decide el equipo |

## Pendientes y límites
- **Láminas:** solo existe el guion; falta montarlas en la herramienta de presentación.
- **Python 3.12:** no se pudo probar (en esta máquina solo hay 3.13). El PO ya confirmó que la instalación funciona con 3.12.10.
- **Preguntas finales 1 a 3 del laboratorio:** abajo hay un borrador mío; hay que consolidarlo con el equipo.
- **Fuera de mi rol:** sección 1 del reporte (PO), secciones 4 a 6 (ML Engineer), sección 7 y tablero (Scrum Master), `train.py`/`predict.py` y modelo guardado.

## Aporte a la retrospectiva (borrador)
- **Qué funcionó:** TDD detectó que la prueba de red fallaba justo en el escenario que queríamos cubrir; los `assert` dentro de los notebooks evitaron que el texto y los datos se desincronizaran; revisar las gráficas a ojo encontró un error de colores que ninguna prueba habría visto.
- **Qué no funcionó:** mi README del Sprint 1 declaraba una versión de Python que nunca verifiqué contra las dependencias.
- **Qué mejorar:** comprobar `Requires-Python` de las dependencias al fijar versiones, y probar en un clon limpio antes de dar un entregable por cerrado.

## Borrador de respuestas a las preguntas 1 a 3 del laboratorio (a consolidar en equipo)
1. **¿Qué fase de CRISP-DM fue más importante?** La **preparación de los datos** (fase 3). Quitar 68 duplicados antes de dividir y estratificar el split determinó que las métricas fueran creíbles; con duplicados repartidos entre train y test, el F1 se habría inflado. La evaluación (fase 5) vino después a mostrar que el límite del modelo está en el solapamiento de clases.
2. **¿Qué ventaja ofrece TDSP frente a archivos desordenados?** Reproducibilidad. Con datos crudos separados de los procesados, código en `src/`, pruebas y bitácora, cualquiera pudo regenerar los resultados (el PO ejecutó el proceso con otro Python) y detectar discrepancias, como el kernel de Anaconda que cambiaba las métricas.
3. **¿Cómo ayuda Scrum ML cuando el resultado del modelo es incierto?** Los sprints cortos con revisión permiten tratar un resultado inesperado como información y no como fracaso: Random Forest no superó al baseline y eso se decidió con evidencia (validación cruzada) en una revisión, en lugar de descubrirse al final. La regla "desarrollado ≠ aceptado" evita cerrar tarjetas antes de verificar.
