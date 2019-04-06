import os
from flask import render_template,request,Blueprint, redirect, url_for, flash, jsonify, abort
from flask_mail import Mail
from weddingRegistry import db
from flask_login import login_required, current_user
from weddingRegistry.models import User, generate_password_hash
from weddingRegistry.users.forms import addUserForm, editUserForm
from weddingRegistry.core.forms import UserSignUpForm
from weddingRegistry.send_mail import send_email
import random, string
from weddingRegistry import app
import time
from datetime import datetime

users = Blueprint('users',__name__)


@users.route('/admin', methods=['GET','POST'])
@login_required
def admin():
    if current_user.is_authenticated and current_user.email in os.environ.get('ADMINS'):
        try:
            users = User.query.order_by(User.id.asc()).all()
            confirmed_users = User.query.filter_by(is_RSVP=True).order_by(User.id.asc()).all()
            pending_users = User.query.filter(User.is_RSVP.isnot(True)).order_by(User.id.asc()).all()
        except Exception as e:
            abort(500,e)

        return render_template('dashboard.html', users=users, name=current_user.name, pendings=pending_users, confirms=confirmed_users)
    else:
        return redirect(url_for('core.not_auth'))



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
                       guests_confirmed = None,
                       total_guests = 0,
                       is_RSVP = False,
                       date_RSVP = None,
                       update_date_RSVP = None,
                       update_times = 0)
        db.session.add(user)
        db.session.commit()
        flash(f"Invitado registrado {user.email}")

        return redirect(url_for('users.add_guest'))

    return render_template('add_guest.html', form=form)


@users.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if current_user.is_authenticated and current_user.email in os.environ.get('ADMINS'):
        if user.email not in os.environ.get('ADMINS'):
            flash(f"Eliminaste al invitado: {user.id}, {user.name}")
            db.session.delete(user)
            db.session.commit()
        else:
            flash(f"Nice try! No puedes eliminar a los Administradores, sucker!")
            return redirect(url_for('users.admin'))
    else:
        return redirect(url_for('core.not_auth'))

    return redirect(url_for("users.admin"))


@users.route('/<int:user_id>/update', methods=['GET', 'POST'])
@login_required
def update_user(user_id):

    user = User.query.get_or_404(user_id)

    if current_user.is_authenticated and current_user.email in os.environ.get('ADMINS'):
        if user.email not in os.environ.get('ADMINS'):
            form = editUserForm()

            if form.validate_on_submit():

                user.name = form.name.data
                user.email = form.email.data

                if form.is_active.data is None or len(form.is_active.data)<1:
                    user.password_hash = None

                user.phone_number = form.phone_number.data
                user.guests = form.number_of_tickets.data
                user.guests_names = form.guests_names.data

                if form.guests_confirmed.data is None or len(form.guests_confirmed.data)<1:
                    user.guests_confirmed = None
                else:
                    user.guests_confirmed = form.guests_confirmed.data


                user.total_guests = form.total_guests.data
                user.is_RSVP = form.is_RSVP.data

                if form.date_RSVP.data is None or len(form.date_RSVP.data)<1:
                    user.date_RSVP = None
                else:
                    user.date_RSVP = datetime.strptime(form.date_RSVP.data,'%Y-%m-%d %H:%M:%S.%f')


                if form.update_date_RSVP.data is None or len(form.update_date_RSVP.data)<1 :
                    user.update_date_RSVP = None
                else:
                    user.update_date_RSVP = datetime.strptime(form.update_date_RSVP.data,'%Y-%m-%d %H:%M:%S.%f')

                user.update_times = form.update_times.data

                db.session.commit()
                flash(f"Actualizaste al invitado id: {user.id}, {user.name}")

                return redirect(url_for('users.admin'))

            elif request.method == 'GET':
                form.name.data = user.name
                form.email.data = user.email
                form.is_active.data = user.password_hash
                form.phone_number.data = user.phone_number
                form.number_of_tickets.data = user.guests
                form.guests_names.data = user.guests_names
                form.guests_confirmed.data = user.guests_confirmed
                form.total_guests.data = user.total_guests
                form.is_RSVP.data = user.is_RSVP
                form.date_RSVP.data = user.date_RSVP
                form.update_date_RSVP.data = user.update_date_RSVP
                form.update_times.data = user.update_times

            return render_template('edit_guest.html', user=user, form=form)
        else:
            flash(f"Nice try! No puedes editar a los Administradores, sucker!")
            return redirect(url_for('users.admin'))

    else:
        return redirect(url_for('core.not_auth'))



@users.route('/register', methods=['GET','POST'])
def register():
    form = addUserForm()


    return render_template('register.html', form=form)



@users.route('/background_process', methods=['POST'])
def background_process():

    form = addUserForm()

    email = request.form['email'].lower()

    try:
        user = User.query.filter_by(email=email).first()
    except Exception as e:
        abort(500,e)


    if user and not user.password_hash:
        pass_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        user.password_hash = generate_password_hash(pass_string)

        try:
            send_email(user.email, "Contraseña para Boda Angie & Marco", render_template('password_register_template.html', pass_string=pass_string) )
            db.session.commit()
            return jsonify(result='success')
        except Exception as e:
            return jsonify(result='error')


    elif user and user.password_hash:
        return jsonify(result='repeated')
    else:
        return jsonify(result='not-found')


@users.route('/recordatorios', methods=['GET','POST'])
@login_required
def reminders():
    if current_user.is_authenticated and current_user.email in os.environ.get('ADMINS'):
        try:
            pending_users = User.query.filter(User.is_RSVP.isnot(True)).order_by(User.id.asc()).all()
        except Exception as e:
            abort(500,e)

        return render_template('send_reminders.html', pendings=pending_users, amount_pendings=len(pending_users))
    else:
        return redirect(url_for('core.not_auth'))


@users.route('/reminders-background', methods=['POST'])
@login_required
def reminders_bgprocess():
    if current_user.is_authenticated and current_user.email in os.environ.get('ADMINS'):
        try:
            pending_users = User.query.filter(User.is_RSVP.isnot(True)).order_by(User.id.asc()).all()
        except Exception as e:
            abort(500,e)

        try:
            for user in pending_users:
                send_email(user.email, "Recordatorio confirmación para Boda Angie & Marco", render_template('reminder_mail_template.html'))

            return jsonify(total_mails=True)

        except Exception as e:
            return jsonify(total_mails=False)

@users.errorhandler(500)
def internal_error(error):
    admin = os.environ.get('ADMINS')
    admin = admin.split(",")
    admin = admin[0][2:-1]
    user = current_user.email
    send_email(admin, "Error en la plataforma", render_template('template_error.html', error=error, user=user))
    return render_template('error_pages/500.html')
