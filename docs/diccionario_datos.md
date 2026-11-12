# Diccionario de datos · Dry Bean Dataset

Fuente: [UCI Machine Learning Repository, id 602](https://archive.ics.uci.edu/dataset/602/dry+bean+dataset). Cada fila es un grano de frijol fotografiado y segmentado por visión por computador. Las medidas de longitud y área están en **píxeles**.

Notación de las fórmulas: A = `Area`, P = `Perimeter`, L = `MajorAxisLength`, l = `MinorAxisLength`, C = `ConvexArea`, Ed = `EquivDiameter`.

## Variable objetivo

| Variable | Tipo | Descripción |
|---|---|---|
| `Class` | Categórica (7) | Variedad del frijol: `BARBUNYA`, `BOMBAY`, `CALI`, `DERMASON`, `HOROZ`, `SEKER`, `SIRA` |

## Características (16, todas numéricas)

### Tamaño

| Variable | Tipo | Descripción |
|---|---|---|
| `Area` | int, px² | Número de píxeles dentro de los límites del grano |
| `Perimeter` | float, px | Longitud del borde del grano |
| `MajorAxisLength` | float, px | Distancia entre los extremos de la línea más larga que se puede trazar en el grano |
| `MinorAxisLength` | float, px | Línea más larga perpendicular al eje mayor |
| `ConvexArea` | int, px² | Píxeles del polígono convexo más pequeño que contiene el grano |
| `EquivDiameter` | float, px | Diámetro de un círculo con la misma área que el grano: √(4A/π) |

### Forma

| Variable | Tipo | Descripción |
|---|---|---|
| `AspectRatio` | float | Relación de aspecto: L / l |
| `Eccentricity` | float | Excentricidad de la elipse con los mismos momentos que la región |
| `Extent` | float | Razón entre el área del grano y la de su caja delimitadora |
| `Solidity` | float | Convexidad: A / C |
| `Roundness` | float | Redondez: 4πA / P² |
| `Compactness` | float | Compacidad: Ed / L |
| `ShapeFactor1` | float | L / A |
| `ShapeFactor2` | float | l / A |
| `ShapeFactor3` | float | A / ((L/2)² · π) |
| `ShapeFactor4` | float | A / ((L/2) · (l/2) · π) |

## Relaciones entre variables

Varias características son derivadas de otras, por eso hay colinealidad alta (ver matriz en `outputs/reports/matriz_correlacion.png`):

- Tamaño: `Area`, `ConvexArea`, `EquivDiameter` y `Perimeter` se mueven casi juntas.
- `Compactness` y `ShapeFactor3` son casi equivalentes (correlación ≈ 1,00).
- `Solidity` y `ConvexArea` se calculan a partir de `Area`.

## Calidad (datos crudos)

| Aspecto | Resultado |
|---|---|
| Filas × columnas | 13.611 × 17 |
| Nulos | 0 |
| Duplicados | 68 (todos de `HOROZ`) |
| Outliers (regla IQR 1,5) | 7.139 valores en total; son mediciones reales y no se eliminan |

Detalle: `outputs/reports/resumen_calidad_datos.csv`.
