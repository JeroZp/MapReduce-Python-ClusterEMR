# Análisis Meteorológico con MapReduce en Hadoop

## 📋 Descripción
Proyecto de procesamiento distribuido que analiza datos meteorológicos de Medellín (2023-2024) usando MapReduce en Hadoop. Calcula temperatura promedio y precipitación total por mes.

## 🎯 Problemática
Analizar patrones climáticos en Medellín para identificar tendencias de temperatura y precipitación mensual durante los años 2023 y 2024.

## 🛠️ Tecnologías
- **Python 3.8+**
- **mrjob** - Framework MapReduce para Python
- **Hadoop/HDFS** - Sistema de archivos distribuido
- **Amazon EMR** - Clúster Hadoop en la nube
- **Flask** - API para visualización
- **Pandas** - Procesamiento de datos

## 📁 Estructura del Proyecto
```
proyecto-mapreduce/
├── data/
│   ├── raw/              # Datos originales
│   └── processed/        # Resultados procesados
├── mapreduce/
│   └── weather_analysis.py   # Programa MapReduce
├── api/
│   └── app.py           # API Flask
├── scripts/
│   ├── download_data.py      # Descarga datos
│   ├── upload_to_hdfs.sh     # Carga a HDFS
│   ├── run_mapreduce.py      # Ejecuta MapReduce
│   └── process_results.py    # Procesa resultados
├── requirements.txt
└── README.md
```

## 🚀 Instrucciones de Ejecución

### 1. Configurar Entorno
```bash
# Clonar repositorio
git clone <tu-repositorio>
cd proyecto-mapreduce

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Descargar Datos
```bash
python scripts/download_data.py
```
Esto descargará datos meteorológicos de Medellín para 2023-2024.

### 3. Ejecutar Localmente (Prueba)
```bash
# Ejecutar MapReduce localmente
python scripts/run_mapreduce.py local

# Procesar resultados y generar CSV
python scripts/process_results.py
```

### 4. Ejecutar en Amazon EMR

#### 4.1 Crear Clúster EMR
1. Ir a AWS Console → EMR
2. Crear clúster con:
   - Hadoop 3.x
   - Python 3
   - Tipo: m5.xlarge (mínimo)

#### 4.2 Cargar Datos a HDFS
```bash
# Conectarse al clúster (SSH)
ssh -i tu-key.pem hadoop@ec2-xxx.compute.amazonaws.com

# Copiar archivos al clúster
scp -i tu-key.pem -r proyecto-mapreduce/ hadoop@ec2-xxx:~/

# En el clúster, cargar a HDFS
cd proyecto-mapreduce
bash scripts/upload_to_hdfs.sh
```

#### 4.3 Ejecutar MapReduce en EMR
```bash
# En el clúster EMR
python mapreduce/weather_analysis.py \
  -r emr \
  hdfs:///user/hadoop/weather_data/input/medellin_weather_2023_2024.json \
  --output-dir hdfs:///user/hadoop/weather_data/output
```

#### 4.4 Descargar Resultados
```bash
# En el clúster
hdfs dfs -getmerge /user/hadoop/weather_data/output ~/mapreduce_results.txt

# En tu máquina local
scp -i tu-key.pem hadoop@ec2-xxx:~/mapreduce_results.txt data/processed/
```

### 5. Procesar Resultados y Visualizar
```bash
# Generar CSV
python scripts/process_results.py

# Iniciar API
python api/app.py
```

Abrir en navegador: http://localhost:5000

## 📊 Resultados Esperados

El análisis proporciona:
- **Temperatura promedio mensual**: Promedio de temperaturas máximas y mínimas
- **Precipitación total mensual**: Suma de precipitaciones diarias
- **Días analizados**: Cantidad de días con datos por mes

## 🔍 Explicación del MapReduce

### Mapper
```python
Input: {"date": "2023-01-15", "temp_max": 25, "temp_min": 15, "precipitation": 10}
Output: ("2023-01", {"temp_sum": 20, "temp_count": 1, "precipitation": 10})
```

### Combiner
Pre-agrega datos localmente para optimizar la red.

### Reducer
```python
Input: ("2023-01", [valores...])
Output: ("2023-01", {"avg_temperature": 22.5, "total_precipitation": 150, ...})
```

## 📝 API Endpoints

- `GET /` - Página web con visualización
- `GET /api/data` - Todos los datos en JSON
- `GET /api/monthly/<year>/<month>` - Datos de un mes específico

## 🎥 Video de Sustentación

Puntos a cubrir:
1. Origen y justificación de los datos meteorológicos
2. Proceso de carga a HDFS en EMR
3. Explicación detallada del algoritmo MapReduce
4. Demostración de resultados y API

## 👥 Autores
- Jerónimo Pérez Baquero

## 📄 Licencia
Proyecto académico - Universidad EAFIT
