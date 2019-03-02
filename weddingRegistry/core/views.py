from flask import render_template,request,Blueprint, redirect, url_for
from weddingRegistry.models import User
from weddingRegistry.core.forms import UserSignUpForm

core = Blueprint('core',__name__)

@core.route('/', methods=['GET','POST'])
def index():
    form = UserSignUpForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        return redirect(url_for('core.register', _anchor="banner", email=email))

        # user = db.session.query(User).filter(email == User.email).first()
        # return redirect(url_for('core.register', user=user.email))


    return render_template('testindex.html', form=form)


@core.route('/register/<string:email>', methods=['GET','POST'])
def register(email):

    return render_template('register.html', email=email, password="pasword")
