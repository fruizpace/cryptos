from movements import app
from flask import Flask, render_template, request, url_for, redirect
import sqlite3
from datetime import date

import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

API_KEY =  app.config['API_KEY']
DBFILE = app.config['DBFILE']

def consulta(query, params=()):
    ## función 1: establecer conexión con sqlite3
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()
    c.execute(query, params)
    filas = c.fetchall()
    conn.close
    
    ## función 2: dar formato a la consulta como lista de diccionarios
    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0]) 

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames): # enumerate() te da una tupla con el índice y el elemento.
            d[columnName] = fila[ix] 
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios 


def peticionAPI(specific_url):
    try:
        response = requests.get(specific_url)
        #print(response.text)
        api = response.json()
        return api
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)



@app.route('/')
def listaMovimientos():
    # mostrar tabla SQL
    query = "SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, from_quantity/to_quantity as precio_unitario_to FROM movements;"
    compras = consulta(query)
    
    for d in compras:
        d['from_quantity'] = "{:.2f}".format(float(d['from_quantity']))
        d['to_quantity'] = "{:.2f}".format(float(d['to_quantity']))
        d['precio_unitario_to'] = str("{:.4f}".format(float(d['precio_unitario_to']))) + ' ' + d['from_currency']
    
    
    return render_template('movementsList.html', datos=compras)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    
    if request.method == 'GET':
        print('soy un get')
    else:
        print('soy un post')
    
    # para obtener precio unitario (¿CUANTOS EUROS CUESTA 1 BTC?)
    simbolo = 'BTC'
    amount = 1 
    convert = 'EUR'

    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(amount, simbolo, convert, API_KEY)
    dicc = peticionAPI(url)
    print(dicc['data']['quote']['EUR']['price'])
    
    
    
    
    # obtener datos del formulario
    # query: GRABAR datos en la bd SQL
    return render_template('purchase.html')


@app.route('/status')
def status():
    # 1)
    query1 = "SELECT SUM(from_quantity) as eur_from FROM movements WHERE from_currency='EUR';"
    total_diccionario = consulta(query1)
    total_eur_invertido = total_diccionario[0]['eur_from'] # string! PASAR A FLOAT!!! o usar eval
    
    #2)
    query2 = 'SELECT sum(case when to_currency = "EUR" then to_quantity else 0 end) - sum(case when  from_currency = "EUR" then from_quantity else 0 end) as saldo_eur from movements;'
    eur_diccionario = consulta(query2)
    saldo_euros_invertidos = eur_diccionario[0]['saldo_eur']
    
    
    #2.5) obtener precio unitario en EUR  de todas las criptomonedas:
    '''
    simbolo = 'BTC'
    amount = 1 # para obtener precio unitario (¿CUANTOS EUROS CUESTA 1 BTC?)
    convert = 'EUR'

    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(amount, simbolo, convert, API_KEY)
    dicc = peticionAPI(url)
    print(dicc['data']['quote']['EUR']['price'])
    '''
    
    #3)
    lista_monedas = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH','BNB', 'USDT','EOS','BSV','XLM','ADA','TRX']
    pu_crypto_eur = {'BTC':'8000.14', 'ETH':'159.3656', 'XRP':'322.1', 'LTC':'54.5198', 'BCH':'0.0006','BNB':'5400.23', 'USDT':'2.3','EOS':'0.09','BSV':'1.33','XLM':'0.9','ADA':'0.002','TRX':'2.6'}
    monedero = {}
    monedero_eur = []
    
    for moneda in lista_monedas:
        query3 = "SELECT sum(case when to_currency = ? then to_quantity else 0 end) - sum(case when  from_currency = ? then from_quantity else 0 end) as saldo_moneda FROM movements;"
        tmp = consulta(query3, (moneda, moneda))
        saldo = tmp[0]['saldo_moneda']
        
        monedero[moneda] = saldo
        
        precio_unitario = float(pu_crypto_eur[moneda])
        monedero_eur.append(saldo * precio_unitario)
    
    #4)
    valor_total_cryptos = 0
    for item in monedero_eur:
        valor_total_cryptos += item
    
    valor_actual = total_eur_invertido + saldo_euros_invertidos + valor_total_cryptos # todo en euros!
    
    
    return render_template('status.html', invertido="{:.2f}".format(total_eur_invertido) , actual="{:.2f}".format(valor_actual), monedero=monedero, monedero_eur=monedero_eur)