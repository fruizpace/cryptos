---
title: Proyecto Flask
author: Fiorella Ruiz
---
# Proyecto Flask: Simulador de cryptos 
## Instrucciones de instalación 

### Desde Visual Studio + Windows:
*Nota: Asumimos que tienes instalado Git y SQLITE3 en tu sistema local.*
1. Crea una carpeta de trabajo.
2. Desde Visual Studio y dentro de la carpeta de trabajo abre una nueva terminal e instala el entorno virtual: ```python -m venv venv``` . Ojo, Si no funciona probar con *python3*.
3. Activa el entorno virtual: ```venv\Scripts\activate```
4. Copia la URL del respositorio remoto usando el icono "Copy to clipboard" y clona el repositorio con el siguiente comando:  ```git clone https://github.com/fruizpace/cryptos.git ```. Se descargará la carpeta cryptos con todos los archivos necesarios.
5. Dentro de la carpeta cryptos ejecutar el comando: ```pip install -r requirements.txt``` para instalar todas las librerías necesarias para la aplicación.
6. En la carpeta Cryptos crear un archivo .env y escribir dentro las variables de entorno: 
- FLASK_APP=run.py
- FLASK_ENV=development
7. En la carpeta Cryptos crear un archivo config.py basado en config_template.py y reemplaza cada contenido de las variables de entorno: 
- 'pon aquí tu clave para CSRF' --> '&Gw&fpt#2JT?#ag'
- 'ruta de mi base de datos db' --> 'movements/data/basededatos.db'
- 'clave para acceder al API de currencymarket'  -->  '1f7a2e8f-a55d-4bf2-895d-d26e6dd0488c'
8.  Para crear la base de datos, entra en las carpetas movements/data y en el terminal escribe los comandos:
```
> sqlite3 basededatos.db
> .read migrations/initial.sql
> .schema
> .q
```
9. Finalmente, vuelve a la carpeta Cryptos y escribe en el terminal: ```flask run```

## Sobre la aplicación:

Simulador de inversiones en cryptos para jugar con valores reales. 

Esta aplicación consta de tres páginas:
+ Inicio
+ Compra
+ Status

Esta aplicación permite consultar el precio de cada criptomoneda (hasta 12 monedas) usando la conexión con la api de coinmarketcap.com. En base a esta consulta usted podrá decidir si quiere adquirir la cantidad de criptomoneda elegida en la página **Compra**.
Para ello siga las intrucciones:

1. **Primera compra:** Use Euros (EUR) para obtener Bitcoins (BTC).
2. Con el botón **calcular** se le informará del precio y cantidad de monedas que puede conseguir. 
3. Para borrar el formulario puede usar el botón **limpiar**.
4. Para validar la compra pulse **aceptar**. El movimiento quedará registrado y no podrá borrarse de la tabla de movimientos.
5. **Siguientes compras:** Una vez tenga BTC podrá adquirir otras criptomonedas disponibles en la lista desplegable *To*.
6. Finalmente, si desea obtener EUR sólo podrá hacerlo mediante BTC.

Toda compra, venta o intercambio de moneda queda debidamente grabada en una base de datos y todos los movimientos realizados se muestran en la tabla del **Inicio**.

Por último, podrá consultar el estatus de su inversión en euros: cuántos euros ha invertido y cual ha sido su ganancia accediendo a la página **Status**.