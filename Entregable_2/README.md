# Entregable 2

## Consigna:

Script que extraiga datos de una API pública para posterior carga de sus datos.
Script de entrega 1 ahora deberá cargar los datos en Amazon Redshift

### Objetivos generales

✓ El script de la entrega 1 deberá adaptar
datos leídos de la API y cargarlos en la
tabla creada en la pre-entrega anterior en
Redshift.

### Objetivos específicos

✓ Implementar funcionalidades de la librería
Pandas en el código cargándolos en la
tabla creada en la misma.

✓ Solucionar una situación real de ETL donde
puedan llegar a aparecer duplicados
durante la ingesta de los datos

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
