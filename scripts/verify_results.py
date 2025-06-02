import os
import json

def verify_mapreduce_results():
    """Verifica y muestra un resumen de todos los resultados de MapReduce"""
    
    output_dir = 'data/processed/local_output'
    
    if not os.path.exists(output_dir):
        print("❌ No se encontró el directorio de salida")
        return
    
    # Recolectar todos los resultados
    all_months = {}
    total_files = 0
    
    for filename in sorted(os.listdir(output_dir)):
        if filename.startswith('part-') and not filename.endswith('.crc'):
            total_files += 1
            file_path = os.path.join(output_dir, filename)
            
            with open(file_path, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split('\t')
                        if len(parts) == 2:
                            month = parts[0].strip('"')
                            data = json.loads(parts[1])
                            all_months[month] = data
    
    print(f"📁 Archivos procesados: {total_files}")
    print(f"📅 Total de meses encontrados: {len(all_months)}")
    
    if all_months:
        # Ordenar por fecha
        sorted_months = sorted(all_months.keys())
        
        print(f"\n📊 Rango de fechas: {sorted_months[0]} a {sorted_months[-1]}")
        print("\n📈 Todos los meses encontrados:")
        
        for year in ['2023', '2024']:
            print(f"\n{year}:")
            year_months = [m for m in sorted_months if m.startswith(year)]
            for month in year_months:
                data = all_months[month]
                print(f"  {month}: {data['avg_temperature']}°C, {data['total_precipitation']}mm ({data['days_counted']} días)")
            print(f"  Total meses en {year}: {len(year_months)}")

if __name__ == "__main__":
    verify_mapreduce_results()