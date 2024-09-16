import sqlite3
import requests
import pandas as pd

responseContentType="application/json"
url="https://datos.madrid.es/egob/catalogo/50055-12105277-fuentes-mascotas.{responseContentType}"

all_pages=[]

while url:
    response = requests.get(url)
    if response.status_code==200:
        data = response.json()
        all_pages.extend(data["records"])
        url=data.get("next",None)

df = pd.DataFrame(all_pages)

ddl="""CREATE TABLE IF NOT EXISTS mascots_fountains (
ID int,
DESC_CLASIFICACION TEXT,
COD_BARRIO TEXT
BARRIO TEXT,
COD_DISTRITO TEXT,
DISTRITO TEXT,
ESTADO TEXT,
LATITUD REAL,
LONGITUD REAL,
TIPO_VIA TEXT,
NOM_VIA TEXT,
NUM_VIA TEXT,
COD_POSTAL TEXT,
DIRECCION_AUX TEXT,
NDP TEXT,
FECHA_INSTALACION TEXT,
UBICACION TEXT
) """
conn = sqlite3.connect('animal_fountains.db')
cursor = conn.cursor()
df.to_sql('fountains', conn, if_exists='replace', index=False)
conn.close()