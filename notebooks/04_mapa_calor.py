%pip install folium

import folium
from pyspark.sql.functions import *

# Leer la capa Gold
df = spark.table("workspace.default.gold_heatmap")

# Tomar muestra para el mapa
df_sample = df.filter(col("color") != "unknown").sample(0.001).toPandas()

# Crear mapa centrado en Chicago
mapa = folium.Map(location=[41.85, -87.65], zoom_start=13)

# Colores
color_map = {"green": "#00cc00", "yellow": "#ffcc00", "red": "#ff0000"}

# Agregar puntos
for _, row in df_sample.iterrows():
    folium.CircleMarker(
        location=[row["START_LATITUDE"], row["START_LONGITUDE"]],
        radius=3,
        color=color_map.get(row["color"], "gray"),
        fill=True,
        fill_opacity=0.6
    ).add_to(mapa)

# Mostrar
displayHTML(mapa._repr_html_())
