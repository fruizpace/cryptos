---
title: Proyecto Flask
author: Fiorella Ruiz
---
# Proyecto Flask: Simulador de cryptos 
##### (BootZ 6ª Ed.)

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