# 2. Criterios numéricos de aceptación del modelo

**Proyecto:** Laboratorio Dry Bean  
**Responsable:** Product Owner (PO)  
**Versión:** 1.0 — propuesta de criterio de aceptación

## 2.1 Propósito

Definir una regla cuantitativa, verificable y acordada antes de declarar que el modelo cumple el objetivo del proyecto. La aceptación no debe depender únicamente de accuracy ni de una impresión general del resultado.

## 2.2 Umbrales propuestos por el PO

El modelo final debe cumplir simultáneamente:

| Métrica | Umbral mínimo | Motivo |
|---|---:|---|
| F1 Macro en test | **≥ 0,92** | Da el mismo peso a cada una de las siete clases y reduce el riesgo de ocultar un mal resultado en clases minoritarias. |
| Recall mínimo por clase en test | **≥ 0,85** | Exige que ninguna variedad quede con una capacidad de detección demasiado baja. |

**Regla de aceptación:** el modelo se acepta por desempeño únicamente si cumple los dos umbrales. Si uno falla, se registra como no aceptado o se solicita una mejora justificada.

El conjunto de test debe permanecer separado del proceso de selección y ajuste de modelos. La selección se realiza mediante validación cruzada sobre train; el test se utiliza para la evaluación final una sola vez, conforme al protocolo del equipo.

## 2.3 Resultados publicados en el repositorio consultado

El README del repositorio reporta para el modelo SVM RBF seleccionado:

| Indicador | Resultado reportado | Umbral | Evaluación |
|---|---:|---:|---|
| F1 Macro en test | 0,9342 | ≥ 0,92 | Cumple |
| Recall mínimo por clase | 0,871 (SIRA) | ≥ 0,85 | Cumple |

Por tanto, **según los resultados publicados actualmente en el README**, el modelo SVM RBF cumple los dos criterios propuestos.

> Nota de consistencia: en conversaciones o resultados previos se mencionaron cifras diferentes (por ejemplo, F1 Macro 0,931 y recall mínimo 0,886). Para el acta de aceptación debe prevalecer el resultado reproducible y versionado del experimento final. Antes de firmar, el ML Engineer y el PO deben confirmar que el notebook, el archivo de métricas y la metadata del modelo coinciden con 0,9342 y 0,871, o actualizar este documento si existe una ejecución posterior válida.

## 2.4 Reglas para medir correctamente

1. Evaluar las siete clases, no solo el promedio global.
2. Calcular F1 Macro como promedio no ponderado del F1 de cada clase.
3. Calcular recall individual para cada variedad y registrar el menor valor, identificando la clase correspondiente.
4. Utilizar exactamente el mismo conjunto de test y el mismo mapeo de etiquetas para comparar modelos.
5. No seleccionar hiperparámetros ni modelos mirando repetidamente el resultado del test.
6. Registrar versión de Python, scikit-learn, parámetros del modelo y semilla/protocolo utilizado.
7. Adjuntar matriz de confusión y reporte de clasificación como evidencia.

## 2.5 Decisión si el modelo no cumple

- Si F1 Macro es menor que 0,92, el modelo no cumple el criterio global.
- Si el recall de cualquiera de las siete clases es menor que 0,85, el modelo no cumple el criterio por clase, aunque F1 Macro supere 0,92.
- El equipo debe analizar los errores, proponer una mejora y volver a evaluar siguiendo un protocolo documentado.
- No se permite cambiar el umbral después de observar el test para declarar el modelo aceptado sin registrar formalmente la nueva decisión del PO.

## 2.6 Alcance de esta aceptación

Cumplir los umbrales significa que el modelo satisface los criterios cuantitativos del proyecto sobre el conjunto de test disponible. No demuestra por sí solo que el modelo esté listo para operar en una empresa agrícola real. Para ese uso se requiere validación con datos representativos del entorno productivo, revisión humana y monitoreo.

## 2.7 Aprobación

**Decisión propuesta del PO:** aprobar los umbrales F1 Macro ≥ 0,92 y recall mínimo por clase ≥ 0,85.

**PO:** __Andres Lopez  
**Fecha de aprobación:** __12 Nov 2026

