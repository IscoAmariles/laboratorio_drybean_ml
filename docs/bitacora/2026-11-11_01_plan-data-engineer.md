> **Bitácora 01 · 2026-11-11** · Plan de trabajo del rol Data Engineer / Analyst.
> Estado: **aprobado y ejecutado (Sprint 1)**. Resultado en [2026-11-11_02_reporte-sprint-1.md](2026-11-11_02_reporte-sprint-1.md).

# Plan de trabajo: Data Engineer / Analyst, proyecto Dry Bean ML

## Contexto
El proyecto es el laboratorio de ML de la UAO ([docs/Lab1.pdf](docs/Lab1.pdf)). Consiste en clasificar 7 variedades de frijol seco del **Dry Bean Dataset** (UCI id=602: 13.611 filas, 16 features numéricas, objetivo `Class`) aplicando **CRISP-DM + TDSP + Scrum ML**. El equipo tiene 4 roles ([docs/Plan_Equipos_ScrumML_DryBean.pdf](docs/Plan_Equipos_ScrumML_DryBean.pdf)): Product Owner, Scrum Master, **Data Engineer / Analyst (tú)** y ML Engineer.

**Tu responsabilidad según el plan del equipo:** preparación y limpieza de datos. **Tus entregables:** dataset limpio y análisis exploratorio. **Tus historias del backlog:** PB-01 (descargar dataset, prioridad alta) y PB-02 (analizar calidad de datos, prioridad alta). También participas en PB-05 (comparar métricas, todo el equipo).

Estado actual del repo: Git ya está conectado a `github.com/IscoAmariles/laboratorio_drybean_ml` (rama `main`). Existen `data/`, `notebooks/`, `outputs/` y `src/` (vacías, con `.gitkeep`). `README.md`, `requirements.txt` y `.gitignore` están vacíos. Faltan las subcarpetas TDSP `data/raw`, `data/processed`, `outputs/models` y `outputs/reports`.

Tu trabajo es la base del proyecto: el ML Engineer no puede empezar hasta que entregues el split train/test y el pipeline de preprocesamiento.

---

## SPRINT 1: Comprensión y preparación (aquí está el grueso de tu rol)

