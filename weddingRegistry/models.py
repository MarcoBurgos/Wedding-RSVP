from weddingRegistry import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),nullable=False )
    email = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(10), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    guests_names = db.Column(db.String(128),nullable=False)
    is_RSVP = db.Column(db.Boolean)
    date_RSVP = db.Column(db.DateTime)

    def __init__(self, name, email, password, phone_number, guests, guests_names,is_RSVP, date_RSVP):
        self.name = name
        self.email = email
        self.password_hash = password
        self.phone_number = phone_number
        self.guests = guests
        self.guests_names = guests_names
        self.is_RSVP = is_RSVP
        self.date_RSVP = date_RSVP

    def check_password(self, passw):
        return check_password_hash(self.password_hash,passw)

    def __repr__(self):
        return f"User {self.email}"
