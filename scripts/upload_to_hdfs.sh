#!/bin/bash

# Script para cargar datos a HDFS en Amazon EMR
# Ejecutar este script después de conectarse al clúster EMR

echo "🚀 Iniciando carga de datos a HDFS..."

# Crear directorio en HDFS
hdfs dfs -mkdir -p /user/hadoop/weather_data/input

# Cargar archivo de datos
hdfs dfs -put data/raw/medellin_weather_2023_2024.json /user/hadoop/weather_data/input/

# Verificar que se cargó correctamente
echo "✅ Verificando archivos en HDFS:"
hdfs dfs -ls /user/hadoop/weather_data/input/

echo "✅ Carga completada!"