# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F

# COMMAND ----------

dbutils.widgets.text("catalogo", "catalog_dev")
dbutils.widgets.text("esquema_source", "silver")
dbutils.widgets.text("esquema_sink", "golden")

# COMMAND ----------

catalogo = dbutils.widgets.get("catalogo")
esquema_source = dbutils.widgets.get("esquema_source")
esquema_sink = dbutils.widgets.get("esquema_sink")

# COMMAND ----------

df_movies_transformed = spark.table(f"{catalogo}.{esquema_source}.movies")
df_genres_extended = spark.table(f"{catalogo}.{esquema_source}.genres_extended")
df_actors_top_extended = spark.table(f"{catalogo}.{esquema_source}.actors_top_extended")

# COMMAND ----------

df_genres_transformed = df_genres_extended.groupBy(col("release_year"), col("genre"), col("classification"), col("language")).agg(
                                                     count(col("title")).alias("cantidad"),
                                                     round(avg(col("user_score")), 2).alias("avg_user_score")
                                                     ).orderBy(col("release_year").desc()
                                                               ,col("genre")
                                                               ,col("classification")
                                                               ,col("cantidad").desc()
                                                               ,col("language").desc())
                                                                

# COMMAND ----------

df_genres_transformed.display()

# COMMAND ----------

# Obtenemos los actores top según el año, la calidad de la película, y la cantidad de películas que ha protagonizado
df_actor_top_transformed = (
    df_actors_top_extended
        .groupBy(
            col("actores")
            ,col("classification")
            ,col("release_year")
            #col("language")
        )
        .agg(
            count(col("title")).alias("cantidad"),
            round(avg(col("user_score")), 2).alias("avg_user_score")
        )
        .orderBy(
            #col("release_year").desc(),
            col("classification")
            ,col("cantidad").desc()
            ,col("avg_user_score").desc()
            ,col("actores")
            ,col("release_year")
            #col("language").desc()
        )
)

# COMMAND ----------

df_actor_top_transformed.display()

# COMMAND ----------

df_movies_transformed.display()

# COMMAND ----------

df_movies_transformed_final = (
    df_movies_transformed
        .groupBy(
            col("title")
            ,col("release_year")
            ,col("language")
            ,col("classification")
            ,col("is_profitable")
        )
        .agg(
            count(col("title")).alias("cantidad")
            ,round(avg(col("user_score")), 2).alias("avg_user_score")
            ,sum(col("utility")).alias("utility")
            ,round(avg(col("duration_minutes")), 2).alias("avg_duration_minutos")
        )
        .orderBy(
            #col("release_year").desc(),
            col("classification")
            ,col("cantidad").desc()
            ,col("avg_user_score").desc()
            ,col("avg_duration_minutos").desc()
            ,col("title")
            ,col("release_year")
            #col("language").desc()
        )
)

# COMMAND ----------

df_movies_transformed_final.display()

# COMMAND ----------

# Creamos las tablas golden, las que se utilizaran para el análisis
df_movies_transformed_final.write.mode("overwrite").saveAsTable(f"{catalogo}.{esquema_sink}.golden_movies")
df_actor_top_transformed.write.mode("overwrite").saveAsTable(f"{catalogo}.{esquema_sink}.golden_actors")
df_genres_transformed.write.mode("overwrite").saveAsTable(f"{catalogo}.{esquema_sink}.golden_genres")
