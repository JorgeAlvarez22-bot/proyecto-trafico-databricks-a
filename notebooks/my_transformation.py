import dlt
from pyspark.sql.functions import *

# =====================
# CAPA BRONZE
# =====================
@dlt.table(
    name="bronze_traffic",
    comment="Ingesta cruda de CSVs de tráfico de Chicago"
)
def bronze_traffic():
    return (
        spark.readStream
            .format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("header", "true")
            .option("inferSchema", "true")
            .load("/Volumes/workspace/default/trafico_raw/")
    )


# =====================
# CAPA SILVER
# =====================
@dlt.table(
    name="silver_traffic",
    comment="Fechas transformadas a formato válido"
)
def silver_traffic():
    return (
        dlt.read_stream("bronze_traffic")
            .withColumn(
                "timestamp_clean",
                to_timestamp(col("TIME"), "MM/dd/yyyy hh:mm:ss a")
            )
            .withColumn("hora", hour(col("timestamp_clean")))
            .withColumn("fecha", to_date(col("timestamp_clean")))
            .drop("TIME")
    )


# =====================
# CAPA GOLD
# =====================
@dlt.table(
    name="gold_heatmap",
    comment="Coordenadas y color predominante por hora para mapa de calor"
)
def gold_heatmap():
    return (
        dlt.read("silver_traffic")
            .withColumn(
                "color",
                when(col("SPEED") >= 20, "green")
                .when((col("SPEED") >= 10) & (col("SPEED") < 20), "yellow")
                .when(col("SPEED") >= 0, "red")
                .otherwise("unknown")
            )
            .select(
                "timestamp_clean",
                "fecha",
                "hora",
                "START_LATITUDE",
                "START_LONGITUDE",
                "color"
            )
    )
