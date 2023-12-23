

# Data Engineering Consigna del Proyecto Final

## Consigna:

ETL completo en Airflow


### Objetivos generales

✓ Crear un pipeline que extraiga datos de una API pública de forma constante combinándolos con información extraída de una base de datos (mínimamente estas 2 fuentes de datos, pero pueden utilizarse hasta 4).

✓ Colocar los datos extraídos en un Data Warehouse. 

✓ Automatizar el proceso que extraerá, transformará y cargará datos cuantitativos (ejemplo estos son: valores de acciones de la bolsa, temperatura de ciudades seleccionadas, valor de una moneda comparado con el dólar, casos de covid). 

✓ Automatizar el proceso para lanzar alertas (2 máximo) por e-mail en caso de que un valor sobrepase un límite configurado en el código.


### Desarrollo

Para este ejemplo voy a utilizar la API de [Datos Argentina](https://www.datos.gob.ar/)

Y voy a extraer los datos de: Exportaciones de productos primarios. En millones de dólares FOB

Para probar la API ir a: [API de Series de Tiempo AR: Generador de URLs](https://datosgobar.github.io/series-tiempo-ar-call-generator/)

Los paso realizados para la realización de este entregable son los siguientes:

1) Importar las librerías
2) Definir funciones para conexión a base de datos
3) Armamos la url con el endpoint y especificando las credenciales como parámetros
4) Generamos la consulta  la API
5) Consulta a la API
5) 1) Generamos la consulta  la API
5) 2) Transformación con pandas de la información extraída de la API
6) Carga de datos
6) 1) Creación de tabla en redshift con python
6) 2) Carga de datos en tabla de Amazon Redshift
7) 1) Automatización a través de Dags de airflow
7) 1) Envío de mail de notificación del proceso