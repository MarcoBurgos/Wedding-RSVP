from flask import render_template,request,Blueprint, redirect, url_for, flash, jsonify
from flask_mail import Mail
from weddingRegistry import db
from flask_login import login_required, current_user
from weddingRegistry.models import User, generate_password_hash
from weddingRegistry.users.forms import addUserForm
from weddingRegistry.core.forms import UserSignUpForm
from weddingRegistry.send_mail import send_email
import random, string
from weddingRegistry import app

users = Blueprint('users',__name__)

@users.route('/add_guest', methods=['GET','POST'])
@login_required
def add_guest():
    form = addUserForm()

    if form.validate_on_submit():
        user = User(email = form.email.data,
                       name = form.name.data,
                       password = None,
                       phone_number = form.phone_number.data,
                       guests = form.guests.data,
                       guests_names = form.guests_names.data,
                       is_RSVP = 0,
                       date_RSVP = None)
#''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        db.session.add(user)
        db.session.commit()
        flash(f"Invitado registrado {user.email}")

        return redirect(url_for('users.add_guest'))

    return render_template('add_guest.html', form=form)



@users.route('/register', methods=['GET','POST'])
def register():
    form = addUserForm()


    return render_template('register.html', form=form)



@users.route('/background_process', methods=['POST'])
def background_process():

    form = addUserForm()

    email = request.form['email']


    user = User.query.filter_by(email=form.email.data).first()

    if user and not user.password_hash:
        pass_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        user.password_hash = generate_password_hash(pass_string)

        mail_body = f"""
        <p>¡Bienvenido! Gracias por registrarte, por favor usa esta contraseña para iniciar sesión y confirmar tu asistencia a la boda:</p>
        <p>Tu contraseña es <strong> {pass_string} </strong></p>
        <p>Sigue esta liga y completa tu confirmación</p>
        <p><a href="http://127.0.0.1:5000/">Boda Angie & Marco </a></p>
        <br>
        <p>¡Gracias y nos vemos el 17 de noviembre!</p>
        """
        print(f"user.email is {user.email}")
        send_email(user.email, "Contraseña para Boda Angie & Marco", mail_body)

        db.session.commit()
        return jsonify(result='success')

    elif user and user.password_hash:
        return jsonify(result='repeated')
    else:
        return jsonify(result='not-found')
