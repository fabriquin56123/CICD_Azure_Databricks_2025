-- Databricks notebook source
-- Revocamos el uso de algunos esquemas
REVOKE USE SCHEMA ON SCHEMA catalog_dev.bronze FROM cuentas_agrupadas

-- COMMAND ----------

REVOKE USE SCHEMA ON SCHEMA catalog_dev.silver FROM cuentas_agrupadas

-- COMMAND ----------

SHOW GRANT ON SCHEMA catalog_dev.bronze

-- COMMAND ----------

SHOW GRANT ON SCHEMA catalog_dev.silver

-- COMMAND ----------

SHOW GRANT ON SCHEMA catalog_dev.golden
