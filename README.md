# Laboratorio Dry Bean · Machine Learning con CRISP-DM + TDSP + Scrum ML

Clasificación de 7 variedades de frijol seco (`Class`) a partir de 16 características geométricas extraídas de imágenes.
Dataset: [Dry Bean Dataset, UCI](https://archive.ics.uci.edu/dataset/602/dry+bean+dataset) (13.611 instancias, 16 características, 7 clases).

Proyecto de equipo de la UAO. Enunciado y plan de equipo en [`docs/`](docs/).

## Estado del proyecto

| Sprint | Alcance | Estado |
|---|---|---|
| 1 · Comprensión y preparación | Ingesta, calidad de datos, EDA, split train/test | Hecho |
| 2 · Modelado y evaluación | Logistic Regression, Random Forest, métricas, matriz de confusión | Hecho (en revisión) |
| 3 · Despliegue y documentación | Modelo `.joblib`, entrenamiento y predicción reproducibles, reporte final, presentación | ML Engineer: hecho (en revisión). Reporte final (secciones 1 y 7) y presentación: en curso |

Registro de planes y decisiones: [`docs/bitacora/`](docs/bitacora/).

## Estructura del repositorio (TDSP)

```
laboratorio_drybean_ml/
├── data/
│   ├── raw/                 # dato original, sin modificar
│   └── processed/           # dry_bean_clean.csv, train.csv, test.csv
├── docs/                    # enunciado, plan de equipo, diccionario de datos
│   ├── bitacora/            # planes y reportes por sprint
│   ├── reporte/             # secciones del reporte final (una por rol)
│   └── presentacion/        # guion de láminas
├── notebooks/               # 01 EDA · 02 modelado · 03 análisis de errores · 04 modelo final y despliegue
├── outputs/
│   ├── models/              # modelo final (.joblib) y su metadata (.json)
│   └── reports/             # gráficas, métricas y resúmenes
├── src/                     # data_loader, preprocessing, quality, make_dataset, models, evaluate, error_analysis, train, predict
├── tests/                   # pruebas con pytest (unitarias y una de red)
├── requirements.txt
└── README.md
```

## Cómo reproducir

**Requiere Python 3.12 o superior** (verificado con 3.12 y 3.13). Con 3.10 u 3.11 no se pueden instalar las dependencias fijadas: `numpy 2.5.4` exige Python 3.12 o superior.

```powershell
# 1. Entorno virtual (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Pruebas
python -m pytest

# 3. Generar datos procesados (descarga de UCI la primera vez)
python -m src.make_dataset

# 4. Entrenar y guardar el modelo final (outputs/models/)
python -m src.train

# 5. Notebooks (01 EDA, 02 modelado, 03 errores, 04 modelo final)
jupyter notebook notebooks/
```

En Linux o macOS la activación es `source .venv/bin/activate`.

**Pruebas sin internet.** La prueba que descarga el dataset real lleva el marcador `network` y se omite sola, con un aviso, si UCI no es accesible; el resto corre siempre. Para forzar la omisión: `DRYBEAN_SKIP_NETWORK=1 python -m pytest`. Para ejecutar solo esa prueba: `python -m pytest -m network`.

**Notebooks.** Ejecútalos con el kernel del `.venv` (un kernel de otro Python, p. ej. Anaconda, cambia los resultados). Cada notebook imprime las versiones de Python y scikit-learn con las que se obtuvieron.

## Datos

| Archivo | Contenido | Filas |
|---|---|---|
| `data/raw/dry_bean_raw.csv` | Dato original de UCI | 13.611 |
| `data/processed/dry_bean_clean.csv` | Sin duplicados | 13.543 |
| `data/processed/train.csv` | 80 % estratificado | 10.834 |
| `data/processed/test.csv` | 20 % estratificado | 2.709 |

Decisiones de preparación (trazabilidad TDSP):

- **Duplicados:** se eliminan 68 filas idénticas (todas de la clase `HOROZ`) para evitar fuga de datos entre train y test.
- **Nulos:** no hay. La limpieza falla con error si aparecen, en vez de imputar en silencio.
- **Outliers:** no se eliminan. Son mediciones físicas reales de los granos. El conteo IQR pasa de 7.139 a 7.152 al quitar duplicados (−35 que estaban en las filas repetidas, +48 por recalcular cuartiles); explicación en el notebook 01, sección 5.1.
- **Split:** 80/20, `random_state=42`, estratificado por `Class`.
- **Escalado:** `StandardScaler` (`build_preprocessor()` en `src/preprocessing.py`), pensado para ir dentro del `Pipeline` del modelo y ajustarse solo con train.
- **Variables:** significado y fórmulas en [`docs/diccionario_datos.md`](docs/diccionario_datos.md).

### Hallazgos del EDA relevantes para el modelado

- Clases desbalanceadas: `DERMASON` 3.546 vs. `BOMBAY` 522 (razón 6,8). Métrica principal: **F1 macro**.
- Colinealidad muy alta entre variables de tamaño (`Area`–`ConvexArea` ≈ 1,00, `Perimeter`–`EquivDiameter` ≈ 0,99) y entre `Compactness`–`ShapeFactor3` ≈ 1,00.

## Modelado y resultados (Sprint 2)

Notebook: [`notebooks/02_modelado_evaluacion.ipynb`](notebooks/02_modelado_evaluacion.ipynb). Código en `src/models.py` y `src/evaluate.py`. Las decisiones se toman con validación cruzada sobre train; el test solo informa el desempeño.

| Modelo | Accuracy (test) | F1 macro (test) | F1 macro CV |
|---|---|---|---|
| Logistic Regression (baseline) | 0,9195 | 0,9306 | 0,9365 ± 0,0037 |
| Random Forest | 0,9195 | 0,9310 | 0,9343 ± 0,0047 |
| Random Forest ajustado | 0,9192 | 0,9308 | 0,9354 ± 0,0043 |

Estos tres son equivalentes entre sí (la diferencia es menor que la desviación entre pliegues). Los errores se concentran en `DERMASON` ↔ `SIRA` (43 % del total). Detalle en [`docs/bitacora/2026-11-12_04_reporte-sprint-2.md`](docs/bitacora/2026-11-12_04_reporte-sprint-2.md). *La elección del modelo final se revisó en el Sprint 3 (sección siguiente).*

Para ejecutar el notebook con las versiones fijadas del `.venv` (un kernel de otro Python, p. ej. Anaconda, cambia los resultados):

```powershell
$env:JUPYTER_PATH = "$PWD\.venv\share\jupyter"
jupyter nbconvert --to notebook --execute --inplace notebooks/02_modelado_evaluacion.ipynb
```

## Modelo final y despliegue (Sprint 3)

Notebook: [`notebooks/04_modelo_final_y_despliegue.ipynb`](notebooks/04_modelo_final_y_despliegue.ipynb). Código en `src/train.py` y `src/predict.py`.

El diagnóstico del repositorio pidió probar SVM y Gradient Boosting con el mismo protocolo antes de cerrar la elección. Validación cruzada **anidada** de 5 pliegues sobre train, con los mismos pliegues para todos:

| Modelo | F1 macro CV | Diferencia vs. logreg | Pliegues ganados |
|---|---|---|---|
| Logistic Regression | 0,9365 ± 0,0037 | — | — |
| Random Forest | 0,9343 ± 0,0047 | −0,0022 | 1 de 5 |
| **SVM RBF** | **0,9432 ± 0,0049** | **+0,0068** | **5 de 5** |
| Gradient Boosting | 0,9405 ± 0,0033 | +0,0041 | 5 de 5 |

Con la regla del equipo la regresión logística ya no es equivalente al mejor; Gradient Boosting sí lo es y se elige el más simple: **SVM RBF** (`C=100`, `gamma=0,01`). En test: accuracy **0,9232**, F1 macro **0,9342**, peor recall **0,871** (`SIRA`), con lo que cumple el criterio propuesto (F1 macro ≥ 0,92 y recall mínimo ≥ 0,85). La mejora es pequeña pero consistente, y la SVM es menos interpretable que la regresión logística: es una decisión que debe validar el Product Owner (si prefiere interpretabilidad, `python -m src.train --model logreg` lo reemplaza y también cumple el criterio).

```powershell
# Reentrenar y guardar el modelo final (Pipeline completo + metadata)
python -m src.train

# Predecir granos nuevos desde un CSV con las 16 variables
python -m src.predict --input nuevos_granos.csv --output predicciones.csv
```

El modelo (`outputs/models/modelo_final_drybean.joblib`, 413 KB) se versiona junto con `modelo_final_metadata.json` (hiperparámetros, métricas, versiones de las librerías, variables y clases). `joblib` es sensible a la versión de scikit-learn: `load_model` avisa si no coincide con la del entrenamiento.

## Uso desde código

```python
from src.predict import load_model, predict_bean_class, predict_beans

modelo = load_model()                       # outputs/models/modelo_final_drybean.joblib
predict_bean_class(modelo, {"Area": 40512, "Perimeter": 737.6, ...})   # un grano (dict, Series o DataFrame)
predict_beans(modelo, datos_nuevos)         # varias filas -> array de variedades
```

Valida que estén las 16 variables (en cualquier orden), rechaza valores nulos e ignora columnas extra.

## Metodología y equipo

- **CRISP-DM:** estructura las fases del proyecto.
- **TDSP:** estructura del repo, reproducibilidad y trazabilidad.
- **Scrum ML:** backlog, sprints y Definition of Done en [`docs/Plan_Equipos_ScrumML_DryBean.pdf`](docs/Plan_Equipos_ScrumML_DryBean.pdf).

| Rol | Responsabilidad |
|---|---|
| Product Owner | Objetivos y priorización |
| Scrum Master | Coordinación y tablero |
| Data Engineer / Analyst | Datos limpios y EDA |
| ML Engineer | Modelos y métricas |

## Flujo de trabajo con Git

1. Una rama por tarea: `git checkout -b feature/nombre-rama`.
2. Commits pequeños con mensaje claro.
3. `git push origin feature/nombre-rama` y abrir un Pull Request a `main`.
4. Otra persona del equipo revisa y aprueba antes del merge.
5. `git pull origin main` antes de empezar a trabajar.
