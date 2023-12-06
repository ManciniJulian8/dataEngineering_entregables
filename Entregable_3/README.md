# Entregable 3

## Consigna:

Entregable 3 - Script de 2da entrega ahora deberá vivir en
un container de Docker y en un DAG de Apache Airflow

### Objetivos generales

✓ El script de la 2da entrega debe
correr en un container de Docker y
estará embebido en un DAG de
Airflow dentro del container.

### Objetivos específicos

✓ El container debe ser lo más liviano
posible como para que el script
funcione sin problemas. Cualquier
usuario podría correr el container y
que el script esté listo para su
ejecución.

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
