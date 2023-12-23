import logging
import json
from configparser import ConfigParser

import requests
from sqlalchemy import create_engine
from pandas import json_normalize, to_datetime, concat
import urllib.parse
config = ConfigParser()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_api_call(ids, **kwargs):
    API_BASE_URL = config["api_datos_argentina"]['API_BASE_URL']
    kwargs["ids"] = ",".join(ids)
    return f"{API_BASE_URL}\"series\"?{urllib.parse.urlencode(kwargs)}"
    
def connect_to_db(config_file, section):
    """
    Crea una conexión a la base de datos especificada en el archivo de configuración.

    Parameters:
    config_file (str): La ruta del archivo de configuración.
    section (str): La sección del archivo de configuración que contiene los datos de la base de datos.

    Returns:
    sqlalchemy.engine.base.Engine: Un objeto de conexión a la base de datos.
    """
    try:
        parser = ConfigParser()
        parser.read(config_file)

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            db = {param[0]: param[1] for param in params}

            logging.info("Conectándose a la base de datos...")
            engine = create_engine(
                f"postgresql://{db['user']}:{db['pwd']}@{db['host']}:{db['port']}/{db['dbname']}"
                , connect_args={"options": f"-c search_path={db['schema']}"}
                )

            logging.info("Conexión a la base de datos establecida exitosamente")
            return engine

        else:
            logging.error(f"Sección {section} no encontrada en el archivo de configuración")
            return None
        
    except Exception as e:
        logging.error(f"Error al conectarse a la base de datos: {e}")
        return None
    
def load_to_sql(df, table_name, engine, check_field):
    """
    Cargar un dataframe en una tabla de base de datos,
    usando una tabla intermedia o stage para control de duplicados.

    Parameters:
    df (pandas.DataFrame): El DataFrame a cargar en la base de datos.
    table_name (str): El nombre de la tabla en la base de datos.
    engine (sqlalchemy.engine.base.Engine): Un objeto de conexión a la base de datos.
    check_field (str): El nombre de la columna que se usará para controlar duplicados.
    """
    try:
        with engine.connect() as conn:
            logging.info(f"Cargando datos en la tabla {table_name}_stg...")
            conn.execute(f"TRUNCATE TABLE {table_name}_stg")
            df.to_sql(
                f"{table_name}_stg", conn,
                if_exists="append", method="multi",
                index=False
                )
            logging.info(f"Datos cargados exitosamente")
            logging.info(f"Cargando datos en la tabla {table_name}...")
            conn.execute(f"""
                BEGIN;
                DELETE FROM {table_name}
                USING {table_name}_stg
                WHERE {table_name}.{check_field} = {table_name}_stg.{check_field};

                INSERT INTO {table_name}
                SELECT * FROM {table_name}_stg;
                COMMIT;
                """)
            logging.info("Datos cargados exitosamente")
    except Exception as e:
        logging.error(f"Error al cargar los datos en la base de datos: {e}")