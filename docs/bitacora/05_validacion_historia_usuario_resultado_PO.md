# Validación de historia de usuario: comprensión del resultado de clasificación

**Historia:** Como usuario final, quiero entender el resultado de la clasificación para saber qué variedad estima el modelo y cómo utilizar esa información.

**Responsable de validación:** Product Owner (PO)  
**Referencia:** Definition of Done (DoD) #8  
**Estado:** Aprobada

## 5.1 Propósito

El propósito de esta historia de usuario es garantizar que los resultados del proyecto puedan ser comprendidos por una persona sin conocimientos técnicos en Machine Learning.

El reporte final debía explicar en lenguaje cotidiano qué hace el modelo, qué significa su resultado, cuáles son sus limitaciones y cómo debe interpretarse la predicción.

Esta información fue incorporada y presentada durante la exposición final del proyecto al usuario final (docente), quien manifestó su aprobación de los resultados obtenidos.

## 5.2 Información presentada al usuario final

### ¿Qué hace el modelo y cómo se interpreta el resultado?

El sistema analiza 16 características geométricas de un grano de fríjol seco y estima a cuál de las siete variedades conocidas se parece más: BARBUNYA, BOMBAY, CALI, DERMASON, HOROZ, SEKER o SIRA.

En términos sencillos, el modelo compara las características medidas del grano con patrones que aprendió de ejemplos previamente clasificados. Como resultado, entrega una variedad estimada. Esta respuesta sirve como apoyo para organizar o revisar la clasificación, pero no debe interpretarse como una certeza absoluta.

Durante el desarrollo del proyecto se compararon diferentes modelos de clasificación y se seleccionó **Logistic Regression** como modelo final. La decisión se tomó porque presentó un rendimiento comparable al de los demás modelos evaluados, con una menor complejidad y mayor facilidad de interpretación y mantenimiento.

Los resultados de evaluación permiten considerar que el modelo tiene un buen desempeño general. Sin embargo, pueden presentarse errores de clasificación y algunas variedades pueden confundirse entre sí.

Por esta razón, cuando la predicción se utilice para tomar una decisión operativa importante, se recomienda que el resultado sea revisado por una persona responsable. Además, si los granos presentan características o condiciones diferentes a las representadas en los datos de entrenamiento, el comportamiento del modelo puede variar.

**Importante:** el sistema estima la variedad del grano. No determina si está dañado, contaminado, húmedo, apto para el consumo o si cumple una norma comercial. Esas evaluaciones requieren controles adicionales.

## 5.3 Criterios de aceptación de la historia

| Criterio | Evidencia presentada | Estado PO |
|---|---|---|
| El reporte explica qué información recibe el modelo. | Se explicó que utiliza 16 características geométricas del grano. | Aprobado |
| El reporte indica qué entrega el modelo. | Se explicó que estima una de las siete variedades de fríjol. | Aprobado |
| El resultado se explica sin depender de jerga técnica. | Se presentó una explicación en lenguaje cotidiano sobre el funcionamiento y la interpretación del resultado. | Aprobado |
| Se comunican límites y errores posibles. | Se aclaró que las predicciones pueden contener errores y que deben revisarse cuando la decisión sea importante. | Aprobado |
| Se evita atribuir capacidades que el modelo no tiene. | Se explicó que el sistema no evalúa humedad, defectos, inocuidad ni calidad comercial. | Aprobado |
| Las métricas y el modelo presentado corresponden a la decisión final del proyecto. | Se presentó Logistic Regression como modelo seleccionado por el PO, de acuerdo con la decisión documentada. | Aprobado |

## 5.4 Forma de presentación al usuario final

Durante la presentación del proyecto se explicó que el resultado de la herramienta debe interpretarse de la siguiente manera:

- **Variedad estimada:** nombre de la clase predicha por el modelo.
- **Mensaje de interpretación:** “El modelo estima que este grano corresponde a la variedad indicada”.
- **Aviso:** “Esta predicción es una ayuda para la clasificación y puede contener errores. Verifique el resultado cuando la decisión sea importante”.
- **Alcance:** “El resultado identifica una variedad probable; no certifica calidad, inocuidad ni ausencia de defectos”.

También se tuvo en cuenta que la etiqueta predicha no equivale automáticamente a un porcentaje de confianza. Por tanto, no se deben presentar porcentajes de certeza si no se cuenta con probabilidades debidamente calculadas y validadas.

## 5.5 Decisión de aceptación del PO

**Estado: Aprobada.**

La historia de usuario se considera aceptada. La información sobre el funcionamiento del modelo, la interpretación de sus resultados y sus principales limitaciones fue incorporada al reporte y presentada al usuario final durante la exposición del proyecto.

El docente recibió la explicación de los resultados obtenidos y manifestó su aprobación durante la presentación.

Con esta validación se considera cumplido el objetivo de la historia de usuario y el criterio correspondiente a la Definition of Done (DoD) #8.

## 5.6 Registro de validación y observaciones

**Responsable PO:** Andrés López

**Fecha de validación:** 14 de noviembre de 2026.

**Usuario final:** Docente del proyecto.

**Resultado de la validación:** Aprobado durante la presentación final.

**Observaciones:** Durante la presentación del proyecto se expusieron los resultados obtenidos, la decisión del modelo seleccionado y el alcance de la solución. El docente manifestó su aprobación frente a los resultados presentados. Por lo tanto, desde el rol de Product Owner, se registra la aceptación de esta historia de usuario.
