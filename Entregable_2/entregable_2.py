# 1) Importar las librerías
from configparser import ConfigParser
import sqlalchemy as sa
import os
import urllib.parse
import requests
import pandas as pd
import numpy as np


config = ConfigParser()

# 2) Definir funciones para conexión a base de datos

def build_conn_string(config_path, config_section):
    """
    Construye la cadena de conexión a la base de datos
    a partir de un archivo de configuración.
    """

    # Lee el archivo de configuración
    parser = ConfigParser()
    parser.read(config_path)

    # Lee la sección de configuración de PostgreSQL
    config = parser[config_section]
    host = config['host']
    port = config['port']
    dbname = config['dbname']
    username = config['username']
    pwd = config['pwd']

    # Construye la cadena de conexión
    conn_string = f'postgresql://{username}:{pwd}@{host}:{port}/{dbname}?sslmode=require'
    
    return conn_string

def connect_to_db(conn_string):
    """
    Crea una conexión a la base de datos.
    """
    engine = sa.create_engine(conn_string)
    conn = engine.connect()
    return conn, engine

"""
Por lo general, las APIs requieren autenticación
Para acceder a sus recursos, es necesario autenticarse usando Key, por ejemplo.
Cada una API tiene su forma de brindarte la/s clave/s
"""

config_dir = "Entregable_2/config/config.ini"

config.read(config_dir)

# 3)Armamos la url con el endpoint y especificando las credenciales como parámetros
def get_api_call(ids, **kwargs):
    API_BASE_URL = config["api_datos_argentina"]['API_BASE_URL']
    kwargs["ids"] = ",".join(ids)
    return f"{API_BASE_URL}{"series"}?{urllib.parse.urlencode(kwargs)}"

api_call = get_api_call([config["api_datos_argentina"]['ids']], 
                        start_date=config["api_datos_argentina"]['start_date'], 
                        end_date=config["api_datos_argentina"]['end_date'])
print(api_call)

# 4) Generamos la consulta  la API
result = requests.get(api_call).json()
print(result)

# 5)1) Creación de dataframe a partir de la data extraída
# Tenemos una lista de diccionario
# Entonces, podemos crear un DataFrame
data = result["data"]
df_exportaciones = pd.DataFrame(data,columns=["date_from", "millones_dolares"])

# 5)2) Transformación de la información extraída de la API

#se incorporá la frecuencia de la data

df_exportaciones['frequency'] = "Mensual"

#otra transformación que se hará, es extraer el mes de la fecha
df_exportaciones['date_from'] = pd.to_datetime(df_exportaciones['date_from'])
df_exportaciones['month'] = df_exportaciones['date_from'].dt.month

# Existencia de duplicados

if df_exportaciones.duplicated().sum() == 0:
    print("No existen duplicados")
else:
    print("Existen {cantidad} registros duplicados".format(cantidad = df_exportaciones.duplicated.sum()))

print(df_exportaciones.info())

# 6) Carga de datos
conn_str = build_conn_string('Entregable_2/config/config.ini', 'redshift')
conn, engine = connect_to_db(conn_str)

schema = "mancinijulian8_coderhouse"

#6)1)Creación de tabla en redshift con python
    # La elección de la sort_key en este caso es por la columna "date_from" permitiendo ordenar la tabla en torno a esta, pra una mayor eficiencia en las consultas a la base
    #La elección del Distribution Styles corresponde a distkey correspondiente a la columns "date_from" que es una columna de fecha y permitirá que la data se distribuya en las slices de acuerdo a esta
conn.execute(
    f"""
        DROP TABLE IF EXISTS {schema}.exportaciones_productos_primarios;
        CREATE TABLE {schema}.exportaciones_productos_primarios (
            date_from TIMESTAMP distkey,
            millones_dolares FLOAT,
            frequency VARCHAR,
            month INT
        )sortkey(date_from);
    """
)

#6)2) Carga de datos en tabla de Amazon Redshift

#la elección de los parámetros  if_exists='append' es porque quiero mantener la estructura de la tabla definida en el create_table, ya que pandas en el caso de "replace" la borrar+ia y crearí sin respetar la sortkey ni distribution_styles
#Si bien el riesgo de usar 'append' es la posibilidad de incluir duplicados, esto está resuelto más arriba con la lógica de pandas en python

#la elección de method="multi" es para que panas no haga la carga de a una fila por vez

df_exportaciones.to_sql(
    name="exportaciones_productos_primarios",
    con=conn,
    schema=schema,
    if_exists="append",
    method="multi",
    index=False,
    )




