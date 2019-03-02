import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager

#flask db init
#flask db migrate  -m "message"
#flask db upgrade
# os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'
#
# #export OAUTHLIB_INSECURE_TRANSPORT=1
# export FLASK_ENV=development
#python app.py


app = Flask(__name__)


app.config['SECRET_KEY'] = 'WR20190205'


################################################
#################Database setup#################
################################################
basedir = os.path.abspath(os.path.dirname(__file__ ))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
################################################################################################

################################################
###############Login configurations#############
################################################

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "users.login"

################################################################################################

from weddingRegistry.core.views import core
from weddingRegistry.users.views import users
from weddingRegistry.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
