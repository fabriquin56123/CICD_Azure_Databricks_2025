-- Databricks notebook source
-- Brindamos permisos de usar el catálogo a las cuentas que están agrupadas
GRANT USE CATALOG ON CATALOG catalog_dev TO `cuentas_agrupadas`;

-- COMMAND ----------

-- Brindamos permisos de uso de esquemas y creaciones en estos esquemas

GRANT USE SCHEMA ON SCHEMA catalog_dev.bronze TO `cuentas_agrupadas`;
GRANT CREATE ON SCHEMA catalog_dev.bronze TO `cuentas_agrupadas`;

GRANT USE SCHEMA ON SCHEMA catalog_dev.silver TO `cuentas_agrupadas`;
GRANT CREATE ON SCHEMA catalog_dev.silver TO `cuentas_agrupadas`;

GRANT USE SCHEMA ON SCHEMA catalog_dev.golden TO `cuentas_agrupadas`;
GRANT CREATE ON SCHEMA catalog_dev.golden TO `cuentas_agrupadas`;

-- COMMAND ----------

-- Visualizo los permisos de uso y de creación sobre cada una de los esquemas
SHOW GRANTS ON SCHEMA catalog_dev.bronze;

-- COMMAND ----------

SHOW GRANTS ON SCHEMA catalog_dev.silver;

-- COMMAND ----------

SHOW GRANTS ON SCHEMA catalog_dev.golden;

-- COMMAND ----------

-- Brindamos permisos de lectura sobre las tablas del catálogo golden
GRANT SELECT ON TABLE catalog_dev.golden.golden_actors TO `cuentas_agrupadas`;
GRANT SELECT ON TABLE catalog_dev.golden.golden_movies TO `cuentas_agrupadas`;
GRANT SELECT ON TABLE catalog_dev.golden.golden_genres TO `cuentas_agrupadas`;

-- COMMAND ----------

-- Visualizo los permisos de lectura sobre cada una de las tablas
SHOW GRANTS ON TABLE catalog_dev.golden.golden_actors;

-- COMMAND ----------

SHOW GRANTS ON TABLE catalog_dev.golden.golden_movies;

-- COMMAND ----------

SHOW GRANTS ON TABLE catalog_dev.golden.golden_genres;

-- COMMAND ----------

-- Visualizo los permisos del uso del catálogo
SHOW GRANTS ON CATALOG catalog_dev;

-- Brindar acceso total al catálogo dev
GRANT MANAGE ON CATALOG catalog_dev TO `quintanafabrizzio14@gmail.com`;
