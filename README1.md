# 🚦 Arquitectura Medallion en Databricks — Tráfico Chicago

Proyecto final de la materia de Big Data. Implementación de una arquitectura Medallion en Databricks usando datos reales de tráfico de la ciudad de Chicago.

## 📋 Descripción

Se construyó un pipeline de datos en **Delta Live Tables (DLT)** con tres capas de transformación (Bronze, Silver, Gold) sobre 4 millones de registros del dataset público **Chicago Traffic Tracker**, que monitorea la velocidad en más de 1,000 segmentos de arterias viales de Chicago cada 10 minutos.

El resultado final es un **mapa de calor interactivo** que muestra las condiciones de tráfico por ubicación geográfica, clasificadas por color (verde, amarillo, rojo).

---

## 🗂️ Arquitectura

    CSVs Chicago Traffic Tracker
            ↓
      [BRONZE] Streaming Table
      Ingesta cruda de los CSVs sin transformaciones
            ↓
      [SILVER] Streaming Table
      Transformación de fechas a formato timestamp válido
      Extracción de hora y fecha
            ↓
      [GOLD] Materialized View
      Coordenadas + color predominante por datetime
            ↓
      Mapa de calor interactivo (Folium en Databricks)

---

## 📊 Dataset

- **Fuente:** [Chicago Traffic Tracker — City of Chicago Data Portal](https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/sxs8-h27x)
- **Registros:** 4,000,000
- **Período:** 2022
- **Columnas principales:** `TIME`, `SPEED`, `START_LATITUDE`, `START_LONGITUDE`, `SEGMENT_ID`

---

## 🛠️ Tecnologías

| Herramienta | Uso |
|---|---|
| Databricks (AWS) | Plataforma principal |
| Delta Live Tables | Pipeline Medallion |
| Apache Spark / PySpark | Procesamiento de datos |
| Unity Catalog | Almacenamiento en Volumes y tablas |
| Folium | Visualización del mapa de calor |
| Python | Lenguaje de desarrollo |

---

## 📁 Estructura del repositorio

    proyecto-trafico-databricks/
    ├── README.md
    └── notebooks/
        ├── my_transformation.py   # Pipeline DLT: Bronze + Silver + Gold
        └── 04_mapa_calor.py       # Mapa de calor interactivo

---

## 🚀 Cómo ejecutar

### 1. Subir los datos

Descargar el dataset desde el portal de Chicago con este link:

    https://data.cityofchicago.org/resource/sxs8-h27x.csv?$query=SELECT * WHERE TIME >= '2022-01-01T00:00:00' AND TIME <= '2022-06-30T23:59:59' LIMIT 4000000

Subir el CSV a `Catalog → workspace → default → trafico_raw` en Databricks.

### 2. Correr el pipeline

- En Databricks ir a **Jobs & Pipelines → ETL Pipeline**
- Seleccionar el notebook `my_transformation.py`
- Configurar destino: catalog `workspace`, schema `default`
- Dar clic en **Run pipeline**

### 3. Ver el mapa

- Abrir el notebook `04_mapa_calor.py` en Databricks
- Correr todas las celdas
- El mapa interactivo aparece al final

---

## 👥 Equipo

- Jorge Alejandro Alvarez Sutti
- Alejandro Gutierrez Romo
