# Sección 6 · Despliegue

*Borrador del ML Engineer · Fase 6 de CRISP-DM. Código: [`src/train.py`](../../src/train.py) y [`src/predict.py`](../../src/predict.py), con pruebas en [`tests/`](../../tests/). Demostración: [notebook 04](../../notebooks/04_modelo_final_y_despliegue.ipynb), secciones 4 a 7.*

El despliegue de este laboratorio es **local y reproducible**: el modelo queda guardado, se puede cargar y usar desde código o desde la terminal. No es un servicio en producción.

## 6.1 Qué se guardó

| Archivo | Contenido |
|---|---|
| `outputs/models/modelo_final_drybean.joblib` (413 KB) | El `Pipeline` **completo**: escalador + SVM. Guardar solo el clasificador rompería la predicción, porque el modelo espera las variables ya estandarizadas |
| `outputs/models/modelo_final_metadata.json` | Nombre del modelo, hiperparámetros elegidos, métricas en test y por clase, variables en su orden, clases, `random_state`, tamaños de train y test, fecha y **versiones** de Python, scikit-learn, pandas, numpy y joblib |

**Política del `.joblib`:** se versiona en Git porque pesa menos de 0,5 MB (el `.gitignore` ya no lo excluye). Si el modelo pasara de unos pocos MB, se volvería a ignorar y se regeneraría con `python -m src.train`. `joblib` no garantiza compatibilidad entre versiones de scikit-learn, por eso la metadata guarda la versión y `load_model` **avisa** si el entorno no coincide.

## 6.2 Cómo reproducirlo

```powershell
python -m src.make_dataset    # datos procesados (Sprint 1)
python -m src.train           # entrena con train, evalúa una vez en test y guarda el modelo
```

`python -m src.train --model logreg` guarda la regresión logística en su lugar (alternativa interpretable). Con `--no-tune` se omite el ajuste de hiperparámetros. Reentrenar produce las mismas métricas e hiperparámetros.

## 6.3 Cómo usarlo

**Desde código** (`predict_bean_class`, paso 18 del laboratorio):

```python
from src.predict import load_model, predict_bean_class, predict_beans

modelo = load_model()
predict_bean_class(modelo, grano)       # un grano: dict, Series o DataFrame de una fila
predict_beans(modelo, granos)           # varias filas
```

**Desde la terminal**, con un CSV que traiga las 16 variables:

```powershell
python -m src.predict --input nuevos_granos.csv --output predicciones.csv
```

El resultado agrega la columna `predicted_class`. Antes de predecir, la entrada se valida: se rechazan variables faltantes (el error nombra cuáles) y valores nulos; las columnas pueden venir en cualquier orden y las extra se ignoran.

## 6.4 Cómo se probó

| Prueba | Qué comprueba |
|---|---|
| Modelo cargado frente a modelo en memoria (paso 17) | Las predicciones del `.joblib` son idénticas a las del modelo recién entrenado |
| Metadata frente a evaluación real | El F1 macro guardado coincide con recalcularlo cargando el modelo |
| Entrada inválida | Variables faltantes y nulos dan un error claro; el orden de columnas no cambia el resultado |
| Versiones | `load_model` avisa si cambia la versión de scikit-learn y no avisa si coincide |
| Aceptación del modelo versionado | Sobre `test.csv`: F1 macro ≥ 0,92 y recall mínimo por clase ≥ 0,85 |

En el notebook 04 se cargó el modelo, se predijo un grano de prueba (predicción `SEKER`, valor real `SEKER`) y se predijo un lote desde un CSV con la línea de comandos. La suite completa tiene 73 pruebas en verde.

## 6.5 Qué falta antes de llevarlo a producción (pregunta 7 del laboratorio)

- **Mismo sistema de captura.** Las medidas están en **píxeles**: el modelo solo es válido con la misma cámara, resolución, calibración y método de segmentación que generaron el dataset. Un cambio de cámara invalida las medidas.
- **Monitoreo de deriva.** Vigilar si las distribuciones de las 16 variables se alejan de las del entrenamiento (nuevas variedades, cambios de cosecha o de iluminación).
- **Umbral de confianza.** La SVM por defecto no entrega probabilidades. Para derivar los casos dudosos (`DERMASON` o `SIRA`) a revisión manual se necesita calibrarlas o usar la regresión logística, que sí las entrega.
- **Criterio de aceptación definido por negocio.** Los umbrales usados (F1 macro ≥ 0,92 y recall ≥ 0,85) son una propuesta; el Product Owner debe fijarlos y, si hay variedades más costosas de confundir, pedir un recall mayor para ellas.
- **Rendimiento y operación.** Medir latencia y volumen reales, versionar el modelo con sus datos y definir cada cuánto se reentrena.
- **Más datos.** Un único dataset y un único split; convendría validar con un lote nuevo de granos.
