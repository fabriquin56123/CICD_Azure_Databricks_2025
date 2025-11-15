# Databricks notebook source
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType
from pyspark.sql.functions import current_timestamp, to_timestamp, concat, col, lit

# COMMAND ----------

dbutils.widgets.removeAll()

# COMMAND ----------

dbutils.widgets.text("storage_name", "adlsfabrizzioquintanav")
dbutils.widgets.text("container", "raw")
dbutils.widgets.text("catalogo", "catalog_dev")
dbutils.widgets.text("esquema", "bronze")

# COMMAND ----------

storage_name = dbutils.widgets.get("storage_name")
container = dbutils.widgets.get("container")
catalogo = dbutils.widgets.get("catalogo")
esquema = dbutils.widgets.get("esquema")

ruta = f"abfss://{container}@{storage_name}.dfs.core.windows.net/FilmDetails.csv"

# COMMAND ----------

# Creamos del esquema de la tabla
film_details_schema = StructType(fields=[StructField("id", IntegerType(), False),
                                  StructField("director", StringType(), True),
                                  StructField("top_billed", StringType(), True),
                                  StructField("budget_usd", IntegerType(), True),
                                  StructField("revenue_usd", IntegerType(), True)
])

# COMMAND ----------

# Leemos la tabla
film_details_df = spark.read \
            .option("header", True) \
            .schema(film_details_schema) \
            .csv(ruta)

# COMMAND ----------

# Creamos una columna adicional del tiempo de ingesta de la data
film_details_with_timestamp_df = film_details_df.withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

"""film_details_selected_df = film_details_with_timestamp_df.select(col('raceId').alias('race_id'), 
                                                   col('year').alias('race_year'), 
                                                   col('round'), col('circuitId').alias('circuit_id'),
                                                   col('name'), col('ingestion_date'))"""

# COMMAND ----------

# Guardamos la tabla en el esquema de bronze
film_details_with_timestamp_df.write.mode('overwrite').saveAsTable(f'{catalogo}.{esquema}.film_details')

# COMMAND ----------

display(film_details_with_timestamp_df)
