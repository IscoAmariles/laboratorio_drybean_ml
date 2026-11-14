# Sección 4 · Modelado

*Borrador del ML Engineer · Fase 4 de CRISP-DM. Código: [`src/models.py`](../../src/models.py) y [`src/evaluate.py`](../../src/evaluate.py), con pruebas en [`tests/`](../../tests/). Notebooks: [02](../../notebooks/02_modelado_evaluacion.ipynb) y [04](../../notebooks/04_modelo_final_y_despliegue.ipynb).*

## 4.1 Qué se entrenó

El problema es de **clasificación multiclase**: dadas 16 medidas de un grano, predecir una de 7 variedades. Se entrenaron cuatro modelos, de más simple a más complejo:

| Modelo | Qué es | Configuración |
|---|---|---|
| Regresión logística (baseline) | Modelo lineal; sirve de punto de comparación | Con escalado de variables, `max_iter=1000` |
| Random Forest | 200 árboles de decisión que votan | `class_weight="balanced"` para compensar las clases pequeñas |
| SVM con kernel RBF | Separa las clases con fronteras curvas | Con escalado; `C` y `gamma` elegidos por validación cruzada |
| Gradient Boosting | Árboles que se corrigen en secuencia | `learning_rate` y `max_iter` elegidos por validación cruzada |

Todos van dentro de un `Pipeline` de scikit-learn. En los que lo necesitan, el escalador se ajusta **solo con los datos de entrenamiento**, para que el test no filtre información al modelo.

## 4.2 Protocolo

| Decisión | Qué se hizo | Por qué |
|---|---|---|
| Datos | El 80/20 estratificado del Sprint 1 (`random_state=42`) | Mismas proporciones de variedad en train y test |
| Cómo se elige | Validación cruzada de 5 pliegues **solo sobre train** | El test no participa en ninguna decisión |
| Ajuste de hiperparámetros | `GridSearchCV` con F1 macro; para comparar, **validación cruzada anidada** (el ajuste ocurre dentro de cada pliegue) | Evita el sesgo optimista de reportar la misma validación con la que se eligió |
| Comparación | Los mismos pliegues para todos los modelos y diferencias por pliegue | Permite ver si un modelo gana de forma consistente o por azar |
| Test | Se usa **una sola vez**, al final, para informar el desempeño | Es la estimación honesta del comportamiento con granos nuevos |
| Métrica principal | **F1 macro** | Pesa igual a `BOMBAY` (522 granos) que a `DERMASON` (3.546) |

## 4.3 Hiperparámetros elegidos

| Modelo | Grilla probada | Elegido |
|---|---|---|
| Random Forest | `n_estimators` {200, 400} × `max_depth` {None, 10, 20} × `min_samples_split` {2, 5, 10} | `n_estimators=400`, `max_depth=20`, `min_samples_split=2` |
| SVM RBF | `C` {1, 10, 100} × `gamma` {`scale`, 0,01} | `C=100`, `gamma=0,01` |
| Gradient Boosting | `learning_rate` {0,05, 0,1} × `max_iter` {100, 300} | Se eligió por pliegue dentro de la validación anidada |

La regresión logística no tiene hiperparámetros que ajustar. Para Gradient Boosting se fijó `early_stopping=False`: con el valor automático se activaría solo con más de 10.000 filas y cambiaría el protocolo entre la validación cruzada (≈ 8.700 filas por pliegue) y el ajuste final (10.834).

## 4.4 Qué no se hizo, y por qué

- **No se ajustó con el test:** ninguna decisión usa esos 2.709 granos.
- **No se quitaron variables correlacionadas:** no afecta a los árboles ni a la SVM de forma relevante, y la regresión logística las tolera con su regularización por defecto.
- **No se ampliaron las grillas indefinidamente:** el valor `C=100` de la SVM está en el borde de su grilla. Es una limitación conocida; seguir buscando sobre los mismos datos aumenta el riesgo de sobreajustar la validación.

## 4.5 Reproducibilidad

Todo el modelado usa `random_state=42` y las versiones fijadas de `requirements.txt` (scikit-learn 1.9.1). Reentrenar con `python -m src.train` produce las mismas métricas e hiperparámetros. Los notebooks deben ejecutarse con el kernel del `.venv`: con otro Python (por ejemplo, el de Anaconda) cambian las versiones y los resultados.
