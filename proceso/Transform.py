# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F

# COMMAND ----------

dbutils.widgets.text("catalogo", "catalog_dev")
dbutils.widgets.text("esquema_source", "bronze")
dbutils.widgets.text("esquema_sink", "silver")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Obtener los Datos

# COMMAND ----------

catalogo = dbutils.widgets.get("catalogo")
esquema_source = dbutils.widgets.get("esquema_source")
esquema_sink = dbutils.widgets.get("esquema_sink")

# COMMAND ----------

# Cargar los datos de film_details
df_film_details = spark.table(f"{catalogo}.{esquema_source}.film_details").withColumnRenamed("id","id_film_details")

# Cargar los datos de more_info
df_more_info = spark.table(f"{catalogo}.{esquema_source}.more_info").withColumnRenamed("id","id_more_info")

# Cargar los datos de movies
df_movies = spark.table(f"{catalogo}.{esquema_source}.movies").withColumnRenamed("id","id_movies")

# Cargar los datos de poster_path
df_poster_path = spark.table(f"{catalogo}.{esquema_source}.poster_path").withColumnRenamed("id","id_poster_path")

# COMMAND ----------

# MAGIC %sql
# MAGIC select max(release_date) from catalog_dev.bronze.movies

# COMMAND ----------

# MAGIC %md
# MAGIC ## Procesamiento de datos

# COMMAND ----------

# MAGIC %md
# MAGIC ### Movies

# COMMAND ----------

# Examinamos cómo está la data
display(df_movies)

# COMMAND ----------

# Verificar si hay valores nulos en la columna
display(df_movies.filter(df_movies["user_score"].isNull()).count())

# COMMAND ----------

# Encontrar el rango de "user_score"
display(df_movies.select(F.max("user_score").alias("max_user_score"), F.min("user_score").alias("min_user_score")))

# COMMAND ----------

# Determinar si la película es rentable o no
def classification(score):
    if score >= 5 and score < 7.5:
        return "Regular"
    elif score >= 7.5:
        return "Alto"
    else:
        return "Bajo"

# COMMAND ----------

classification_udf = F.udf(classification, StringType())

# COMMAND ----------

