# Instrucciones para ejecutar en Amazon EMR (AWS Academy)

## 1. Iniciar Laboratorio AWS Academy

1. **Acceder a AWS Academy**
   - Ingresar a tu curso en Canvas/AWS Academy
   - Ir a "Modules" → "Learner Lab"
   - Click en "Start Lab" (botón verde)
   - Esperar que el círculo cambie de rojo a verde (3-5 minutos)
   - Click en "AWS" para abrir la consola

2. **Verificar tiempo restante**
   - Los labs tienen límite de 4 horas
   - Puedes ver el tiempo restante en la parte superior

## 2. Crear clúster EMR en el Lab

### Usando AWS Console (Recomendado para Academy)

1. En la consola AWS, buscar **"EMR"**
2. Click en **"Create cluster"**
3. **Configuración rápida**:
   ```
   - Cluster name: MapReduce-Weather-Analysis
   - Logging: Deshabilitado (para ahorrar tiempo)
   - Launch mode: Cluster
   - Release: EMR-6.10.0 o la más reciente
   - Applications: Core Hadoop
   - Instance type: m4.large (más económico para labs)
   - Number of instances: 3 (1 master, 2 workers)
   - EC2 key pair: 
     * Click "Create key pair"
     * Name: mapreduce-key
     * Type: RSA
     * Format: .pem
     * Descargar y guardar el archivo
   ```
4. Click en **"Create cluster"**
5. Esperar 5-10 minutos hasta que el estado sea "Waiting"

## 3. Conectarse al clúster

1. **Obtener DNS del Master**:
   - En EMR → Clusters → Click en tu clúster
   - Copiar "Master public DNS"
   - O en CloudShell:
   ```bash
   aws emr list-clusters --active
   # Copiar el ClusterId
   aws emr describe-cluster --cluster-id j-XXXXX \
     --query 'Cluster.MasterPublicDnsName'
   ```

2. **Configurar Security Group** (IMPORTANTE):
   - EC2 → Security Groups
   - Buscar "ElasticMapReduce-master"
   - Edit inbound rules → Add rule:
     * Type: SSH
     * Source: My IP
     * Save

3. **Conectarse por SSH**:
   ```bash
   # En CloudShell o terminal local
   ssh -i mapreduce-key.pem hadoop@<master-dns>
   ```

## 4. Subir archivos al clúster

### Clonar desde GitHub
```bash
# En el clúster EMR
git clone https://github.com/tu-usuario/proyecto-mapreduce-weather.git
cd proyecto-mapreduce-weather
```

## 5. Ejecutar MapReduce en el clúster

```bash
# Instalar mrjob
sudo pip3 install mrjob

# Crear directorios en HDFS
hdfs dfs -mkdir -p /user/hadoop/weather_data/input

# Generar datos de prueba (si no los tienes)
cd proyecto-mapreduce
python3 scripts/generate_test_data.py

# Cargar datos a HDFS
hdfs dfs -put data/raw/medellin_weather_2023_2024.json \
  /user/hadoop/weather_data/input/

# Verificar
hdfs dfs -ls /user/hadoop/weather_data/input/

# Ejecutar MapReduce
python3 mapreduce/weather_analysis.py \
  -r hadoop \
  hdfs:///user/hadoop/weather_data/input/medellin_weather_2023_2024.json \
  --output-dir hdfs:///user/hadoop/weather_data/output

# Ver resultados
hdfs dfs -ls /user/hadoop/weather_data/output/
hdfs dfs -cat /user/hadoop/weather_data/output/part-00000 | head -20

# Descargar todos los resultados
hdfs dfs -getmerge /user/hadoop/weather_data/output ~/results.txt
cat ~/results.txt | wc -l  # Verificar que tengamos 24 líneas
```

## 6. Descargar resultados a tu máquina

### Mostrar en pantalla y copiar:
```bash
# En el clúster
cat ~/results.txt
# Copiar y pegar en tu archivo local
```

## 7. IMPORTANTE: Terminar recursos

⚠️ **CRÍTICO para AWS Academy**:
1. **Terminar el clúster**:
   ```bash
   aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXXX
   ```
   O en la consola: EMR → Clusters → Select → Terminate

2. **Detener el Lab**:
   - Volver a AWS Academy
   - Click en "End Lab"
   - Confirmar

## Comandos rápidos para copiar

```bash
# Todo en uno para ejecutar rápido en EMR
sudo pip3 install mrjob requests
git clone <tu-repo>
cd proyecto-mapreduce-weather
python3 scripts/generate_test_data.py
hdfs dfs -mkdir -p /user/hadoop/weather_data/input
hdfs dfs -put data/raw/*.json /user/hadoop/weather_data/input/
python3 mapreduce/weather_analysis.py -r hadoop hdfs:///user/hadoop/weather_data/input/*.json --output-dir hdfs:///user/hadoop/weather_data/output
hdfs dfs -getmerge /user/hadoop/weather_data/output ~/results.txt
cat ~/results.txt | wc -l
```
