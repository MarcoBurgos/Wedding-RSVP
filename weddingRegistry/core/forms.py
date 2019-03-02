from flask_wtf import FlaskForm
from wtforms import (StringField,SelectField,TextAreaField,PasswordField,SubmitField)
from wtforms.validators import DataRequired, url, Email

class UserSignUpForm(FlaskForm):
    email = StringField('Ingresa el email registrado', validators=[DataRequired(), Email()])
    password = PasswordField("Ingresa la contraseña que recibiste por correo", validators=[DataRequired()] )
    submit = SubmitField('Recibir mi contraseña')
