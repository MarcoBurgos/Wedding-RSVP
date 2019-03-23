import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config


load_dotenv()
app = Flask(__name__)


app.config.from_object(os.environ.get('APP_SETTINGS'))



mail = Mail(app)


################################################
#################Database setup#################
################################################




db = SQLAlchemy(app)
Migrate(app, db)
################################################################################################

################################################
###############Login configurations#############
################################################

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "core.not_auth"

################################################################################################

from weddingRegistry.core.views import core
from weddingRegistry.users.views import users
from weddingRegistry.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
