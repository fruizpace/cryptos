from movements import app
from movements.forms import MovementForm
from flask import Flask, render_template, request, url_for, redirect
import sqlite3
from datetime import date
import time
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
    conn.commit()
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
    response = requests.get(specific_url) #print(response.text)
    if response.status_code == 200:
        api = response.json()
        return api
    else: #(ConnectionError, Timeout, TooManyRedirects) as e:
        raise Exception("Problema de consulta tipo {}".format(response.status_code)) 


def calc_monedero():
    lista_monedas = ['BTC','ADA','BCH','BSV','EOS','ETH','LTC','BNB','TRX','USDT','XLM','XRP']
    monedero = {} # cuantas monedas tengo de cada cripto
    for moneda in lista_monedas:
        query = "SELECT sum(case when to_currency = ? then to_quantity else 0 end) - sum(case when  from_currency = ? then from_quantity else 0 end) as saldo_moneda FROM movements;"
        tmp = consulta(query, (moneda, moneda))
        saldo = tmp[0]['saldo_moneda']
        monedero[moneda] = saldo
    return monedero

@app.route('/')
def listaMovimientos(): # mostrar tabla SQL
    query = "SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, from_quantity/to_quantity as precio_unitario_to FROM movements;"
    compras = consulta(query)
    monedero_actual = calc_monedero()
    
    return render_template('movementsList.html', datos=compras, monedero=monedero_actual)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    # 1) Formulario vacío:
    if request.method == 'GET':
        form_vacio = MovementForm()
        monedero = calc_monedero()
        lista_from = ['EUR'] # crear una lista de monedas disponibles para FROM: EUR + las que tengan cantidad > 0 en mi monedero
        
        try:
            for moneda, q in monedero.items():
                if q>0:
                    lista_from.append(moneda)
            form_vacio.from_currency.choices = lista_from # choices necesita una lista
        except:
            monedero = 'vacio'
            form_vacio.from_currency.choices = lista_from
        
        print('es un GET')
        
        return render_template('purchase.html', form=form_vacio, vacio='yes', monedero=monedero)
    
    else: #2) request.method == 'POST': Grabar o Calcular
        form = MovementForm()
        form.from_currency.choices = [request.form.get('from_currency')] # bloqueamos la lista con  la moneda elegida
        form.to_currency.choices = [request.form.get('to_currency')] # bloqueamos la lista con  la moneda elegida
        monedero = calc_monedero()
        
        if  request.form.get('submit') == 'Grabar' and form.validate():
            try:
                print('GRABAR SQL')
                
                query = "INSERT INTO movements (date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES (?,?,?,?,?,?);"
                consulta(query, (request.form.get("date"), request.form.get("time"), request.form.get("from_currency"),
                                request.form.get("from_quantity"), request.form.get("to_currency"), request.form.get("to_quantity")))
                
                return redirect(url_for('listaMovimientos'))
            except:
                return redirect(url_for('listaMovimientos'))
        else:
            print('soy CALCULAR')
            
            amount = request.form.get('from_quantity') # x "simbolo" convierte a "convert"
            simbolo = request.form.get('from_currency') 
            convert = request.form.get('to_currency')
            
            #3) Errores en la conversión de monedas:
            try:
                if float(amount) <= 0:
                    error = 'Cifra no válida. Entre cantidad superior a 0.'
                    return render_template('purchase.html', form=form, vacio='yes', error_cantidad=error, monedero=monedero)
            except:
                error = 'Cifra no válida. Use el punto para separar decimales. No se admiten otros símbolos.'
                return render_template('purchase.html', form=form, vacio='yes', error_cantidad=error, monedero=monedero)
            
            if simbolo != 'EUR' and monedero[simbolo] < float(amount):
                error = 'Sólo dispones de {:.3f} {} para gastar.'.format(monedero[simbolo], simbolo)
                return render_template('purchase.html', form=form, vacio='yes', error_cantidad=error, monedero=monedero)
            
            if simbolo == convert:
                error = 'Las monedas From y To deben ser diferentes.'
                return render_template('purchase.html', form=form, vacio='yes', error_moneda_igual=error, monedero=monedero)
            
            if simbolo == 'EUR' and convert != 'BTC':
                error = 'Con EUR sólo puedes comprar BTC.'
                return render_template('purchase.html', form=form, vacio='yes', error_eur_btc=error, monedero=monedero)
            
            if simbolo != 'BTC' and convert == 'EUR':
                error = 'Sólo puedes comprar EUR con BTC.'
                return render_template('purchase.html', form=form, vacio='yes', error_cripto_eur=error, monedero=monedero)
            
            # 4) Finalmente: consulta a la API
            try:
                url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(amount, simbolo, convert, API_KEY)
                dicc = peticionAPI(url)
                q_to = dicc['data']['quote'][convert]['price'] # cantidad de monedas que podemos comprar (viene del API)
                precioUnitario = float(amount)/q_to
                
                fecha_compra = time.strftime("%d/%m/%Y") # fecha y hora del momento de la consulta API
                hora_compra = time.strftime("%X")
                
                return render_template('purchase.html', vacio='no', form=form, q_to="{:.3f}".format(q_to), precioUnitario="{:.8f}".format(precioUnitario), fecha_compra=fecha_compra, hora_compra=hora_compra, monedero=monedero)
            except Exception as error:
                return render_template('purchase.html', vacio='yes', form=form, error_conexion=error, monedero=monedero)

