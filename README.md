# Cancelaciones de Reservas Hoteleras — ¿Las Peticiones Especiales Reducen la Cancelación?

**Curso:** Programación y Análisis Reproducible de Datos  
**Dataset:** [Hotel Reservations Dataset](https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset) · Kaggle · Licencia CC0  
**Pregunta de análisis:** ¿Existe una relación de dependencia estadística entre el número de peticiones especiales realizadas por un huésped y la probabilidad de cancelación de su reserva, y cómo modera el precio promedio de la habitación esta relación?

---

## Estructura del proyecto

```
hotel-cancelaciones/
├── data/
│   ├── raw/                  # Dataset original sin modificar (no se sube a GitHub)
│   │   └── hotel_reservations.csv
│   └── processed/            # Datos limpios y enriquecidos
│       └── hotel_clean.csv
├── notebooks/
│   └── analisis_principal.ipynb   # Notebook principal con todo el análisis
├── src/
│   └── features.py           # Funciones de Feature Engineering reutilizables
├── reports/                  # Gráficos exportados (opcional)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Reproducción del análisis

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/hotel-cancelaciones.git
cd hotel-cancelaciones
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Descargar el dataset

Descarga el archivo `Hotel Reservations.csv` desde:  
[https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset](https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset)

Guárdalo en `data/raw/hotel_reservations.csv`.

> El dataset no se incluye en el repositorio por tamaño. Es de uso libre (licencia CC0).

### 4. Ejecutar el notebook

```bash
jupyter notebook notebooks/analisis_principal.ipynb
```

Ejecutar todas las celdas en orden (Kernel → Restart & Run All).

---

## Descripción del dataset

| Atributo | Descripción |
|---|---|
| Fuente | Kaggle — Ahsan Raza |
| Registros | 36,275 |
| Variables | 19 |
| Target | `booking_status` (Canceled / Not_Canceled) |
| Tasa de cancelación | ~33% |
| Período aproximado | No especificado (datos sintéticos basados en patrones reales) |

### Variables clave del análisis

- `no_of_special_requests`: número de peticiones especiales del huésped (0–5)
- `avg_price_per_room`: precio promedio de la habitación (EUR/noche)
- `lead_time`: días de antelación entre reserva y llegada
- `market_segment_type`: canal de reserva (Online, Offline, Corporate, Aviation, Complementary)
- `booking_status`: variable objetivo (cancelada o no)

---

## Metodología

El análisis sigue el flujo estándar de un proyecto de ciencia de datos reproducible:

1. **Exploración inicial** — dimensiones, tipos, estadísticos descriptivos
2. **Limpieza y transformación** — validación de nulos, duplicados, tipos; creación de variables derivadas
3. **Join** — cruce con tabla de comisiones OTA por `market_segment_type`
4. **Feature Engineering** — variables derivadas orientadas a modelos futuros
5. **EDA** — 5+ visualizaciones con interpretaciones; gráfico interactivo con Plotly
6. **Análisis estadístico** — prueba Chi-cuadrado + Regresión Logística (statsmodels)
7. **Conclusiones** — respuesta a la pregunta, limitaciones, recomendaciones

---

## Dependencias principales

Ver `requirements.txt`. Las librerías principales son:

- `pandas`, `numpy` — manipulación de datos
- `matplotlib`, `seaborn` — visualización estática
- `plotly` — visualización interactiva
- `scipy` — pruebas estadísticas
- `statsmodels` — regresión logística con interpretación de coeficientes
- `jupyter` — entorno de notebooks

---

## Uso documentado de IA

Se utilizó Claude (Anthropic) como asistente durante el desarrollo. El detalle completo de qué se solicitó, qué se recibió y qué ajustes se realizaron manualmente se encuentra en la **Sección 6** del notebook.

---

## Licencia

Código bajo licencia MIT. Dataset bajo CC0 (dominio público).
