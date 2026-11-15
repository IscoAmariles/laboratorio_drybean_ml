# 3. Acta de aceptación del Sprint 1 — Comprensión y preparación de datos

**Proyecto:** Laboratorio Dry Bean  
**Responsable de aceptación:** Product Owner (PO)  
**Sprint:** 1 — Comprensión y preparación de datos  
**Alcance:** PB-01 (ingesta) y PB-02 (calidad), EDA y partición train/test  
**Estado del acta:** Aceptación documentada con evidencia; verificación final reproducible del PO registrada como control de cierre.

## 3.1 Criterios de aceptación

El Sprint 1 se considera aceptable cuando el equipo demuestra que:

- Los datos originales se cargan y se conservan sin alteración.
- Se documentan estructura, clases, valores nulos y duplicados.
- Se genera un conjunto limpio y se explica el tratamiento aplicado.
- Se exploran distribución, correlaciones y valores atípicos.
- Se conserva la trazabilidad de los archivos procesados y reportes.
- Se genera una partición de entrenamiento y prueba estratificada.
- El notebook y el código se pueden ejecutar en el entorno documentado.

## 3.2 Tabla de revisión y evidencias

| ID / aspecto | Criterio | Evidencia revisada | Resultado PO |
|---|---|---|---|
| PB-01 — Ingesta | Carga del dataset original | Dataset Dry Bean con 13.611 filas y 17 columnas (16 características y `Class`), documentado en README y notebook 01. | Cumple |
| PB-02 — Nulos | Identificar valores faltantes | Resumen de calidad: 0 nulos en datos crudos y limpios. | Cumple |
| PB-02 — Duplicados | Identificar y tratar duplicados | 68 duplicados eliminados; conjunto limpio de 13.543 filas. Todos los duplicados reportados pertenecen a HOROZ. | Cumple |
| PB-02 — Outliers | Analizar y justificar tratamiento | El README indica que no se eliminan porque representan mediciones físicas. El notebook 01, sección 5.1, documenta el cambio del conteo IQR de 7.139 a 7.152: se retiran 35 conteos de filas repetidas y aparecen 48 al recalcular cuartiles. | Cumple según evidencia documentada |
| EDA — Clases | Revisar distribución de las siete clases | DERMASON: 3.546; SIRA: 2.636; SEKER: 2.027; HOROZ: 1.860; CALI: 1.630; BARBUNYA: 1.322; BOMBAY: 522. | Cumple |
| EDA — Desbalance | Identificar desbalance y consecuencia | README reporta razón aproximada 6,8 entre DERMASON y BOMBAY y propone F1 Macro como métrica principal. | Cumple |
| EDA — Correlaciones | Identificar variables altamente correlacionadas | README reporta Area–ConvexArea ≈ 1,00; Perimeter–EquivDiameter ≈ 0,99; Compactness–ShapeFactor3 ≈ 1,00. | Cumple |
| Preparación — Split | Partición reproducible | 80/20 estratificado, `random_state=42`: train 10.834 y test 2.709. | Cumple |
| Preprocesamiento | Evitar fuga de información | README describe `StandardScaler` dentro del Pipeline, ajustado con train. | Cumple |
| Pruebas | Validar funciones del Sprint 1 | En la primera revisión local del PO se ejecutó `python -m pytest`: 15 pruebas aprobadas. | Cumple en esa ejecución |
| Generación de datos | Verificar proceso de preparación | En la primera revisión local del PO, `python -m src.make_dataset` generó 13.611 crudas, 68 duplicados eliminados, 13.543 limpias, 10.834 train y 2.709 test. | Cumple en esa ejecución |

## 3.3 Observaciones y alertas cerradas

1. **Aumento del conteo IQR después de limpiar:** queda explicado en el README y en la sección 5.1 del notebook 01. El aumento no implica que se hayan añadido registros; el cálculo de los límites IQR cambia al recalcular los cuartiles sobre el conjunto sin duplicados.
2. **Desbalance de clases:** está identificado y se relaciona con la elección de F1 Macro.
3. **Colinealidad:** se identifican pares de variables con correlación muy alta; debe considerarse al interpretar modelos lineales y la importancia de variables.
4. **Compatibilidad de Python:** el README actualizado especifica Python 3.12 o superior, coherente con las dependencias fijadas y con el entorno 3.12.10 utilizado en la revisión local.
5. **Trazabilidad:** el README documenta archivos crudos, procesados, reportes, código y pruebas.

## 3.4 Control de reproducibilidad antes del cierre definitivo

Aunque existen resultados de pruebas y generación de datos de la primera revisión, el PO debe realizar una verificación integral desde el repositorio sincronizado para cerrar la reproducibilidad del entregable:

- [ ] Activar el entorno virtual basado en Python 3.12 o superior.
- [ ] Confirmar que el kernel del notebook utiliza ese mismo entorno.
- [ ] Abrir `notebooks/01_comprension_preparacion_datos.ipynb`.
- [ ] Ejecutar **Restart Kernel and Run All** (o equivalente) desde el inicio.
- [ ] Confirmar que no hay celdas con errores.
- [ ] Confirmar que las salidas y los archivos de `data/processed/` y `outputs/reports/` se generan correctamente.
- [ ] Registrar fecha, versión de Python y resultado de la ejecución.

**Registro de ejecución del PO**

| Campo | Registro |
|---|---|
| Fecha | ___13 Nov 2026 |
| Versión de Python | __3.12 |
| Kernel utilizado | __IPython Kernel  |
| Resultado Restart & Run All | Pendiente de registrar |
| Incidencias | __0  |

## 3.5 Dictamen del Product Owner

Con las evidencias registradas en el repositorio y los resultados obtenidos durante la primera revisión local, los criterios funcionales de PB-01 y PB-02 se consideran satisfechos. Las alertas identificadas tienen una explicación o evidencia asociada.

**Decisión:** Sprint 1 aceptado desde el punto de vista de los entregables de ingesta, calidad, EDA y preparación, sujeto a completar el control de reproducibilidad del apartado 3.4 por el PO antes de declarar el cierre administrativo definitivo.

**PO:** __Andres Lopez  
**Fecha de aceptación:** __13 Nov 2026 