@app.route('/status')
def status():
    # 1)
    query1 = "SELECT SUM(from_quantity) as eur_from FROM movements WHERE from_currency='EUR';"
    total_diccionario = consulta(query1)
    total_eur_invertido = total_diccionario[0]['eur_from'] 
    
    #2)
    query2 = 'SELECT sum(case when to_currency = "EUR" then to_quantity else 0 end) - sum(case when  from_currency = "EUR" then from_quantity else 0 end) as saldo_eur from movements;'
    eur_diccionario = consulta(query2)
    saldo_euros_invertidos = eur_diccionario[0]['saldo_eur']
    
    #3) obtener precio unitario en EUR de todas las criptomonedas:
    simbolo = "BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX" # no debe tener espacios en blanco!
    convert = 'EUR'
    
    try:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(simbolo, convert, API_KEY)
        dicc = peticionAPI(url)
    except Exception as error:
        return render_template('status.html', error_conexion = error)
    
    lista_monedas = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH','BNB', 'USDT','EOS','BSV','XLM','ADA','TRX']
    pu_crypto_eur = {}
    id_cryptos = {}
    for moneda in lista_monedas: # crear diccionario pu_crypto_eur
        precio = dicc['data'][moneda]['quote']['EUR']['price']
        id_crypto = dicc['data'][moneda]['id']
        pu_crypto_eur[moneda] = precio
        id_cryptos[moneda] = id_crypto #print(id_cryptos)
    
    #4)
    monedero = {} # cuantas monedas tengo de cada cripto
    monedero_eur = [] # valor en EUR de las monedas que tengo
    
    for moneda in lista_monedas:
        query3 = "SELECT sum(case when to_currency = ? then to_quantity else 0 end) - sum(case when  from_currency = ? then from_quantity else 0 end) as saldo_moneda FROM movements;"
        tmp = consulta(query3, (moneda, moneda))
        saldo = tmp[0]['saldo_moneda']
        
        monedero[moneda] = saldo
        
        precio_unitario = float(pu_crypto_eur[moneda])
        monedero_eur.append(saldo * precio_unitario)
    
    valor_total_cryptos = 0
    for item in monedero_eur:
        valor_total_cryptos += item
    
    valor_actual = total_eur_invertido + saldo_euros_invertidos + valor_total_cryptos # todo en euros!
    
    return render_template('status.html', invertido="{:.2f}".format(total_eur_invertido) , actual="{:.2f}".format(valor_actual))