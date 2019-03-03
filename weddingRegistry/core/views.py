from flask import render_template,request,Blueprint, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from weddingRegistry.models import User
from weddingRegistry import db
from weddingRegistry.core.forms import UserSignUpForm
import datetime

core = Blueprint('core',__name__)

@core.route('/', methods=['GET', 'POST'])
def index():

    if current_user.is_authenticated:

        return redirect(url_for('core.auth'))

    else:
        form = UserSignUpForm()

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user_submited = User.query.filter_by(email=email).first()
            print(str(user_submited))

            if user_submited is None:
                flash(f"Correo no registrado")

                return redirect(url_for('core.index', _anchor='banner'))

            else:
                if (user_submited.check_password(password)):
                    login_user(user_submited)

                    return redirect(url_for('core.auth'))

                else:
                    flash(f"Contraseña equivocada")

                    return redirect(url_for('core.index', _anchor='banner'))


    return render_template('index.html', form=form)


@core.route('/auth', methods=['GET'])
@login_required
def auth():
    if current_user.is_RSVP == 1:
        return redirect(url_for('core.user_confirmed'))
    else:
        form = UserSignUpForm()
        guests = {'Marco','Ramón','Emmanuel','Martha','Emma Luz'}

        if form.validate_on_submit():

            return redirect(url_for('core.confirm'))

        return render_template('auth.html', form=form, guests=guests)




@core.route('/confirm/', methods=['POST'])
@login_required
def confirm():

    if request.method == "POST":
        guests = request.form.getlist("guests")

        user = User.query.filter_by(email=current_user.email).first()
        if user:
            user.guests_names = str(guests)
            user.is_RSVP = 1
            user.date_RSVP = datetime.datetime.now()

            db.session.commit()


    return redirect(url_for('core.user_confirmed'))


@core.route('/user_confirmed', methods=['GET'])
@login_required
def user_confirmed():

    return render_template('confirm.html')


@core.route('/user_confirmed/quinta_san_carlos', methods=['GET'])
@login_required
def quinta_san_carlos():

    return render_template('quinta-san-carlos.html')


@core.route('/user_confirmed/como_llegar', methods=['GET'])
@login_required
def how_to_get_there():

    return render_template('how-to-get-there.html')




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

    return render_template('not_auth.html')
