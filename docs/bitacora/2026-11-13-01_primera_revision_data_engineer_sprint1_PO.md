# Primera revisión del Data Engineer — Sprint 1

**Proyecto:** Laboratorio de Machine Learning — Dry Bean Dataset  
**Revisor:** Product Owner (PO)  
**Rol revisado:** Data Engineer / Analyst  
**Alcance:** Primera revisión de los entregables de comprensión y preparación de datos (CRISP-DM), con énfasis en PB-01 y PB-02.  
**Estado de esta revisión:** **Revisión parcial; aceptación final pendiente de completar evidencias.**

---

## 1. Objetivo de la revisión

Como Product Owner, esta revisión busca comprobar que los entregables de preparación y calidad de los datos cumplen los criterios acordados para el Sprint 1 y que el conjunto de datos queda listo para el trabajo de modelado del Sprint 2.

La revisión se basa únicamente en las evidencias compartidas hasta el momento: resultados de pruebas automatizadas, ejecución del proceso de preparación y fragmentos del notebook `01_comprension_preparacion_datos.ipynb`.

## 2. Evidencias verificadas

### 2.1. Pruebas automatizadas

Se ejecutó:

```powershell
python -m pytest
```

Resultado observado:

- **15 pruebas aprobadas.**
- No se reportaron pruebas fallidas.
- Se ejecutaron pruebas relacionadas con carga de datos, preparación, preprocesamiento y calidad.

**Observación del PO:** es una señal positiva de que las funciones cubiertas por las pruebas responden como se espera. Sin embargo, aprobar las pruebas no sustituye la revisión de todos los entregables funcionales del Sprint 1.

### 2.2. Ejecución de preparación del conjunto de datos

Se ejecutó:

```powershell
python -m src.make_dataset
```

Resultado observado:

| Indicador | Resultado |
|---|---:|
| Filas crudas | 13.611 |
| Duplicados eliminados | 68 |
| Filas limpias | 13.543 |
| Filas de entrenamiento | 10.834 |
| Filas de prueba | 2.709 |

**Observación del PO:** las cantidades son coherentes con una eliminación de 68 registros duplicados y una partición aproximada de 80/20. La ejecución del proceso terminó correctamente.

### 2.3. Revisión del encabezado del notebook

Se revisó el encabezado de `01_comprension_preparacion_datos.ipynb`.

Puntos positivos observados:

- Identifica el rol Data Engineer / Analyst y el Sprint 1.
- Relaciona el notebook con PB-01 (ingesta) y PB-02 (calidad de datos).
- Ubica las actividades dentro de las fases de comprensión y preparación de CRISP-DM.
- Describe la separación de datos crudos, procesados, reportes, código reutilizable y pruebas, alineada con TDSP.

**Observación del PO:** la estructura y el propósito están bien identificados. Queda pendiente comprobar el contenido y la ejecución integral del notebook.

## 3. Revisión del resumen de calidad — PB-02

El notebook presenta el siguiente resumen:

| Métrica | Datos crudos | Datos limpios |
|---|---:|---:|
| Filas | 13.611 | 13.543 |
| Columnas | 17 | 17 |
| Nulos totales | 0 | 0 |
| Duplicados | 68 | 0 |
| Outliers detectados con IQR | 7.139 | 7.152 |

### Hallazgos positivos

1. El conjunto crudo contiene 13.611 filas y 17 columnas.
2. No se reportan valores nulos en los datos crudos ni en los limpios.
3. Se identifican 68 duplicados y el conjunto limpio queda sin duplicados.
4. El número de filas limpias (13.543) coincide con el resultado de `src.make_dataset`.
5. Se mantienen las 17 columnas en el conjunto limpio.

### Observación que requiere aclaración: outliers

El conteo de valores atípicos calculado con IQR pasa de 7.139 en los datos crudos a 7.152 en los datos limpios.

Esto no demuestra por sí solo un error: al retirar duplicados pueden cambiar los cuartiles y los límites del IQR. Sin embargo, el equipo debe explicar brevemente por qué cambia el conteo y confirmar que los valores atípicos se conservan o tratan según una decisión documentada.

**Criterio del PO:** no se solicita eliminar automáticamente todos los outliers. En este dataset pueden corresponder a mediciones físicas reales de los granos. Se solicita justificar la decisión adoptada.

## 4. Revisión de la distribución de clases

El resumen de clases compartido muestra:

| Variedad | Crudo | Limpio |
|---|---:|---:|
| DERMASON | 3.546 | 3.546 |
| SIRA | 2.636 | 2.636 |
| SEKER | 2.027 | 2.027 |
| HOROZ | 1.928 | 1.860 |
| CALI | 1.630 | 1.630 |
| BARBUNYA | 1.322 | 1.322 |
| BOMBAY | 522 | 522 |

