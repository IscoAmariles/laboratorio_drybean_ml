# Guion de láminas: datos y análisis de errores

*Data Engineer / Analyst. Seis láminas, unos 6 minutos. Cada lámina usa una figura que ya existe en `outputs/reports/`.*

| # | Título (mensaje) | Contenido | Figura |
|---|---|---|---|
| 1 | **Los datos: 13.611 granos, 7 variedades, 16 medidas** | Origen UCI; medidas de tamaño y forma tomadas por visión por computador; problema: clasificar la variedad para automatizar el control de calidad | — |
| 2 | **Las clases están desbalanceadas** | DERMASON 3.546 frente a BOMBAY 522 (6,8 veces). Por eso la métrica es F1 macro y la división es estratificada | `distribucion_clases.png` |
| 3 | **Calidad: limpios salvo 68 duplicados** | 0 nulos; 68 duplicados, todos HOROZ, eliminados para evitar fuga; atípicos conservados porque son mediciones reales | `boxplots_por_clase.png` |
| 4 | **Las medidas de tamaño se repiten entre sí** | Correlación ≈ 1,00 entre `Area` y `ConvexArea`; relevante para interpretar la regresión logística | `matriz_correlacion.png` |
| 5 | **¿Dónde se equivoca el modelo?** | 218 errores en 2.709 granos (8 %); DERMASON↔SIRA son el 43 %; Random Forest comete los mismos 218. SIRA es la clase más débil (F1 0,872) | `matriz_confusion_normalizada_logreg.png` |
| 6 | **Por qué: se parecen en tamaño** | Los DERMASON mal clasificados son más grandes de lo normal y los SIRA más pequeños; la forma es casi idéntica. Cada par de confusión tiene su variable (tamaño, redondez, alargamiento). Riesgo: un cambio de cámara afectaría justo a esta pareja | `errores_dermason_sira_area.png` |

**Notas para quien presente**
- En la lámina 5, mostrar la matriz normalizada, no la de conteos: BOMBAY tiene 104 granos de prueba y DERMASON 709.
- Si preguntan "¿por qué no un modelo más potente?": un Random Forest no baja ni cambia los errores; el límite está en el solapamiento de clases. Hay una exploración preliminar con SVM y boosting en la bitácora 06, aún no confirmada.
