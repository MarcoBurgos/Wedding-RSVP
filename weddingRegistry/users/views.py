from flask import render_template,request,Blueprint, redirect, url_for
from weddingRegistry.models import User
from weddingRegistry.users.forms import addUserForm

users = Blueprint('users',__name__)

@users.route('/add_guest', methods=['GET','POST'])
def add_guest():
    form = addUserForm()

    return render_template('add_guest.html', form=form)
