# 🚦 Arquitectura Medallion en Databricks — Tráfico Chicago

Proyecto final de la materia de Big Data. Implementación de una arquitectura Medallion en Databricks usando datos reales de tráfico de la ciudad de Chicago, con un pipeline ETL completo y dos capas de resultados: mapa de calor interactivo y chat con LLM.

---

## Descripción

Se construyó un pipeline de datos en **Delta Live Tables (DLT)** con tres capas de transformación (Bronze, Silver, Gold) sobre 4 millones de registros del dataset público **Chicago Traffic Tracker**, que monitorea la velocidad en más de 1,000 segmentos de arterias viales de Chicago cada 10 minutos.

El proyecto incluye dos capas de resultados:
1. **Mapa de calor interactivo** que muestra las condiciones de tráfico por ubicación geográfica clasificadas por color
2. **Chat con LLM** (Claude API) que permite hacer preguntas en lenguaje natural sobre los datos de tráfico

---

## Arquitectura

```
CSVs Chicago Traffic Tracker
        |
        v
  [BRONZE] Streaming Table
  Ingesta cruda de los CSVs sin transformaciones
        |
        v
  [SILVER] Streaming Table
  Transformación de fechas a timestamp válido
  Extracción de columnas: hora, fecha
  Filtrado de registros nulos
        |
        v
  [GOLD] Tabla Delta
  Coordenadas + color por velocidad (verde/amarillo/rojo)
  Filtrado de registros inválidos
        |
        v
  Mapa de calor (Folium)     Chat con LLM (Claude API)
```

### Criterios de color por velocidad

| Color | Velocidad | Condición |
|-------|-----------|-----------|
| 🟢 Verde | >= 40 mph | Tráfico fluido |
| 🟡 Amarillo | 20–39 mph | Tráfico moderado |
| 🔴 Rojo | 0–19 mph | Tráfico congestionado |

---

## Dataset

- **Fuente:** [Chicago Traffic Tracker — City of Chicago Data Portal](https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/sxs8-h27x)
- **Registros:** 4,000,000
- **Período:** 2022 (primera mitad del año)
- **Columnas principales:** `TIME`, `SPEED`, `START_LATITUDE`, `START_LONGITUDE`, `SEGMENT_ID`

---

## Tecnologías

| Herramienta | Uso |
|-------------|-----|
| Databricks (AWS) | Plataforma principal de cómputo y almacenamiento |
| Delta Live Tables (DLT) | Orquestación del pipeline Medallion |
| Apache Spark / PySpark | Procesamiento distribuido de datos |
| Unity Catalog | Gestión de tablas y volúmenes |
| Delta Lake | Formato de almacenamiento transaccional |
| Folium | Mapa de calor interactivo |
| Claude API (Anthropic) | Chat con LLM sobre los datos de tráfico |
| Python 3 | Lenguaje de desarrollo |

---

## Estructura del repositorio

```
proyecto-trafico-databricks/
├── README.md
└── notebooks/
    ├── my_transformation.py    # Pipeline DLT: Bronze + Silver + Gold
    ├── 04_mapa_calor.py        # Mapa de calor interactivo con Folium
    └── 05_chat_trafico.py      # Chat con LLM usando Claude API
```

---

## Cómo ejecutar

### 1. Subir los datos

Descargar el dataset desde el portal de Chicago con esta URL:

```
https://data.cityofchicago.org/resource/sxs8-h27x.csv?$query=SELECT * WHERE TIME >= '2022-01-01T00:00:00' AND TIME <= '2022-06-30T23:59:59' LIMIT 4000000
```

Subir el CSV a Databricks en: `Catalog → workspace → default → trafico_raw`

### 2. Correr el pipeline Medallion

1. Ir a **Jobs & Pipelines** en Databricks
2. Abrir el pipeline ETL
3. Hacer clic en el menú junto a "Start" y seleccionar **"Full refresh all"**
4. Esperar a que completen las tres capas (Bronze → Silver → Gold)

### 3. Ver el mapa de calor

1. Abrir el notebook `04_mapa_calor.py` en Databricks
2. Conectar al cluster
3. Correr todas las celdas en orden
4. El mapa interactivo aparece al final del notebook

### 4. Usar el chat con LLM

1. Abrir el notebook `05_chat_trafico.py` en Databricks
2. Ingresar tu API key de Anthropic en la variable `ANTHROPIC_API_KEY`
3. Correr todas las celdas con **Run All**
4. Llamar a la función `preguntar("tu pregunta aquí")` con cualquier consulta

**Ejemplos de preguntas:**
```python
preguntar("¿En qué hora del día hay más tráfico rojo?")
preguntar("¿Cuántos registros hay por color de tráfico?")
preguntar("¿Cuáles son las coordenadas con más tráfico rojo?")
```

---

## Resultados

- **77%** de los registros corresponden a tráfico amarillo (moderado)
- **19%** a tráfico rojo (congestionado)
- **4%** a tráfico verde (fluido)
- La hora con más congestión es las **17:00 hrs (5 PM)** con 31,263 registros rojos

---

## Equipo

- Jorge Alejandro Alvarez Sutti
- Alejandro Gutierrez Romo

