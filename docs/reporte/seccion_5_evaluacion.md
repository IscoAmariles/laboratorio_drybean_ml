# Sección 5 · Evaluación

*Borrador del ML Engineer · Fase 5 de CRISP-DM. Evidencia en [`outputs/reports/`](../../outputs/reports/) y en los notebooks [02](../../notebooks/02_modelado_evaluacion.ipynb), [03](../../notebooks/03_analisis_errores.ipynb) y [04](../../notebooks/04_modelo_final_y_despliegue.ipynb).*

## 5.1 Resultado en palabras simples

El modelo final acierta la variedad en **92 de cada 100 granos** nuevos, y su F1 macro es 0,934. Reconoce sin errores los granos `BOMBAY` y se equivoca sobre todo entre `DERMASON` y `SIRA`, dos variedades casi iguales en forma que solo se distinguen por tamaño y cuyos tamaños se solapan.

## 5.2 Comparación de modelos

**Sprint 2 (test = 2.709 granos y validación cruzada sobre train):**

| Modelo | Accuracy | F1 macro | F1 macro CV |
|---|---|---|---|
| Regresión logística | 0,9195 | 0,9306 | 0,9365 ± 0,0037 |
| Random Forest | 0,9195 | 0,9310 | 0,9343 ± 0,0047 |
| Random Forest ajustado | 0,9192 | 0,9308 | 0,9354 ± 0,0043 |

Los tres son equivalentes: la diferencia entre ellos es menor que la variación entre pliegues.

**Sprint 3 (validación cruzada anidada, mismos 5 pliegues):**

| Modelo | F1 macro CV | Diferencia vs. regresión logística | Pliegues ganados |
|---|---|---|---|
| Regresión logística | 0,9365 ± 0,0037 | — | — |
| Random Forest | 0,9343 ± 0,0047 | −0,0022 | 1 de 5 |
| **SVM RBF** | **0,9432 ± 0,0049** | **+0,0068** | **5 de 5** |
| Gradient Boosting | 0,9405 ± 0,0033 | +0,0041 | 5 de 5 |

## 5.3 Decisión del modelo final

Regla del equipo (Sprint 2): dos modelos son equivalentes si la diferencia de sus medias de CV no supera la mayor de sus desviaciones; entre los equivalentes al mejor se elige el **más simple**.

- La SVM supera a la regresión logística por 0,0068, **más que la mayor desviación** (0,0049), y gana en los 5 pliegues: ya no son equivalentes.
- Gradient Boosting es equivalente a la SVM; entre los dos se elige el más simple.
- **Modelo elegido: SVM RBF** (`C=100`, `gamma=0,01`).

Esto **corrige la conclusión del Sprint 2**, que eligió la regresión logística al comparar solo tres modelos. La prueba formal que pidió el diagnóstico del repositorio mostró una mejora que el Sprint 2 no había explorado.

## 5.4 Desempeño del modelo final en test

| Métrica | SVM RBF (final) | Regresión logística |
|---|---|---|
| Accuracy | 0,9232 | 0,9195 |
| F1 macro | 0,9342 | 0,9306 |
| Peor recall por clase | 0,871 (`SIRA`) | 0,886 (`SIRA`) |

**Por clase (modelo final):**

| Clase | Recall | F1 |
|---|---|---|
| BOMBAY | 1,000 | 1,000 |
| HOROZ | 0,938 | 0,952 |
| SEKER | 0,956 | 0,951 |
| CALI | 0,936 | 0,930 |
| DERMASON | 0,922 | 0,920 |
| BARBUNYA | 0,913 | 0,917 |
| **SIRA** | **0,871** | **0,870** |

**Criterio de aceptación propuesto** (F1 macro ≥ 0,92 y recall mínimo por clase ≥ 0,85, a validar por el Product Owner): se **cumple** (0,934 y 0,871).

## 5.5 Dónde se equivoca

- **`DERMASON` ↔ `SIRA`:** 95 errores en total (49 y 46), el 46 % de los 208 errores del modelo. Forma casi idéntica (relación de aspecto mediana 1,48 y 1,56; solidez 0,989 en ambas); se diferencian por tamaño, con solapamiento.
- **`BARBUNYA` → `CALI`:** 15 errores, y 11 en el sentido contrario. Áreas medianas parecidas.
- **Los errores no dependen del algoritmo:** la regresión logística y el Random Forest también concentran ~95 errores en `DERMASON` ↔ `SIRA`. El límite está en que las variedades se solapan en las medidas, no en el modelo.

## 5.6 Cómo leer la mejora, y sus límites

- Es **pequeña pero consistente**: +0,0068 de F1 macro en validación cruzada (en los 5 pliegues) y +0,0036 en test. Un solo conjunto de test no basta para confirmarla por sí solo.
- **No mejora el punto débil:** el recall de `SIRA` baja de 0,886 a 0,871. Mejoran otras clases, por ejemplo `BARBUNYA` (de 0,891 a 0,913).
- **Interpretabilidad:** la SVM no entrega coeficientes por variable como la regresión logística. La mejora (≈ 0,7 puntos de F1 en CV) tiene ese costo; es una decisión de valor para el Product Owner.
- **Importancia de variables** (Random Forest, Sprint 2): por impureza se reparte entre variables colineales (`Perimeter`, `ShapeFactor1`, `Compactness`); por permutación destaca `Roundness`. No prueba causalidad.
- **Alcance:** un solo split 80/20 y un solo dataset.

## 5.7 Preguntas de reflexión del laboratorio (4 a 7)

| Pregunta | Respuesta |
|---|---|
| 4. ¿Por qué se usa un baseline? | Es el punto de comparación. Aquí fue útil dos veces: mostró que Random Forest no aportaba nada, y su comparación formal con la SVM permitió medir una mejora real. |
| 5. ¿Qué métrica para escoger el mejor modelo? | F1 macro, porque da el mismo peso a las variedades pequeñas y a las grandes; se complementa con el recall por clase. |
| 6. ¿Qué haría si una clase tiene muchos más errores? | Revisar sus errores con el EDA (aquí, `SIRA` frente a `DERMASON`), buscar variables que separen mejor, probar pesos de clase o más muestras. |
| 7. ¿Qué información falta antes de producción? | Ver la sección 6.5. |