Hallazgos:

- Se conservan las siete variedades.
- La reducción de 68 registros corresponde a la clase HOROZ.
- Las demás clases mantienen la misma cantidad de registros.
- Existe desbalance entre clases: DERMASON tiene 3.546 registros y BOMBAY 522.

**Observación del PO:** es razonable considerar F1 Macro como métrica principal para comparar modelos, porque permite evaluar el desempeño por clase y no favorece únicamente a las clases más numerosas. Esta decisión debe mantenerse y explicarse en el Sprint 2.

## 5. Revisión de las conclusiones del Sprint 1

Las conclusiones compartidas indican que:

- El dataset carga sin errores: 13.611 filas × 17 columnas.
- Se eliminan 68 duplicados y quedan 13.543 filas limpias.
- No se detectan nulos.
- Se identifica desbalance entre las siete clases.
- Se reporta colinealidad alta entre algunas variables.
- Se realiza una partición 80/20 estratificada con semilla 42.
- Los datos quedan preparados para el Sprint 2.

**Valoración del PO:** las conclusiones son coherentes con los resultados de preparación y calidad compartidos. La distribución de clases respalda la elección de F1 Macro. No obstante, las afirmaciones sobre correlaciones, EDA y partición deben contrastarse con sus gráficos, código y archivos generados antes de dar por cerrada la aceptación.

## 6. Observación de reproducibilidad del entorno

Durante la instalación de dependencias se encontró una incompatibilidad entre la versión de Python indicada en las instrucciones del proyecto y las versiones fijadas en `requirements.txt`.

- Con Python 3.11.9 no fue posible instalar el conjunto completo de dependencias fijadas.
- Con Python 3.12.10 la instalación terminó correctamente.
- El entorno usado para ejecutar las pruebas y preparar los datos fue `.venv312`.

**Recomendación del PO:** actualizar el README para indicar claramente la versión mínima de Python compatible con las dependencias actuales, o ajustar las versiones de dependencias si el proyecto realmente debe admitir Python 3.10 o 3.11. La instrucción de instalación debe poder reproducirse por otro integrante del equipo.

## 7. Acciones solicitadas al equipo

| Prioridad | Acción | Motivo |
|---|---|---|
| Alta | Explicar el cambio en el conteo de outliers IQR después de eliminar duplicados. | Trazabilidad de la decisión de calidad. |
| Alta | Compartir y revisar la matriz de correlación/heatmap y su interpretación. | Verificar las conclusiones del EDA. |
| Alta | Confirmar que el notebook completo ejecuta de principio a fin sin errores. | Comprobar reproducibilidad del entregable. |
| Media | Mostrar los gráficos de distribución de clases y el análisis de valores atípicos. | Completar la evidencia del análisis exploratorio. |
| Media | Confirmar que los archivos de train y test se generan correctamente y que la partición es estratificada. | Validar el entregable de preparación. |
| Media | Alinear la versión de Python del README con `requirements.txt`. | Facilitar la instalación reproducible del proyecto. |

## 8. Aspectos pendientes de verificar por el PO

A la fecha de esta primera revisión, todavía no se ha comprobado:

- La ejecución completa del notebook con **Restart & Run All**.
- Los gráficos y las interpretaciones completas del EDA.
- La matriz de correlación y el análisis de multicolinealidad.
- El análisis visual y la justificación del tratamiento de outliers.
- La existencia y contenido de todos los archivos de datos y reportes esperados.
- Los resultados de entrenamiento y evaluación de modelos, matriz de confusión y modelo guardado; estos corresponden principalmente a los siguientes sprints.

## 9. Dictamen preliminar del Product Owner

**Resultado: avance satisfactorio, con observaciones y evidencias pendientes.**

La revisión confirma resultados positivos en las pruebas automatizadas (15 aprobadas), en la ejecución del proceso de preparación y en el resumen de calidad compartido. Los conteos principales coinciden y se conserva la distribución de las siete clases, salvo la eliminación de duplicados identificados en HOROZ.

Sin embargo, todavía no corresponde emitir una aceptación definitiva de todo el Sprint 1, porque falta revisar la ejecución integral del notebook y las evidencias gráficas e interpretativas del EDA, además de aclarar el conteo de outliers y la compatibilidad de versiones de Python.

**Decisión del PO:** mantener el entregable en estado **“En revisión — requiere completar evidencias y atender observaciones”**. Una vez atendidos estos puntos, se podrá realizar la validación final del Sprint 1.

---

*Documento de seguimiento de la revisión. Este dictamen refleja únicamente las evidencias examinadas hasta la fecha y no constituye una auditoría completa del repositorio.*
