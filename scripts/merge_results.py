import os
import shutil

def merge_mapreduce_output():
    """Combina todos los archivos part-* en un solo archivo"""
    
    output_dir = 'data/processed/local_output'
    
    if not os.path.exists(output_dir):
        print("❌ No se encontró el directorio de salida")
        return
    
    # Listar todos los archivos part-*
    part_files = sorted([f for f in os.listdir(output_dir) 
                         if f.startswith('part-') and not f.endswith('.crc')])
    
    if not part_files:
        print("❌ No se encontraron archivos part-*")
        return
    
    print(f"📁 Encontrados {len(part_files)} archivos para combinar")
    
    # Archivo de salida combinado
    merged_file = 'data/processed/mapreduce_results_merged.txt'
    
    with open(merged_file, 'w') as outfile:
        for part_file in part_files:
            file_path = os.path.join(output_dir, part_file)
            print(f"  - Agregando {part_file}...")
            
            with open(file_path, 'r') as infile:
                content = infile.read()
                if content.strip():  # Solo agregar si no está vacío
                    outfile.write(content)
                    if not content.endswith('\n'):
                        outfile.write('\n')
    
    print(f"✅ Archivos combinados en: {merged_file}")
    
    # Contar líneas
    with open(merged_file, 'r') as f:
        line_count = sum(1 for line in f if line.strip())
    
    print(f"📊 Total de registros en archivo combinado: {line_count}")

if __name__ == "__main__":
    merge_mapreduce_output()