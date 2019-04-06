from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField, IntegerField, BooleanField)
from wtforms.validators import DataRequired, url, Email

class addUserForm(FlaskForm):
    name = StringField('Nombre del invitado registrado')
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Número de teléfono')
    guests = IntegerField('Número de pases')
    guests_names = StringField('Nombre de los invitados')
    submit = SubmitField('Crear invitado')


class editUserForm(FlaskForm):
    name = StringField('Nombre del invitado registrado')
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_active = StringField('Solicitó contraseña')
    phone_number = StringField('Número de teléfono')
    number_of_tickets = IntegerField('Número de pases registrados')
    guests_names = StringField('Nombre de los invitados registrados')
    guests_confirmed = StringField('Nombre de los invitados confirmados')
    total_guests = IntegerField('Número de pases confirmados')
    is_RSVP = BooleanField('¿Realizó confirmación?')
    date_RSVP = StringField('Fecha de confirmación')
    update_date_RSVP = StringField('Fecha de actualización de confirmación')
    update_times = IntegerField('Número de actualizaciones realizadas')
    submit = SubmitField('Actualizar invitado')
