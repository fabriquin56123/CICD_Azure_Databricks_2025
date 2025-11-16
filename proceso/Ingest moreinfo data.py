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

ruta = f"abfss://{container}@{storage_name}.dfs.core.windows.net/MoreInfo.csv"

# COMMAND ----------

"""df_more_info = spark.read.option('header', True)\
                        .option('inferSchema', True)\
                        .csv(ruta)"""

# COMMAND ----------

# Creamos del esquema de la tabla
more_info_schema = StructType(fields=[StructField("id", IntegerType(), False),
                                     StructField("runtime", StringType(), True),
                                     StructField("budget", StringType(), True),
                                     StructField("revenue", StringType(), True),
                                     StructField("film_id", IntegerType(), True)
])

# COMMAND ----------

# DBTITLE 1,Use user specified schema to load df with correct types
# Leemos la tabla
df_more_info = spark.read\
.option('header', True)\
.schema(more_info_schema)\
.csv(ruta)


# COMMAND ----------

# DBTITLE 1,Add col with current timestamp 
# Creamos una columna adicional del tiempo de ingesta de la data
df_more_info_final = df_more_info.withColumn("ingestion_date", current_timestamp())

# COMMAND ----------

# Guardamos la tabla en el esquema de bronze
df_more_info_final.write.mode("overwrite").saveAsTable(f"{catalogo}.{esquema}.more_info")
