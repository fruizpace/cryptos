---
title: Proyecto Flask
author: Fiorella Ruiz
---
# Proyecto Flask: Simulador de cryptos 
##### (BootZ 6ª Ed.)

Simulador de inversiones en cryptos para jugar con los valores a ver si
puede hacer crecer su inversión en euros o no. Esta aplicación consta de tres páginas:
+ Inicio
+ Compra
+ Status

Esta aplicación permite consultar el precio de cada criptomoneda (hasta 12 monedas) usando la conexión con la api de coinmarketcap.com. En base a esta consulta usted podrá decidir si quiere adquirir la cantidad de criptomoneda elegida en la página **Compra**.

Toda compra, venta o intercambio de moneda queda debidamente grabada en una base de datos y todos los movimientos realizados se muestran en la tabla del **Inicio**.

Finalmente, podrá consultar el estatus de su inversión en euros: cuántos euros ha invertido y cual ha sido su ganancia accediendo a la página **Status**.