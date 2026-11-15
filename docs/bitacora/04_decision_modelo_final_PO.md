# 4. Decisión del Product Owner sobre el modelo final

**Proyecto:** Laboratorio Dry Bean  
**Responsable de decisión:** Product Owner (PO)  
**Modelos considerados:** Logistic Regression, Random Forest, SVM RBF y Gradient Boosting  
**Estado:** Recomendación de decisión basada en resultados publicados; requiere ratificación del PO.

## 4.1 Decisión que debe tomar el PO

La selección del modelo final no depende exclusivamente de cuál obtiene el mayor resultado numérico. Debe equilibrar:

- Desempeño global y por clase.
- Estabilidad de los resultados de validación cruzada.
- Interpretabilidad para los usuarios.
- Complejidad de mantenimiento.
- Cumplimiento de los criterios de aceptación definidos por el PO.

## 4.2 Evidencia comparativa publicada

El README reporta la siguiente validación cruzada anidada de cinco pliegues sobre train, utilizando los mismos pliegues para los modelos:

| Modelo | F1 Macro CV | Diferencia frente a Logistic Regression | Pliegues ganados |
|---|---:|---:|---:|
| Logistic Regression | 0,9365 ± 0,0037 | — | — |
| Random Forest | 0,9343 ± 0,0047 | −0,0022 | 1 de 5 |
| SVM RBF | 0,9432 ± 0,0049 | +0,0068 | 5 de 5 |
| Gradient Boosting | 0,9405 ± 0,0033 | +0,0041 | 5 de 5 |

En la comparación entre SVM RBF y Gradient Boosting, SVM obtiene una media de F1 Macro CV 0,0027 superior. Frente a Logistic Regression, la diferencia de SVM es 0,0068, equivalente a **0,68 puntos porcentuales** de F1 Macro.

El README reporta para SVM RBF en test:

- Accuracy: 0,9232.
- F1 Macro: 0,9342.
- Recall mínimo por clase: 0,871, correspondiente a SIRA.

Estos resultados superan los umbrales propuestos por el PO: F1 Macro ≥ 0,92 y recall mínimo por clase ≥ 0,85.

## 4.3 Interpretación de valor

**Ventajas de SVM RBF**

- Presenta el mejor promedio de F1 Macro CV entre los modelos comparados.
- Supera a Logistic Regression en los cinco pliegues reportados.
- Supera a Gradient Boosting en la media de CV reportada.
- Cumple los criterios cuantitativos publicados para test.

**Costos y riesgos de SVM RBF**

- Es menos interpretable que Logistic Regression.
- Puede ser más difícil explicar directamente el efecto de cada característica.
- Requiere documentar sus hiperparámetros y el entorno de ejecución.
- La ventaja frente a Gradient Boosting es pequeña (0,0027 de F1 Macro CV), por lo que debe evitarse exagerar su impacto práctico.

**Alternativa interpretable**

Logistic Regression obtiene F1 Macro CV de 0,9365 ± 0,0037 y también cumple los umbrales publicados para el modelo final en las evaluaciones disponibles del proyecto. Si la prioridad del negocio fuera explicar de forma sencilla la relación entre variables y predicción, sería una alternativa razonable.

## 4.4 Recomendación del PO

**Recomendación:** seleccionar **SVM RBF (`C=100`, `gamma=0,01`)** como modelo final del prototipo, porque ofrece el mejor F1 Macro CV reportado y cumple los umbrales de aceptación en test.

La recomendación acepta explícitamente el costo de una menor interpretabilidad a cambio de una mejora de 0,68 puntos porcentuales frente a Logistic Regression en F1 Macro CV. Esta decisión es adecuada si el objetivo prioritario del prototipo es la calidad de clasificación y si el reporte explica sus límites de interpretación.

Si la empresa prioriza explicabilidad por encima de esa mejora, el PO puede seleccionar Logistic Regression como alternativa. La elección debe registrarse como decisión de producto, no presentarse como una obligación puramente técnica.

## 4.5 Condiciones antes de ratificar la decisión

- [ ] Confirmar que los resultados de CV y test corresponden a la misma versión final del código y del dataset.
- [ ] Confirmar que el test no se utilizó para elegir hiperparámetros.
- [ ] Revisar la matriz de confusión y el recall de las siete clases.
- [ ] Confirmar que `outputs/models/modelo_final_drybean.joblib` y su metadata corresponden a SVM RBF.
- [ ] Confirmar que el procedimiento de carga y predicción funciona con las versiones de librerías documentadas.
- [ ] Incorporar en el reporte una explicación sencilla de la menor interpretabilidad de SVM.

## 4.6 Acta de decisión

**Modelo seleccionado por el PO:** Logistic Regression 

**Justificación de negocio:**  
_Se selecciona Logistic Regression porque presenta un rendimiento comparable al de los demás modelos evaluados, sin ofrecer diferencias de desempeño que justifiquen adoptar una alternativa de mayor complejidad. Desde la perspectiva del negocio, se prioriza una solución más sencilla, interpretable y fácil de mantener, que cumple con los criterios de aceptación establecidos para el proyecto.

**PO:** __Andres Lopez 
**Fecha:** __13 Nov 2026
