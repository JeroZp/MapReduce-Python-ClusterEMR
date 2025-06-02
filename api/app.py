from flask import Flask, jsonify, render_template_string
import pandas as pd
import numpy as np
import os
import json

app = Flask(__name__)

# Template HTML para visualización (sin gráfico)

# Template HTML para visualización (sin gráfico)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Análisis Meteorológico - Medellín</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 40px auto;
            background-color: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #2d3748;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #718096;
            margin-bottom: 40px;
            font-size: 1.2em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }
        .stat-card {
            background: linear-gradient(135deg, #f6f6f6 0%, #e9e9e9 100%);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s ease;
            border: 1px solid #e2e8f0;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .stat-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 10px 0;
        }
        .stat-label {
            color: #4a5568;
            font-size: 1.1em;
            font-weight: 500;
        }
        .data-section {
            margin-top: 50px;
        }
        .data-section h2 {
            color: #2d3748;
            margin-bottom: 20px;
            font-size: 2em;
        }
        table { 
            width: 100%;
            border-collapse: collapse; 
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        th, td { 
            padding: 15px; 
            text-align: left; 
        }
        th { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }
        td {
            border-bottom: 1px solid #e2e8f0;
            color: #2d3748;
        }
        tr:hover {
            background-color: #f7fafc;
        }
        tr:last-child td {
            border-bottom: none;
        }
        .year-separator {
            background-color: #edf2f7;
            font-weight: bold;
            color: #4a5568;
        }
        .api-info {
            margin-top: 40px;
            padding: 20px;
            background-color: #f7fafc;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .api-info h3 {
            margin-top: 0;
            color: #2d3748;
        }
        .api-info code {
            background-color: #e2e8f0;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Análisis Meteorológico de Medellín</h1>
        <div class="subtitle">Datos procesados con MapReduce en Hadoop</div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-icon">🌡️</div>
                <div class="stat-value">{{ stats.avg_temp }}°C</div>
                <div class="stat-label">Temperatura Promedio General</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💧</div>
                <div class="stat-value">{{ stats.total_precip }}mm</div>
                <div class="stat-label">Precipitación Total Acumulada</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📅</div>
                <div class="stat-value">{{ stats.months }}</div>
                <div class="stat-label">Meses Analizados</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value">{{ stats.total_days }}</div>
                <div class="stat-label">Total de Días Procesados</div>
            </div>
        </div>
        
        <div class="data-section">
            <h2>📈 Datos Mensuales Detallados</h2>
            <table>
                <thead>
                    <tr>
                        <th>Año</th>
                        <th>Mes</th>
                        <th>Temperatura Promedio</th>
                        <th>Precipitación Total</th>
                        <th>Días Analizados</th>
                    </tr>
                </thead>
                <tbody>
                    {% set current_year = 0 %}
                    {% for row in data %}
                        {% if row.year != current_year %}
                            {% set current_year = row.year %}
                            <tr class="year-separator">
                                <td colspan="5">Año {{ row.year }}</td>
                            </tr>
                        {% endif %}
                        <tr>
                            <td>{{ row.year }}</td>
                            <td>{{ row.month_name }}</td>
                            <td>{{ row.avg_temperature }}°C</td>
                            <td>{{ row.total_precipitation }}mm</td>
                            <td>{{ row.days_counted }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="api-info">
            <h3>🔌 Endpoints API disponibles:</h3>
            <ul>
                <li><code>GET /api/data</code> - Obtener todos los datos en formato JSON</li>
                <li><code>GET /api/monthly/&lt;year&gt;/&lt;month&gt;</code> - Datos de un mes específico</li>
            </ul>
        </div>
    </div>
</body>
</html>
'''

def load_data():
    """Carga los datos del CSV procesado"""
    csv_file = 'data/processed/weather_analysis_results.csv'
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    return None

@app.route('/')
def index():
    """Página principal con visualización"""
    df = load_data()
    
    if df is None:
        return jsonify({"error": "No se encontraron datos procesados"}), 404
    
    # Calcular estadísticas
    stats = {
        'avg_temp': round(df['avg_temperature'].mean(), 2),
        'total_precip': round(df['total_precipitation'].sum(), 2),
        'months': len(df),
        'total_days': df['days_counted'].sum()
    }
    
    # Convertir DataFrame a diccionario para el template
    data = df.to_dict('records')
    
    return render_template_string(
        HTML_TEMPLATE,
        data=data,
        stats=stats
    )

@app.route('/api/data')
def api_data():
    """Endpoint API para obtener datos en formato JSON"""
    df = load_data()
    
    if df is None:
        return jsonify({"error": "No se encontraron datos procesados"}), 404
    
    # Convertir tipos numpy a tipos nativos de Python
    data_dict = df.to_dict('records')
    for record in data_dict:
        for key, value in record.items():
            if hasattr(value, 'item'):  # Es un tipo numpy
                record[key] = value.item()
            elif pd.isna(value):  # Manejar NaN
                record[key] = None
    
    # Preparar resumen con conversión de tipos
    by_year = df.groupby('year').agg({
        'avg_temperature': 'mean',
        'total_precipitation': 'sum',
        'days_counted': 'sum'
    }).round(2)
    
    by_year_dict = {}
    for year in by_year.index:
        by_year_dict[int(year)] = {
            'avg_temperature': float(by_year.loc[year, 'avg_temperature']),
            'total_precipitation': float(by_year.loc[year, 'total_precipitation']),
            'days_counted': int(by_year.loc[year, 'days_counted'])
        }
    
    return jsonify({
        "data": data_dict,
        "summary": {
            "avg_temperature": float(round(df['avg_temperature'].mean(), 2)),
            "total_precipitation": float(round(df['total_precipitation'].sum(), 2)),
            "months_analyzed": int(len(df)),
            "total_days": int(df['days_counted'].sum()),
            "date_range": {
                "start": f"{int(df.iloc[0]['year'])}-{int(df.iloc[0]['month']):02d}",
                "end": f"{int(df.iloc[-1]['year'])}-{int(df.iloc[-1]['month']):02d}"
            },
            "by_year": by_year_dict
        }
    })

@app.route('/api/monthly/<year>/<month>')
def monthly_data(year, month):
    """Obtener datos de un mes específico"""
    df = load_data()
    
    if df is None:
        return jsonify({"error": "No se encontraron datos procesados"}), 404
    
    # Filtrar por año y mes
    result = df[(df['year'] == int(year)) & (df['month'] == int(month))]
    
    if result.empty:
        return jsonify({"error": "No se encontraron datos para ese mes"}), 404
    
    # Convertir a diccionario y manejar tipos numpy
    data = result.iloc[0].to_dict()
    for key, value in data.items():
        if hasattr(value, 'item'):  # Es un tipo numpy
            data[key] = value.item()
        elif pd.isna(value):  # Manejar NaN
            data[key] = None
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)