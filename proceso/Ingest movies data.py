# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

dbutils.widgets.removeAll()

# COMMAND ----------

dbutils.widgets.text("storage_name", "adlsfabrizzioquintanav")
dbutils.widgets.text("container", "bronze")
dbutils.widgets.text("catalogo", "catalog_dev")
dbutils.widgets.text("esquema", "bronze")

# COMMAND ----------

storage_name = dbutils.widgets.get("storage_name")
container = dbutils.widgets.get("container")
catalogo = dbutils.widgets.get("catalogo")
esquema = dbutils.widgets.get("esquema")

ruta = f"abfss://{container}@{storage_name}.dfs.core.windows.net/Movies.csv"

# COMMAND ----------

# Creamos del esquema de la tabla
movies_schema = StructType(fields=[StructField("id", IntegerType(), False),
                                     StructField("title", StringType(), True),
                                     StructField("genres", StringType(), True),
                                     StructField("language", StringType(), True),
                                     StructField("user_score", DoubleType(), True),
                                     StructField("runtime_hour", IntegerType(), True),
                                     StructField("runtime_min", IntegerType(), True),
                                     StructField("release_date", DateType(), True),
                                     StructField("vote_count", IntegerType(), True)
])

# COMMAND ----------

# Leemos la tabla
df_movies = spark.read\
.option('header', True)\
.schema(movies_schema)\
.csv(ruta)

# COMMAND ----------

# Creamos una columna adicional del tiempo de ingesta de la data
df_movies_final = df_movies.withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

# Guardamos la tabla en el esquema de bronze
df_movies_final.write.mode("overwrite").option("mergeSchema", "true").saveAsTable(f"{catalogo}.{esquema}.movies")
