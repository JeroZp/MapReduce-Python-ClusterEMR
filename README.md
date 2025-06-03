# 🌤️ Análisis Meteorológico con MapReduce en Hadoop

## 📋 Descripción
Proyecto de procesamiento distribuido que analiza datos meteorológicos de Medellín (2023-2024) usando MapReduce en Hadoop. Calcula temperatura promedio y precipitación total por mes utilizando el paradigma de programación MapReduce.

## 🎯 Problemática
Analizar patrones climáticos en Medellín para identificar tendencias de temperatura y precipitación mensual durante los años 2023 y 2024, procesando más de 730 días de datos meteorológicos de manera distribuida.

## 🛠️ Tecnologías
- **Python 3.8+** - Lenguaje de programación
- **mrjob** - Framework MapReduce para Python
- **Hadoop/HDFS** - Sistema de archivos distribuido
- **Amazon EMR** - Clúster Hadoop en la nube (AWS Academy)
- **Flask** - API para visualización de resultados
- **Pandas** - Procesamiento de datos y exportación a CSV

## 📁 Estructura del Proyecto
```
proyecto-mapreduce/
├── data/
│   ├── raw/                      # Datos meteorológicos originales
│   └── processed/                # Resultados procesados
│       └── local_output/         # Salida de MapReduce local
├── mapreduce/
│   └── weather_analysis.py       # Programa MapReduce principal
├── api/
│   └── app.py                    # API Flask para visualización
├── scripts/
│   ├── download_data.py          # Descarga datos de Open-Meteo
│   ├── generate_test_data.py     # Genera datos de prueba
│   ├── upload_to_hdfs.sh         # Script para cargar a HDFS
│   ├── run_mapreduce.py          # Ejecuta MapReduce (local/EMR)
│   ├── process_results.py        # Procesa resultados y genera CSV
│   ├── verify_results.py         # Verifica integridad de resultados
│   ├── merge_results.py          # Combina archivos part-*
│   └── emr_quick_run.sh          # Script rápido para EMR
├── requirements.txt              # Dependencias Python
├── README.md                     # Este archivo
├── EMR_INSTRUCTIONS.md           # Guía detallada para AWS EMR
├── VIDEO_GUIDE.md                # Guía para el video
└── .gitignore                    # Archivos ignorados por Git
```

## 🚀 Instrucciones de Ejecución

### 1. Configurar Entorno
```bash
# Clonar repositorio
git clone https://github.com/<tu-usuario>/proyecto-mapreduce
cd proyecto-mapreduce

# Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Obtener Datos

#### Opción A: Descargar datos reales
```bash
python scripts/download_data.py
```

#### Opción B: Generar datos de prueba
```bash
python scripts/generate_test_data.py
```

### 3. Ejecutar Localmente (Desarrollo)
```bash
# Ejecutar MapReduce localmente
python scripts/run_mapreduce.py local

# Procesar todos los archivos de resultados
python scripts/process_results.py

# Verificar resultados (opcional)
python scripts/verify_results.py
```

### 4. Visualizar Resultados
```bash
# Iniciar API Flask
python api/app.py

# Abrir en navegador
# http://localhost:5000
```

### 5. Ejecutar en Amazon EMR (Producción)

#### 5.1 Preparación
1. Subir proyecto a GitHub
2. Iniciar AWS Academy Lab
3. Crear clúster EMR (ver EMR_INSTRUCTIONS.md)

#### 5.2 En el clúster EMR
```bash
# Conectarse al clúster
ssh -i tu-key.pem hadoop@<master-dns>

# Instalar dependencias
sudo pip3 install mrjob requests

# Clonar repositorio
git clone https://github.com/<tu-usuario>/proyecto-mapreduce
cd proyecto-mapreduce

# Generar datos si es necesario
python3 scripts/generate_test_data.py

# Cargar a HDFS
hdfs dfs -mkdir -p /user/hadoop/weather_data/input
hdfs dfs -put data/raw/*.json /user/hadoop/weather_data/input/

# Ejecutar MapReduce
python3 mapreduce/weather_analysis.py \
  -r hadoop \
  hdfs:///user/hadoop/weather_data/input/medellin_weather_2023_2024.json \
  --output-dir hdfs:///user/hadoop/weather_data/output

# Descargar resultados
hdfs dfs -getmerge /user/hadoop/weather_data/output ~/results.txt
```

## 📊 Resultados Esperados

El análisis proporciona:
- **Temperatura promedio mensual**: Promedio entre temperaturas máximas y mínimas
- **Precipitación total mensual**: Suma de todas las precipitaciones del mes
- **Días analizados**: Cantidad de días con datos disponibles por mes

### Ejemplo de salida:
```
2023-01: Temp. promedio: 23.5°C, Precipitación: 120.5mm (31 días)
2023-02: Temp. promedio: 24.1°C, Precipitación: 85.3mm (28 días)
...
```

## 🔍 Explicación del MapReduce

### Mapper
- **Entrada**: Línea JSON con datos de un día
- **Proceso**: Extrae año-mes y calcula temperatura promedio diaria
- **Salida**: `(año-mes, {temp_sum, temp_count, precipitation})`

### Combiner
- **Función**: Pre-agrega datos localmente para optimizar red
- **Proceso**: Suma parcial de temperaturas y precipitaciones

### Reducer
- **Entrada**: Todos los valores de un mes específico
- **Proceso**: Calcula promedio final y suma total
- **Salida**: `(año-mes, {avg_temperature, total_precipitation, days_counted})`

## 📦 Scripts Auxiliares

### `process_results.py`
Procesa TODOS los archivos `part-*` generados por MapReduce y los convierte en un CSV único.

### `verify_results.py`
Verifica la integridad de los resultados y muestra un resumen de todos los meses procesados.

### `merge_results.py`
Combina múltiples archivos `part-*` en un solo archivo (útil para resultados distribuidos).

## 🌐 API Endpoints

- `GET /` - Página web con visualización de datos
- `GET /api/data` - Todos los datos en formato JSON
- `GET /api/monthly/<year>/<month>` - Datos de un mes específico

### Ejemplo de respuesta API:
```json
{
  "data": [...],
  "summary": {
    "avg_temperature": 23.2,
    "total_precipitation": 2880.5,
    "months_analyzed": 24,
    "total_days": 731
  }
}
```

## 🎥 Video de Sustentación

El video de sustentación (10 minutos) cubre:
1. Origen y justificación de los datos meteorológicos
2. Proceso de carga a HDFS en EMR
3. Explicación detallada del algoritmo MapReduce
4. Demostración de ejecución local y en clúster
5. Visualización de resultados mediante la API

## 📈 Métricas del Proyecto

- **Datos procesados**: 2 años (2023-2024)
- **Registros totales**: ~730 días
- **Meses analizados**: 24
- **Temperatura promedio**: ~23°C
- **Tecnología**: Hadoop MapReduce distribuido

## 🤝 Contribución

Proyecto académico desarrollado para el curso ST0263: Tópicos Especiales en Telemática.

## 👥 Autores
- Jerónimo Pérez Baquero
- Universidad EAFIT

## 📄 Licencia
Proyecto académico - Universidad EAFIT - 2025

---
**Nota**: Para instrucciones detalladas de Amazon EMR, consultar `EMR_INSTRUCTIONS.md`
