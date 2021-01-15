from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, SelectField, ValidationError, TimeField, validators
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
import time

class MovementForm(FlaskForm):
    lista_monedas = ['EUR','BTC','ADA','BCH','BSV','EOS','ETH','LTC','NBN','TRX','USDT','XLM','XRP']
    from_currency = SelectField('From', choices=[], validators=[DataRequired()])
    from_quantity = FloatField('Q', validators=[InputRequired(), NumberRange(min=0, message='Entrar un valor válido')])
    to_currency =  SelectField('To', choices=lista_monedas, validators=[DataRequired()])
    to_quantity = FloatField('Q', render_kw={'readonly': True})
    precio_unitario_to = FloatField('P.U.', render_kw={'readonly': True})
    date = StringField('Fecha', render_kw={'readonly': True}) 
    time = StringField('Hora', render_kw={'readonly': True}) 
    
    submit = SubmitField('Calcular')
    submit = SubmitField('Grabar')