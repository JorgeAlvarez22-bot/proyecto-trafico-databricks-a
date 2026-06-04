import dlt
from pyspark.sql.functions import *

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

@dlt.table(
    name="silver_traffic",
    comment="Fechas transformadas a formato válido"
)
def silver_traffic():
    return (
        dlt.read_stream("bronze_traffic")
            .withColumn(
                "timestamp_clean",
                coalesce(
                    to_timestamp(col("TIME"), "MM/dd/yyyy hh:mm:ss a"),
                    to_timestamp(col("TIME"), "MM/dd/yyyy HH:mm:ss"),
                    to_timestamp(col("TIME"))
                )
            )
            .withColumn("hora", hour(col("timestamp_clean")))
            .withColumn("fecha", to_date(col("timestamp_clean")))
            .filter(col("timestamp_clean").isNotNull())
            .drop("TIME")
    )

@dlt.table(
    name="gold_heatmap",
    comment="Coordenadas y color predominante por hora para mapa de calor"
)
def gold_heatmap():
    return (
        dlt.read("silver_traffic")
            .withColumn(
                "color",
                when(col("SPEED") >= 40, "green")
                .when((col("SPEED") >= 20) & (col("SPEED") < 40), "yellow")
                .when((col("SPEED") >= 0) & (col("SPEED") < 20), "red")
                .otherwise("unknown")
            )
            .filter(col("color") != "unknown")
            .filter(col("hora").isNotNull())
            .filter(col("START_LATITUDE").isNotNull())
            .filter(col("START_LONGITUDE").isNotNull())
            .select(
                "timestamp_clean",
                "fecha",
                "hora",
                "START_LATITUDE",
                "START_LONGITUDE",
                "color"
            )
    )
