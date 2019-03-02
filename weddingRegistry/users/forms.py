from flask_wtf import FlaskForm
from wtforms import (StringField,SelectField,TextAreaField,PasswordField,BooleanField,SubmitField)
from wtforms.validators import DataRequired, url, Email

class addUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Número de teléfono')
    submit = SubmitField('Crear invitado')
