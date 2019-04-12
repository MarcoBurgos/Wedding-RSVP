from flask import render_template,request,Blueprint, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from weddingRegistry.models import User
from weddingRegistry import db
from weddingRegistry.fetch_playlist import get_tracks
from weddingRegistry.core.forms import UserSignUpForm
from datetime import datetime, timedelta
import os
import re

core = Blueprint('core',__name__)

@core.route('/', methods=['GET', 'POST'])
def index():

    if current_user.is_authenticated:

        return redirect(url_for('core.user_confirmed'))

    else:
        form = UserSignUpForm()

        if form.validate_on_submit():
            email = form.email.data.lower()
            password = form.password.data
            try:
                user_submited = User.query.filter_by(email=email).first()
            except Exception as e:
                abort(500,e)


            if user_submited is None:
                flash(f"Correo no registrado")

                return redirect(url_for('core.index', _anchor='banner'))

            else:
                if (user_submited.check_password(password)):
                    login_user(user_submited)

                    if(current_user.is_RSVP==1):
                        return redirect(url_for('core.user_confirmed'))
                    else:
                        return redirect(url_for('core.auth'))

                else:
                    flash(f"Contraseña equivocada")

                    return redirect(url_for('core.index', _anchor='banner'))


    return render_template('index.html', form=form)


@core.route('/auth:confirmar-invitados', methods=['GET'])
@login_required
def auth():

    form = UserSignUpForm()
    name = current_user.name
    tickets = current_user.guests

    is_update = current_user.is_RSVP is True

    if is_update:
        if current_user.guests_confirmed is None:
            guests_confirmed = None
            guests_not_confirmed = current_user.guests_names.split(",")

        else:
            guests_confirmed = current_user.guests_confirmed.split(",")
            guests_not_confirmed = current_user.guests_names.split(",")
            guests_not_confirmed = set(guests_not_confirmed) - set(guests_confirmed)
    else:
        guests_confirmed = current_user.guests_names.split(",")
        guests_not_confirmed = None

    if form.validate_on_submit():

        return redirect(url_for('core.confirm'))

    return render_template('auth.html', form=form, guests=guests_confirmed, guests_not=guests_not_confirmed, name=name, tickets=tickets)




@core.route('/confirm/', methods=['POST'])
@login_required
def confirm():

    if request.method == "POST":
        guests = request.form.getlist("guests")

        try:
            user = User.query.filter_by(email=current_user.email).first()
        except Exception as e:
            abort(500,e)


        if user:
            user.total_guests = len(guests)
            if len(guests) == 0:
                user.guests_confirmed = None
            else:
                guests = ",".join(guests)
                guests = re.sub("[']", "", str(guests))
                user.guests_confirmed = guests

            if current_user.is_RSVP ==  True:
                user.update_date_RSVP = (datetime.now()) - (timedelta(hours=4, minutes=00))
                edit = current_user.update_times
                edit += 1
                user.update_times = edit
            else:
                user.is_RSVP = True
                user.date_RSVP = (datetime.now()) - (timedelta(hours=4, minutes=00))

            db.session.commit()

    return redirect(url_for('core.user_confirmed'))


@core.route('/user_confirmed', methods=['GET'])
@login_required
def user_confirmed():
    name = current_user.name
    admins = os.environ.get('ADMINS')

    return render_template('confirm.html', name=name, admins=admins)


@core.route('/user_confirmed/quinta_san_carlos', methods=['GET'])
@login_required
def quinta_san_carlos():

    return render_template('quinta-san-carlos.html')


@core.route('/user_confirmed/como-llegar', methods=['GET'])
@login_required
def how_to_get_there():

    return render_template('how_to_get_there.html')


@core.route('/user_confirmed/mesa-regalos', methods=['GET'])
@login_required
def registry():

    return render_template('registry.html')

@core.route('/user_confirmed/vuelos', methods=['GET'])
@login_required
def flights():

    return render_template('flights.html')


@core.route('/user_confirmed/playlist', methods=['GET'])
@login_required
def playlist():

    tracks = get_tracks()

    return render_template('music.html', tracks=tracks)

@core.route('/user_confirmed/preguntas-frecuentes', methods=['GET'])
@login_required
def faq():

    return render_template('faq.html')

@core.route('/user_confirmed/otros-hospedaje', methods=['GET'])
@login_required
def others():

    return render_template('others.html')


@core.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@core.route('/login', methods=['GET'])
def login():

    return redirect(url_for('core.index'))


@core.route('/not_auth', methods=['GET'])
def not_auth():

    return render_template('error_pages/403.html')

@core.errorhandler(500)
def internal_error(error):
    admin = os.environ.get('ADMINS')
    admin = admin.split(",")
    admin = admin[0][2:-1]
    user = current_user.email
    send_email(admin, "Error en la plataforma", render_template('template_error.html', error=error, user=user))
    return render_template('error_pages/500.html')
