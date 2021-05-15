from flask_login import UserMixin
from . import db
import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


