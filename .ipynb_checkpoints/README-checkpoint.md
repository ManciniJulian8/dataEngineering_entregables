# Entregable 1

## Consigna:

Script que extraiga datos de una API pública y crear la tabla en Redshift para posterior carga de sus datos.

### Objetivos generales

✓ Tener un código inicial que será usado
en el proyecto final como un script ETL
inicial.

### Objetivos específicos

✓ El script debería extraer datos en JSON
y poder leer el formato en un
diccionario de Python.

✓ La entrega involucra la creación de una
versión inicial de la tabla donde los
datos serán cargados posteriormente.

Esto lo vamos a llevar a cabo usando `requests`, `Spark` y un driver de conexión de `Postgres`

Para correr el script de ejemplo Entregable1.ipynb se debe ejecutar el docker-compose que contiene el contenedor de Pyspark con Jupyter Notebook.

Docker Compose con Pyspark
Password o Token del Jupyter Notebook: coder

URL del Jupyter Notebook: http://localhost:8888/lab?token=coder