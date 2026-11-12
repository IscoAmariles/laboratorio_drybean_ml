# Laboratorio Dry Bean · Machine Learning con CRISP-DM + TDSP + Scrum ML

Clasificación de 7 variedades de frijol seco (`Class`) a partir de 16 características geométricas extraídas de imágenes.
Dataset: [Dry Bean Dataset, UCI](https://archive.ics.uci.edu/dataset/602/dry+bean+dataset) (13.611 instancias, 16 características, 7 clases).

Proyecto de equipo de la UAO. Enunciado y plan de equipo en [`docs/`](docs/).

## Estado del proyecto

| Sprint | Alcance | Estado |
|---|---|---|
| 1 · Comprensión y preparación | Ingesta, calidad de datos, EDA, split train/test | Hecho |
| 2 · Modelado y evaluación | Logistic Regression, Random Forest, métricas, matriz de confusión | Pendiente |
| 3 · Despliegue y documentación | Modelo `.joblib`, README final, presentación | Pendiente |

Registro de planes y decisiones: [`docs/bitacora/`](docs/bitacora/).

## Estructura del repositorio (TDSP)

```
laboratorio_drybean_ml/
├── data/
│   ├── raw/                 # dato original, sin modificar
│   └── processed/           # dry_bean_clean.csv, train.csv, test.csv
├── docs/                    # enunciado, plan de equipo, diccionario de datos
│   └── bitacora/            # planes y reportes por sprint
├── notebooks/               # 01_comprension_preparacion_datos.ipynb
├── outputs/
│   ├── models/              # modelos entrenados (.joblib)
│   └── reports/             # gráficas y resúmenes de calidad
├── src/                     # código reutilizable (data_loader, preprocessing, quality, make_dataset)
├── tests/                   # pruebas con pytest
├── requirements.txt
└── README.md
```

## Cómo reproducir

Requiere Python 3.10 o superior (desarrollado con 3.13).

```powershell
# 1. Entorno virtual (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Pruebas
python -m pytest

# 3. Generar datos procesados (descarga de UCI la primera vez)
python -m src.make_dataset

# 4. Notebook de EDA
jupyter notebook notebooks/01_comprension_preparacion_datos.ipynb
```

En Linux o macOS la activación es `source .venv/bin/activate`.

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
- **Outliers:** no se eliminan. Son mediciones físicas reales de los granos.
- **Split:** 80/20, `random_state=42`, estratificado por `Class`.
- **Escalado:** `StandardScaler` (`build_preprocessor()` en `src/preprocessing.py`), pensado para ir dentro del `Pipeline` del modelo y ajustarse solo con train.
- **Variables:** significado y fórmulas en [`docs/diccionario_datos.md`](docs/diccionario_datos.md).

### Hallazgos del EDA relevantes para el modelado

- Clases desbalanceadas: `DERMASON` 3.546 vs. `BOMBAY` 522 (razón 6,8). Métrica principal: **F1 macro**.
- Colinealidad muy alta entre variables de tamaño (`Area`–`ConvexArea` ≈ 1,00, `Perimeter`–`EquivDiameter` ≈ 0,99) y entre `Compactness`–`ShapeFactor3` ≈ 1,00.

## Uso desde código

```python
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from src.preprocessing import build_preprocessor

train = pd.read_csv("data/processed/train.csv")
test = pd.read_csv("data/processed/test.csv")
X_train, y_train = train.drop(columns="Class"), train["Class"]
X_test, y_test = test.drop(columns="Class"), test["Class"]

modelo = Pipeline([("scaler", build_preprocessor()),
                   ("clf", LogisticRegression(max_iter=1000, random_state=42))])
```

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
