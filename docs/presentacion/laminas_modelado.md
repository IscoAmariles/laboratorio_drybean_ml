# Guion de láminas: modelado, evaluación y despliegue

*ML Engineer. Seis láminas, unos 7 minutos. Cada lámina usa una figura o tabla que ya existe en `outputs/reports/`. Complementa [`laminas_datos.md`](laminas_datos.md).*

| # | Título (mensaje) | Contenido | Figura |
|---|---|---|---|
| 1 | **Cómo elegimos el modelo: sin mirar el test** | Mismo 80/20 del Sprint 1; todas las decisiones con validación cruzada de 5 pliegues solo sobre train; el test se usa una sola vez al final. Métrica: F1 macro (pesa igual `BOMBAY` que `DERMASON`) | — |
| 2 | **Cuatro candidatos, los mismos pliegues** | Regresión logística (baseline), Random Forest, SVM RBF y Gradient Boosting. Validación cruzada **anidada**: los hiperparámetros se eligen dentro de cada pliegue, para no ser optimistas | `comparacion_ampliada_por_pliegue.png` |
| 3 | **La SVM gana en los 5 pliegues** | F1 macro CV: SVM 0,9432, Gradient Boosting 0,9405, regresión logística 0,9365, Random Forest 0,9343. La SVM supera a la logística por 0,0068, más que la variación entre pliegues (0,0049). Gradient Boosting empata con la SVM y se elige la más simple. **El Sprint 2 había elegido la logística; la prueba formal corrigió esa conclusión** | `comparacion_ampliada.csv` (tabla) |
| 4 | **Resultado: acierta 92 de cada 100 granos** | Test: accuracy 0,9232, F1 macro 0,9342, peor recall 0,871 (`SIRA`). Cumple el criterio propuesto (F1 macro ≥ 0,92 y recall ≥ 0,85). `BOMBAY` sin errores; el error está en `DERMASON` ↔ `SIRA` (95 de 208) | `matriz_confusion_normalizada_modelo_final.png` |
| 5 | **Despliegue: del notebook a un modelo que se usa** | `Pipeline` completo (escalador + SVM) guardado con `joblib` (413 KB) y un JSON con hiperparámetros, métricas, variables y versiones. `python -m src.train` lo regenera con las mismas métricas; `python -m src.predict --input nuevos.csv` predice un lote y rechaza datos incompletos. 73 pruebas en verde | — (demostración en vivo del paso 18) |
| 6 | **Límites y decisiones abiertas** | Mejora pequeña pero consistente (+0,0036 de F1 en test). No mejora a `SIRA` (recall 0,886 → 0,871). La SVM es menos interpretable y no da probabilidades: decide el Product Owner si vale ≈ 0,7 puntos de F1. Producción: misma cámara y calibración (medidas en píxeles), monitoreo de deriva y umbral de confianza | — |

**Notas para quien presente**
- En la lámina 3, insistir en que el equipo **corrigió** su propia conclusión: es el resultado de una buena práctica (probar formalmente antes de cerrar), no un error.
- La lámina 5 de los datos ([`laminas_datos.md`](laminas_datos.md)) habla de 218 errores con la regresión logística; con el modelo final son 208.
- Si preguntan "¿por qué no Random Forest, que suele ganar?": aquí no ganó; ni ajustado supera a la regresión logística.
- Si preguntan "¿por qué la SVM y no el boosting, si empatan?": la regla del equipo elige el más simple entre los equivalentes.
- Si preguntan "¿y si queremos interpretabilidad?": `python -m src.train --model logreg` cambia el modelo guardado y también cumple el criterio (F1 macro 0,9306, recall mínimo 0,886).
- No ejecutar el notebook 04 en vivo: la validación anidada tarda varios minutos. Mostrar el notebook ya ejecutado y correr solo el paso 18.
