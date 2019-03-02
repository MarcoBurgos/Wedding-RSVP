from weddingRegistry import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(10), nullable=False)
    is_RSVP = db.Column(db.Boolean)
    date_RSVP = db.Column(db.DateTime)

    def __init__(self, id, email, password, phone_number, is_RSVP, date_RSVP):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.phone_number = phone_number
        self.is_RSVP = is_RSVP
        self.date_RSVP = date_RSVP

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"User {self.email}"
