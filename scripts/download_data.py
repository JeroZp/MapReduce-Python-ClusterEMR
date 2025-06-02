import requests
import json
import os
from datetime import datetime, timedelta

def download_weather_data():
    """Descarga datos meteorológicos de Medellín para 2023-2024"""
    
    # Crear directorio si no existe
    os.makedirs('data/raw', exist_ok=True)
    
    # Coordenadas de Medellín
    lat = 6.25
    lon = -75.56
    
    all_data = []
    
    # Descargar por trimestres para evitar límites de la API
    periods = [
        ('2023-01-01', '2023-03-31', '2023-Q1'),
        ('2023-04-01', '2023-06-30', '2023-Q2'),
        ('2023-07-01', '2023-09-30', '2023-Q3'),
        ('2023-10-01', '2023-12-31', '2023-Q4'),
        ('2024-01-01', '2024-03-31', '2024-Q1'),
        ('2024-04-01', '2024-06-30', '2024-Q2'),
        ('2024-07-01', '2024-09-30', '2024-Q3'),
        ('2024-10-01', '2024-12-31', '2024-Q4')
    ]
    
    for start_date, end_date, period in periods:
        url = f"https://archive-api.open-meteo.com/v1/archive"
        params = {
            'latitude': lat,
            'longitude': lon,
            'start_date': start_date,
            'end_date': end_date,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
            'timezone': 'America/Bogota'
        }
        
        print(f"Descargando datos para {period}...")
        
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Procesar datos diarios
                daily_data = data['daily']
                records_in_period = 0
                
                for i in range(len(daily_data['time'])):
                    # Validar que los datos no sean None
                    if (daily_data['temperature_2m_max'][i] is not None and 
                        daily_data['temperature_2m_min'][i] is not None):
                        record = {
                            'date': daily_data['time'][i],
                            'temp_max': daily_data['temperature_2m_max'][i],
                            'temp_min': daily_data['temperature_2m_min'][i],
                            'precipitation': daily_data['precipitation_sum'][i] or 0
                        }
                        all_data.append(record)
                        records_in_period += 1
                
                print(f"✅ {period}: {records_in_period} días descargados")
            else:
                print(f"❌ Error descargando {period}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error descargando {period}: {str(e)}")
    
    # Guardar como JSON lines (un registro por línea)
    output_file = 'data/raw/medellin_weather_2023_2024.json'
    with open(output_file, 'w') as f:
        for record in all_data:
            f.write(json.dumps(record) + '\n')
    
    print(f"\n✅ Datos guardados en: {output_file}")
    print(f"Total de registros: {len(all_data)}")

if __name__ == "__main__":
    download_weather_data()