### 1. Configuración del repo y del entorno (con el Scrum Master)
1.1. Crear la estructura TDSP completa: `data/raw/`, `data/processed/`, `outputs/models/`, `outputs/reports/` (con `.gitkeep`).
1.2. Llenar `requirements.txt` con versiones fijas: `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `ucimlrepo`, `joblib`, `openpyxl`, `jupyter`, `seaborn` (opcional).
1.3. Llenar `.gitignore` con: `.venv/`, `__pycache__/`, `.ipynb_checkpoints/` y `outputs/models/*.joblib` (decidir con el equipo si el modelo se sube).
1.4. Crear el entorno virtual:
   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
1.5. Agregar a los 3 compañeros como colaboradores en GitHub (Settings → Collaborators).
1.6. Trabajar siempre en ramas: `git checkout -b feature/data-ingesta`, abrir un PR hacia `main` y pedir revisión antes del merge.

### 2. PB-01: Ingesta de datos (CRISP-DM fase 2, Pasos 2-3 del lab)
2.1. Crear `src/data_loader.py` con la función `load_raw_data()`. Esta función:
   - descarga con `fetch_ucirepo(id=602)`;
   - concatena `features` + `targets` en un solo `df`;
   - guarda una copia sin modificar en `data/raw/dry_bean_raw.csv`;
   - si el CSV ya existe, lo lee de disco (así no depende de internet y es reproducible).
2.2. **Criterio de aceptación:** el dataframe carga sin errores y `df.shape == (13611, 17)`.
2.3. Responder las preguntas del Paso 3: ¿cuántas columnas tiene? (17), ¿cuál es el objetivo? (`Class`), ¿es clasificación o regresión? (clasificación multiclase, 7 clases).

### 3. PB-02: Calidad de datos y EDA (CRISP-DM fase 2, Pasos 4-6)
Notebook: `notebooks/01_comprension_preparacion_datos.ipynb`
3.1. Revisar `df.shape`, `df.info()` y `df.describe()`. Documentar los tipos de datos (todas las features son numéricas; `Class` es la única categórica).
3.2. Contar nulos con `df.isna().sum()` (se espera 0).
3.3. Contar duplicados con `df.duplicated().sum()` (se esperan ~68). Decisión: eliminarlos con `drop_duplicates()` y documentar el porqué.
3.4. Distribución de clases: hacer `value_counts()` y un gráfico de barras, guardado en `outputs/reports/distribucion_clases.png`. Responder si las clases están balanceadas: **no lo están** (BOMBAY es minoritaria y DERMASON mayoritaria). Explicar el impacto y por qué conviene usar F1 macro y `stratify`.
3.5. EDA adicional (aporte de analista, suma puntos en la rúbrica):
   - histogramas o boxplots por variable para ver distribución y outliers (método IQR);
   - boxplots de las features clave por clase (`Area`, `Perimeter`, `MajorAxisLength`, `Compactness`, `ShapeFactor*`);
   - matriz de correlación (heatmap). Esperar alta colinealidad entre las variables de tamaño (`Area`, `ConvexArea`, `EquivDiameter`, `Perimeter`); anotarla como insumo para el ML Engineer.
3.6. Generar un **resumen de calidad** en `outputs/reports/resumen_calidad_datos.csv` o `.md`: filas, columnas, nulos, duplicados eliminados, outliers por variable y conteo por clase. Este archivo es el criterio de aceptación de PB-02.
3.7. Crear un **diccionario de datos** (`docs/diccionario_datos.md`): cada una de las 16 variables con su descripción (forma, tamaño o estructura del grano) y sus unidades.

### 4. Preparación de datos (CRISP-DM fase 3, Pasos 5, 7 y 8)
4.1. Crear `src/preprocessing.py` con estas funciones:
   - `clean_data(df)`: elimina duplicados y valida que no haya nulos;
   - `split_data(df, test_size=0.2, random_state=42)`: separa `X`/`y` y llama a `train_test_split(..., stratify=y)`;
   - `build_preprocessor()`: devuelve el `StandardScaler`, que el ML Engineer mete en el `Pipeline`.
4.2. Guardar los datos procesados:
   - `data/processed/dry_bean_clean.csv`;
   - `data/processed/train.csv` y `data/processed/test.csv` (con la columna `Class`).
4.3. Verificar que el split conserva las proporciones de clase (comparar `value_counts(normalize=True)` de train y test).
4.4. Documentar en el notebook y en el README las decisiones: semilla 42, test 20%, estratificación y eliminación de duplicados. Esto es trazabilidad TDSP.
4.5. **Handoff al ML Engineer:** abrir un PR con `src/` y `data/processed/`, y explicarle cómo importar `split_data()` o leer los CSV.

**Entregables Sprint 1:** dataset limpio, notebook inicial ejecutado, split train/test, pipeline de preprocesamiento y repo configurado.

---

## SPRINT 2: Modelado y evaluación (rol de soporte)
5.1. Responder las dudas de datos del ML Engineer y ajustar el preprocesamiento si hace falta.
5.2. **PB-05, comparar métricas (todo el equipo):** ayudar a armar la tabla comparativa de accuracy y F1 macro (LogReg vs. RandomForest) y guardarla en `outputs/reports/comparacion_modelos.csv`.
5.3. **Análisis de errores (rol analista):** con la matriz de confusión, identificar qué clases se confunden. Se espera SIRA ↔ DERMASON y BARBUNYA ↔ CALI. Explicar el porqué usando el EDA: los boxplots muestran que esas clases tienen tamaño y forma muy similares.
5.4. Interpretar la importancia de variables (Paso 15) y cruzarla con lo encontrado en el EDA. Aclarar que importancia no implica causalidad.
5.5. (Opcional) Extensión C: guardar `outputs/reports/predicciones_drybean.csv` con las columnas `real_class` y `predicted_class`, y analizar dónde falla el modelo.

---

## SPRINT 3: Despliegue y documentación
6.1. Escribir las secciones de datos del **reporte final** (Entregable 2):
   - 2. Comprensión de datos: tamaño, variables, clases y calidad;
   - 3. Preparación: transformaciones realizadas.
6.2. Aportar al README las secciones "Datos", "Cómo reproducir" (venv, `pip install -r requirements.txt`, ejecutar los notebooks en orden) y la estructura del repo.
6.3. Verificar la reproducibilidad: clonar el repo en una carpeta limpia, crear el venv y correr los notebooks de inicio a fin sin errores (DoD #1).
6.4. Aportar a la presentación las láminas de datos/EDA (gráfica de clases, calidad, correlaciones, hallazgos).
6.5. Aportar a la retrospectiva: qué funcionó, qué no funcionó y qué mejorarías.

---

## Scrum: actividades continuas
- Daily: responder ¿qué hice?, ¿qué haré? y ¿qué bloqueos tengo?
- Mantener tus tarjetas (PB-01, PB-02) al día en el tablero (Por hacer → En progreso → Hecho).
- Cada tarea se cierra solo cuando cumple su criterio de aceptación y está mergeada en `main` vía PR.

## Archivos que te corresponden
| Archivo | Propósito |
|---|---|
| `requirements.txt`, `.gitignore` | Entorno reproducible |
| `src/data_loader.py` | Ingesta (PB-01) |
| `src/preprocessing.py` | Limpieza, split y scaler |
| `notebooks/01_comprension_preparacion_datos.ipynb` | EDA + calidad + preparación |
| `data/raw/dry_bean_raw.csv` | Dato original inmutable |
| `data/processed/{dry_bean_clean,train,test}.csv` | Datos para modelado |
| `outputs/reports/*.png`, `resumen_calidad_datos.*` | Evidencia de EDA y calidad |
| `docs/diccionario_datos.md` | Documentación de variables |

## Verificación (tu parte del Definition of Done)
1. `pip install -r requirements.txt` funciona en un venv nuevo.
2. El notebook 01 corre de inicio a fin sin errores (Kernel → Restart & Run All).
3. Se reportan nulos (0) y duplicados (~68 eliminados).
4. `train.csv` + `test.csv` suman las filas del dataset limpio y las proporciones de clase coinciden.
5. El ML Engineer puede cargar los datos procesados y entrenar sin tocar tu código.
6. El PR está revisado y mergeado en `main`.

