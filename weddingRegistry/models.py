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
    phone_number = db.Column(db.String(64), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    guests_names = db.Column(db.String(128),nullable=False)
    guests_confirmed = db.Column(db.String(128))
    total_guests = db.Column(db.Integer)
    is_RSVP = db.Column(db.Boolean)
    date_RSVP = db.Column(db.DateTime)
    update_date_RSVP = db.Column(db.DateTime)
    update_times = db.Column(db.Integer)

    def __init__(self, name, email, password, phone_number, guests, guests_names, guests_confirmed, total_guests, is_RSVP, date_RSVP, update_date_RSVP, update_times):
        self.name = name
        self.email = email
        self.password_hash = password
        self.phone_number = phone_number
        self.guests = guests
        self.guests_names = guests_names
        self.guests_confirmed = guests_confirmed
        self.total_guests = total_guests
        self.is_RSVP = is_RSVP
        self.date_RSVP = date_RSVP
        self.update_date_RSVP = update_date_RSVP
        self.update_times = update_times

    def check_password(self, passw):
        return check_password_hash(self.password_hash,passw)

    def __repr__(self):
        return f"User {self.email}"



CREATE TABLE public.user ( id SERIAL, name VARCHAR(64) NOT NULL, email VARCHAR(64), password_hash VARCHAR(256), phone_number VARCHAR(10) NOT NULL, guests INTEGER NOT NULL, guests_names VARCHAR(128) NOT NULL, guests_confirmed VARCHAR(128), total_guests INTEGER, "is_RSVP" BOOLEAN, "date_RSVP" TIMESTAMP, "update_date_RSVP" TIMESTAMP, update_times INTEGER, PRIMARY KEY (id));
