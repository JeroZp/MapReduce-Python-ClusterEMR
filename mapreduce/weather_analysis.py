from mrjob.job import MRJob
from mrjob.step import MRStep
import json
from datetime import datetime

class WeatherAnalysis(MRJob):
    """
    Análisis de datos meteorológicos con MapReduce
    Calcula temperatura promedio y precipitación total por mes
    """
    
    def mapper(self, _, line):
        """
        Mapper: extrae año-mes y emite temperatura y precipitación
        """
        try:
            # Parsear línea JSON
            data = json.loads(line)
            
            # Extraer año y mes de la fecha
            date = datetime.strptime(data['date'], '%Y-%m-%d')
            year_month = date.strftime('%Y-%m')
            
            # Calcular temperatura promedio del día
            temp_avg = (data['temp_max'] + data['temp_min']) / 2
            
            # Emitir año-mes como clave, y tupla con valores
            yield year_month, {
                'temp_sum': temp_avg,
                'temp_count': 1,
                'precipitation': data['precipitation']
            }
            
        except Exception as e:
            # Ignorar líneas con errores
            pass
    
    def combiner(self, year_month, values):
        """
        Combiner: pre-agrega valores localmente para optimizar
        """
        temp_sum = 0
        temp_count = 0
        precipitation_sum = 0
        
        for value in values:
            temp_sum += value['temp_sum']
            temp_count += value['temp_count']
            precipitation_sum += value['precipitation']
        
        yield year_month, {
            'temp_sum': temp_sum,
            'temp_count': temp_count,
            'precipitation': precipitation_sum
        }
    
    def reducer(self, year_month, values):
        """
        Reducer: calcula promedios finales y totales
        """
        temp_sum = 0
        temp_count = 0
        precipitation_sum = 0
        
        for value in values:
            temp_sum += value['temp_sum']
            temp_count += value['temp_count']
            precipitation_sum += value['precipitation']
        
        # Calcular temperatura promedio
        temp_avg = round(temp_sum / temp_count, 2) if temp_count > 0 else 0
        
        # Formatear resultado
        result = {
            'year_month': year_month,
            'avg_temperature': temp_avg,
            'total_precipitation': round(precipitation_sum, 2),
            'days_counted': temp_count
        }
        
        yield year_month, result
    
    def steps(self):
        """Define los pasos del job"""
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer)
        ]

if __name__ == '__main__':
    WeatherAnalysis.run()