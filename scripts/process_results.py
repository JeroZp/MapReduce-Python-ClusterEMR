import json
import pandas as pd
import os
import glob

def process_mapreduce_output():
    """Convierte la salida de MapReduce a CSV"""
    
    # Leer archivo de resultados
    results = []
    
    # Buscar directorio de salida local o archivo único de EMR
    if os.path.exists('data/processed/local_output'):
        # Leer TODOS los archivos part-* del directorio local
        output_dir = 'data/processed/local_output'
        print(f"📖 Leyendo resultados desde directorio: {output_dir}")
        
        # Listar todos los archivos part-*
        part_files = sorted([f for f in os.listdir(output_dir) if f.startswith('part-')])
        print(f"📁 Encontrados {len(part_files)} archivos de salida")
        
        for part_file in part_files:
            file_path = os.path.join(output_dir, part_file)
            print(f"  - Leyendo {part_file}...")
            
            with open(file_path, 'r') as f:
                for line in f:
                    # Formato: "2023-01" {"year_month": "2023-01", ...}
                    parts = line.strip().split('\t')
                    if len(parts) == 2:
                        year_month = parts[0].strip('"')
                        data = json.loads(parts[1])
                        results.append(data)
    
    elif os.path.exists('data/processed/mapreduce_results.txt'):
        # Leer archivo único de EMR
        input_file = 'data/processed/mapreduce_results.txt'
        print(f"📖 Leyendo resultados desde archivo: {input_file}")
        
        with open(input_file, 'r') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    year_month = parts[0].strip('"')
                    data = json.loads(parts[1])
                    results.append(data)
    else:
        print("❌ No se encontraron archivos de resultados")
        return
    
    print(f"\n📊 Total de registros encontrados: {len(results)}")
    
    if len(results) == 0:
        print("❌ No se encontraron datos en los archivos de salida")
        return
    
    # Convertir a DataFrame
    df = pd.DataFrame(results)
    
    # Ordenar por fecha
    df['year_month'] = pd.to_datetime(df['year_month'] + '-01')
    df = df.sort_values('year_month')
    
    # Formatear columnas
    df['year'] = df['year_month'].dt.year
    df['month'] = df['year_month'].dt.month
    df['month_name'] = df['year_month'].dt.strftime('%B')
    
    # Reordenar columnas
    df = df[['year', 'month', 'month_name', 'avg_temperature', 
             'total_precipitation', 'days_counted']]
    
    # Guardar como CSV
    output_file = 'data/processed/weather_analysis_results.csv'
    df.to_csv(output_file, index=False)
    
    print(f"✅ Resultados guardados en: {output_file}")
    print(f"\n📊 Resumen de resultados:")
    print(f"- Total de meses analizados: {len(df)}")
    print(f"- Temperatura promedio general: {df['avg_temperature'].mean():.2f}°C")
    print(f"- Precipitación promedio mensual: {df['total_precipitation'].mean():.2f}mm")
    print(f"- Años cubiertos: {df['year'].min()} - {df['year'].max()}")
    
    # Mostrar primeras filas
    print("\n🔍 Primeras filas del resultado:")
    print(df.head(10).to_string())
    
    # Mostrar últimas filas
    print("\n🔍 Últimas filas del resultado:")
    print(df.tail(5).to_string())
    
    return df

if __name__ == "__main__":
    process_mapreduce_output()