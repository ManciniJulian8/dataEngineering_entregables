from datetime import datetime, timedelta
from configparser import ConfigParser
import pandas as pd

from utils import *

config = ConfigParser()

base_url = "https://apis.datos.gob.ar/series/api/"

def load_exportaciones_data(config_file):
    """
    Proceso ETL para los datos de exportaciones productos primarios
    """
    
    try:
        api_call = get_api_call([config["api_datos_argentina"]['ids']], 
                        start_date=config["api_datos_argentina"]['start_date'], 
                        end_date=config["api_datos_argentina"]['end_date'])
        # 4) Generamos la consulta  la API
        result = requests.get(api_call).json()

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
        
        engine = connect_to_db(config_file, "redshift")
        load_to_sql(df_exportaciones, "exportaciones_productos_primarios", engine, check_field="date_from")
        
    except Exception as e:
        logging.error(f"Error al obtener datos de {base_url}: {e}")
        raise e

if __name__ == "__main__":
    load_exportaciones_data("airflow/config/config.ini")