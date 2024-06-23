import requests
import hashlib
import time
import pandas as pd
import sqlite3
import json

# Obtener datos de la API
response = requests.get("https://restcountries.com/v3.1/all")
countries = response.json()

# Inicializar listas para el DataFrame
data = []

# Procesar datos
for country in countries:
    start_time = time.time()
    
    # Obtener el nombre de la región y el país
    region = country.get('region', 'Unknown')
    country_name = country['name']['common']
    
    # Obtener el nombre del idioma
    languages = country.get('languages', {})
    if languages:
        language_name = list(languages.values())[0]
    else:
        language_name = 'Unknown'
    
    # Encriptar el nombre del idioma con SHA1
    sha1_language = hashlib.sha1(language_name.encode()).hexdigest()
    
    # Medir el tiempo
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Añadir datos a la lista
    data.append({
        'Region': region,
        'Country': country_name,
        'Language': sha1_language,
        'Time': processing_time * 1000  # convertir a milisegundos
    })

# Crear DataFrame
df = pd.DataFrame(data)

# Calcular estadísticas de tiempo
total_time = df['Time'].sum()
average_time = df['Time'].mean()
min_time = df['Time'].min()
max_time = df['Time'].max()

# Mostrar estadísticas
print(f"Total time: {total_time} ms")
print(f"Average time: {average_time} ms")
print(f"Min time: {min_time} ms")
print(f"Max time: {max_time} ms")

# Guardar en SQLite
conn = sqlite3.connect('countries.db')
df.to_sql('countries', conn, if_exists='replace', index=False)
conn.close()

# Guardar en JSON
df.to_json('data.json', orient='records', lines=True)