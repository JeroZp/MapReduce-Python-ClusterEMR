import subprocess
import os
import sys

def run_local():
    """Ejecuta MapReduce localmente para pruebas"""
    print("🧪 Ejecutando MapReduce localmente...")
    
    cmd = [
        'python', 'mapreduce/weather_analysis.py',
        'data/raw/medellin_weather_2023_2024.json',
        '--output-dir', 'data/processed/local_output',
        '--no-output'
    ]
    
    subprocess.run(cmd)
    print("✅ Ejecución local completada!")

def run_on_emr():
    """Ejecuta MapReduce en Amazon EMR"""
    print("☁️  Ejecutando MapReduce en EMR...")
    
    # Configuración EMR
    cmd = [
        'python', 'mapreduce/weather_analysis.py',
        '-r', 'emr',
        '--emr-job-flow-id', 'j-XXXXXXXXXXXXX',  # Reemplazar con tu Job Flow ID
        'hdfs:///user/hadoop/weather_data/input/medellin_weather_2023_2024.json',
        '--output-dir', 'hdfs:///user/hadoop/weather_data/output',
        '--no-output'
    ]
    
    print("Comando:", ' '.join(cmd))
    print("\n⚠️  Asegúrate de:")
    print("1. Tener configuradas las credenciales AWS")
    print("2. Reemplazar el Job Flow ID con el de tu clúster")
    print("3. Haber cargado los datos a HDFS")
    
    # subprocess.run(cmd)

def download_results():
    """Descarga resultados desde HDFS"""
    print("📥 Descargando resultados desde HDFS...")
    
    os.makedirs('data/processed', exist_ok=True)
    
    cmd = [
        'hdfs', 'dfs', '-getmerge',
        '/user/hadoop/weather_data/output',
        'data/processed/mapreduce_results.txt'
    ]
    
    print("Ejecuta este comando en el clúster EMR:")
    print(' '.join(cmd))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'local':
            run_local()
        elif sys.argv[1] == 'emr':
            run_on_emr()
        elif sys.argv[1] == 'download':
            download_results()
    else:
        print("Uso:")
        print("  python scripts/run_mapreduce.py local     # Ejecutar localmente")
        print("  python scripts/run_mapreduce.py emr       # Ejecutar en EMR")
        print("  python scripts/run_mapreduce.py download  # Descargar resultados")