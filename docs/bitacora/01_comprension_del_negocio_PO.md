# 1. Comprensión del negocio — CRISP-DM

**Proyecto:** Laboratorio de Machine Learning — Dry Bean Dataset  
**Responsable de la sección:** Product Owner (PO)  
**Fase CRISP-DM:** 1. Comprensión del negocio  
**Estado:** Borrador para revisión y aprobación del equipo

## 1.1 Contexto del negocio

Una empresa agrícola que recibe, acondiciona, almacena y comercializa fríjol seco necesita mantener información confiable sobre los lotes que procesa. La identificación consistente de las variedades es relevante para organizar el inventario, separar lotes, planificar procesos posteriores y entregar información clara a clientes y áreas operativas.

En un proceso de clasificación manual pueden presentarse diferencias entre operarios, tiempos de inspección variables y errores al distinguir variedades con características físicas semejantes. Estas situaciones pueden afectar la trazabilidad del producto y generar reprocesos o decisiones operativas incorrectas.

Este proyecto desarrolla un prototipo de clasificación automática de siete variedades de fríjol seco a partir de 16 características geométricas extraídas de imágenes. El conjunto de datos Dry Bean contiene 13.611 observaciones originales y la variable objetivo `Class`. Después de la limpieza reportada en el repositorio se conservan 13.543 registros.

**Alcance real del prototipo:** el modelo estima la variedad del grano a partir de las variables geométricas disponibles. No determina por sí mismo humedad, contaminación, daño, calibre comercial, inocuidad, calidad sanitaria ni aptitud de consumo. Tampoco sustituye una inspección o un sistema de calidad industrial validado.

## 1.2 Problema de negocio

La necesidad que aborda el proyecto es apoyar la identificación de variedades de fríjol seco de forma más consistente y reproducible, reduciendo la dependencia exclusiva de la clasificación visual manual.

En el contexto de una empresa agrícola, una identificación incorrecta puede ocasionar:

- Mezcla o registro incorrecto de variedades en inventario.
- Errores en la separación, almacenamiento o preparación de lotes.
- Pérdida de trazabilidad entre la recepción y la comercialización.
- Reprocesos y tiempo adicional de verificación.
- Menor confianza en los reportes operativos cuando la clasificación no es consistente.

El problema analítico se formula como una tarea de **clasificación multiclase supervisada**: dada una observación con 16 características geométricas, estimar una de las siete clases de variedad presentes en el dataset.

## 1.3 Objetivo general

Desarrollar y evaluar un modelo de Machine Learning que clasifique granos de fríjol seco en una de las siete variedades del conjunto Dry Bean, utilizando 16 características geométricas, con desempeño equilibrado entre clases, trazabilidad y capacidad de ejecución reproducible.

## 1.4 Objetivos específicos

1. Comprender la estructura, calidad y distribución de los datos disponibles.
2. Preparar un conjunto de datos reproducible, evitando fuga de información entre entrenamiento y prueba.
3. Entrenar y comparar modelos de clasificación con un protocolo de evaluación consistente.
4. Priorizar métricas que reflejen el desempeño en todas las variedades y no solamente en las clases mayoritarias.
5. Seleccionar un modelo final considerando desempeño, complejidad, interpretabilidad y uso previsto.
6. Documentar cómo interpretar el resultado y cuáles son las limitaciones del prototipo.

## 1.5 Usuarios y partes interesadas

| Interesado | Necesidad o interés |
|---|---|
| Operario de recepción/clasificación | Obtener una estimación de variedad como apoyo a la revisión del grano o lote. |
| Responsable de calidad | Consultar resultados consistentes y detectar casos que requieren verificación. |
| Responsable de inventario/operaciones | Mantener una identificación y trazabilidad más ordenadas de las variedades. |
| Dirección o responsable del negocio | Conocer el valor, las limitaciones y los riesgos antes de considerar una adopción. |
| Equipo del proyecto | Entregar un prototipo reproducible, evaluado y documentado. |

## 1.6 Criterios de éxito del negocio y del producto

El prototipo se considerará útil para una evaluación académica y técnica cuando:

- Identifique las siete variedades definidas en el dataset.
- Cumpla los umbrales de desempeño establecidos por el PO en el documento de criterios de aceptación del modelo.
- Presente resultados por clase, además de métricas globales.
- Permita reproducir preparación, entrenamiento y predicción siguiendo las instrucciones del repositorio.
- Explique el resultado en lenguaje comprensible para un usuario no especializado.
- Comunique claramente que la predicción es una ayuda y no una certificación de calidad comercial.

Los umbrales numéricos del modelo se especifican en `02_criterios_aceptacion_modelo_PO.md`.

## 1.7 Alcance y exclusiones

**Incluye:**

- Clasificación de las siete variedades del dataset.
- Uso de las 16 características geométricas.
- Preparación de datos, entrenamiento, comparación y evaluación.
- Registro de métricas, matriz de confusión y modelo reproducible.
- Documentación de uso, interpretación y limitaciones.

**No incluye:**

- Detección de granos defectuosos, contaminantes o cuerpos extraños.
- Medición de humedad, peso, tamaño comercial certificado o inocuidad.
- Clasificación de variedades que no estén representadas en el entrenamiento.
- Integración con cámaras, bandas transportadoras, PLC o sistemas productivos.
- Garantía de rendimiento en imágenes, equipos, fincas o condiciones diferentes a las del dataset sin validación adicional.

## 1.8 Riesgos del negocio y del proyecto

| Riesgo | Consecuencia posible | Mitigación / respuesta |
|---|---|---|
| Desbalance de clases | El modelo puede favorecer variedades frecuentes y fallar más en clases minoritarias. | Usar F1 Macro y recall por clase; revisar matriz de confusión. |
| Confusión entre variedades similares | Una predicción equivocada puede afectar inventario o separación de lotes. | Identificar pares de clases confundidos y derivar casos dudosos a revisión humana. |
| Diferencias entre dataset y operación real | El desempeño de laboratorio puede no generalizar a otras cámaras, fincas o condiciones. | Validar con datos representativos del entorno real antes de desplegar. |
| Datos de entrada incompletos o incorrectos | Predicciones inválidas o rechazo de registros. | Validar presencia y calidad de las 16 variables antes de predecir. |
| Interpretación excesiva de la predicción | El usuario puede confundir variedad estimada con calidad o inocuidad. | Incluir advertencias explícitas y capacitación básica. |
| Cambios en el origen o distribución de los datos | Caída del rendimiento con el tiempo. | Monitorear métricas y revisar el modelo cuando cambien variedades, equipos o procesos. |
| Dependencia de versiones de librerías | Resultados o carga del modelo diferentes entre equipos. | Fijar dependencias, registrar versiones y ejecutar pruebas reproducibles. |

## 1.9 Supuestos y restricciones

- Se asume que las observaciones representan granos de las siete variedades incluidas en el dataset.
- Se asume que las 16 características geométricas fueron calculadas de forma consistente.
- La variable objetivo es `Class`.
- El resultado se limita al dominio de datos utilizado; no se debe asumir que el modelo reconoce clases desconocidas.
- La solución se evalúa inicialmente como prototipo académico, no como sistema industrial certificado.

## 1.10 Decisión de negocio propuesta

Se propone aceptar el prototipo como una herramienta de apoyo a la identificación de variedades, siempre que cumpla los criterios cuantitativos y de reproducibilidad definidos por el PO. Cualquier uso operativo debe incluir revisión humana y una validación adicional con datos reales de la empresa.

**Aprobación PO:** _Andres Lopez  
**Fecha:** 12 Nov 2026  
