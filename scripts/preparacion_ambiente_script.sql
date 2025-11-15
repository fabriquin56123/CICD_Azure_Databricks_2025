-- Databricks notebook source
-- MAGIC %python
-- MAGIC dbutils.widgets.removeAll()

-- COMMAND ----------

create widget text storageName default "adlsfabrizzioquintanav";

-- COMMAND ----------

-- Borramos el catálogo para empezar desde 0
DROP CATALOG IF EXISTS catalog_dev CASCADE;

-- COMMAND ----------

-- Creamos el catalogo
CREATE CATALOG IF NOT EXISTS catalog_dev;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Creamos los esquemas

-- COMMAND ----------

-- Creamos los esquemas según la arquitectura medallion
CREATE SCHEMA IF NOT EXISTS catalog_dev.bronze;
CREATE SCHEMA IF NOT EXISTS catalog_dev.silver;
CREATE SCHEMA IF NOT EXISTS catalog_dev.golden;
CREATE SCHEMA IF NOT EXISTS catalog_dev.exploratory;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Creamos los externals locations de cada capa

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-raw`
URL 'abfss://raw@${storageName}.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL credential)
COMMENT 'Ubicación externa para las tablas de la capa raw del Data Lake';

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-bronze`
URL 'abfss://bronze@${storageName}.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL credential)
COMMENT 'Ubicación externa para las tablas bronze del Data Lake';

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-silver`
URL 'abfss://silver@${storageName}.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL credential)
COMMENT 'Ubicación externa para las tablas silver del Data Lake';

-- COMMAND ----------

CREATE EXTERNAL LOCATION IF NOT EXISTS `exlt-golden`
URL 'abfss://golden@${storageName}.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL credential)
COMMENT 'Ubicación externa para las tablas golden del Data Lake';