df_movies = df_movies.withColumn("classification", classification_udf("user_score"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Film Details

# COMMAND ----------

# Examinamos cómo está la data
display(df_film_details)

# COMMAND ----------

# Verificar si hay valores nulos en la columna "budget_usd"
display(df_film_details.filter(df_film_details["budget_usd"].isNull()).count())

# COMMAND ----------

# Verificar si hay valores nulos en la columna "revenue_usd"
display(df_film_details.filter(df_film_details["revenue_usd"].isNull()).count())

# COMMAND ----------

# Obtener la utilidad de la película
def utility(budget, revenue):
    # Como anteriormente se encontraron valores nulos, se procede a crear una condicional para que se pueda controlarlo
    if budget is None or revenue is None:
        return None 
    utility = revenue - budget
    return utility

# COMMAND ----------

utility_udf = F.udf(utility, IntegerType())

# COMMAND ----------

df_film_details = df_film_details.withColumn("utility", utility_udf("budget_usd", "revenue_usd"))

# COMMAND ----------

# Determinar si la película es rentable o no
def is_profitable(utility):
    # De la verificación de si hay valores nulos en budget y revenue, se deduce que también hay valores nulos en utility
    if utility is None:
        return "Indeterminado"
    elif utility <= 0:
        return "No rentable"
    else:
        return "Rentable"

# COMMAND ----------

is_profitable_udf = F.udf(is_profitable, StringType())

# COMMAND ----------

df_film_details = df_film_details.withColumn("is_profitable", is_profitable_udf("utility"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### More Info

# COMMAND ----------

# Examinamos cómo está la data
display(df_more_info)

# COMMAND ----------

# Transformar columna de texto a entero
df_more_info = df_more_info.withColumn("budget", regexp_replace(col("budget"), "[$,]", "").cast("int"))
df_more_info = df_more_info.withColumn("revenue", regexp_replace(col("revenue"), "[$,]", "").cast("int"))

# COMMAND ----------

# Obtener la duración de la película en minutos
df_more_info = (
    df_more_info.withColumn("hours", regexp_extract(col("runtime"), r"(\d+)\s*h", 1))
      .withColumn("minutes", regexp_extract(col("runtime"), r"(\d+)\s*min", 1))
      .withColumn(
          "duration_minutes",
          when(col("hours") != "", col("hours").cast("int") * 60).otherwise(0) +
          when(col("minutes") != "", col("minutes").cast("int")).otherwise(0)
      )
      .drop("hours", "minutes")  # opcional, para limpiar
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Poster Path

# COMMAND ----------

# Examinamos cómo está la data
display(df_poster_path)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Unión y creación de nuevas tablas

# COMMAND ----------

df_joined = df_movies.alias("x").join(df_more_info.alias("y"), col("x.id_movies") == col("y.id_more_info"), "left")\
                                    .drop(col("id_more_info")
                                        ,col("x.ingestion_date")
                                        ,col("y.ingestion_date")
                                        ,col("y.runtime"))
                                  

df_joined.display()

# COMMAND ----------

df_joined2 = df_joined.alias("x").join(df_film_details.alias("y"), col("x.id_movies") == col("y.id_film_details"), "left")\
                                  .drop(col("id_film_details")
                                        ,col("y.ingestion_date")
                                        ,col("x.budget")
                                        ,col("x.revenue")
                                        ,col("x.film_id"))

df_joined2.display()

# COMMAND ----------

df_final = (
    df_joined2
    .withColumn("release_year", year(col("release_date")).cast("string"))  # año como string
    .withColumn("release_month", date_format(col("release_date"), "MMMM"))  # nombre completo del mes
    .orderBy("release_date", ascending = False)
)

# COMMAND ----------

# Verificamos la cantidad de registros que hay de la unión final
df_final.count()

# COMMAND ----------

df_final.display()

# COMMAND ----------

# Verificamos si las películas son registros únicos
df_final.select(countDistinct("title")).display()

# COMMAND ----------

# El valor difiere de la cantidad total de registros. Pueden haber dos casuísticas: El mismo título pero en diferentes años o idiomas y por ende diferentes valoraciones, o registros duplicados. Se procede a eliminar duplicados excluyendo a la columna id_movies.
cols_to_check = [c for c in df_final.columns if c != "id_movies"]

df_final = df_final.dropDuplicates(cols_to_check)

df_final.display()

# COMMAND ----------

# Contamos la cantidad de registros que quedaron después de borrar duplicados
df_final.count()

# COMMAND ----------

# Verificamos si hay películas con el mismo título pero en diferentes años o idiomas
df_final.groupBy("title") \
    .agg(F.count("*").alias("count")) \
    .filter(F.col("count") > 1) \
    .orderBy(F.desc("count")) \
    .display()

# COMMAND ----------

df_final.filter(col("title") == "Return").display()

# COMMAND ----------

# Creamos una nueva tabla donde aparezcan los actores top separados que estaban separados por comas en un registro
df_actores_top = (
    df_final
    .withColumn("actores", split(col("top_billed"), ",\\s*"))
    .withColumn("actores", explode(col("actores")))
    .select("id_movies", "actores")
)

display(df_actores_top)

# COMMAND ----------

# Creamos una nueva tabla donde aparezcan los géneros de las películas separados que estaban separados por comas en un registro
df_genres = (
    df_final
    .withColumn("genre", split(col("genres"), ",\\s*"))
    .withColumn("genre", explode(col("genre")))
    .select("id_movies", "genre")
)

df_genres.display()

# COMMAND ----------

df_genres_extended = df_genres.alias("x").join(df_final.alias("y"), col("x.id_movies") == col("y.id_movies"), "left")\
                                  .select(col("x.id_movies"),col("x.genre"), col("y.title"), col("y.language"), col("y.user_score")
                                          , col("y.classification"), col("y.release_year"), col("y.release_month") )

# COMMAND ----------

df_genres_extended.display()

# COMMAND ----------

df_actors_top_extended = df_actores_top.alias("x").join(df_final.alias("y"), col("x.id_movies") == col("y.id_movies"), "left")\
                                  .select(col("x.id_movies"),col("x.actores"), col("y.title"), col("y.language")
                                          ,col("y.user_score")
                                          ,col("y.classification")
                                          ,col("y.release_year")
                                          ,col("y.release_month") )

# COMMAND ----------

df_actors_top_extended.display()

# COMMAND ----------

df_actors_top_extended.write.mode("overwrite").saveAsTable(f"{catalogo}.{esquema_sink}.actors_top_extended")
df_genres_extended.write.mode("overwrite").saveAsTable(f"{catalogo}.{esquema_sink}.genres_extended")
df_final.write.mode("overwrite").saveAsTable(f"{catalogo}.{esquema_sink}.movies")
