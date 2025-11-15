# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

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

ruta = f"abfss://{container}@{storage_name}.dfs.core.windows.net/PosterPath.csv"

# COMMAND ----------

# Creamos del esquema de la tabla
poster_path_schema = StructType(fields=[StructField("id", IntegerType(), False),
                                     StructField("poster_path", StringType(), True),
                                     StructField("backdrop_path", StringType(), True)
])

# COMMAND ----------

# Leemos la tabla
df_poster_path = spark.read\
.option('header', True)\
.schema(poster_path_schema)\
.csv(ruta)

# COMMAND ----------

# Creamos una columna adicional del tiempo de ingesta de la data
df_poster_path_final = df_poster_path.withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

# Guardamos la tabla en el esquema de bronze
df_poster_path_final.write.mode("overwrite").saveAsTable(f"{catalogo}.{esquema}.poster_path")
