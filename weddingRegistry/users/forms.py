from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField)
from wtforms.validators import DataRequired, url, Email

class addUserForm(FlaskForm):
    name = StringField('Nombre del invitado registrado')
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Número de teléfono')
    guests = StringField('Número de pases')
    guests_names = StringField('Nombre de los invitados')
    submit = SubmitField('Crear invitado')
