from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(16))

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posterName = db.Column(db.String(16))
    content = db.Column(db.String(1000))
    postTime = db.Column(db.Integer)
    likes = db.Column(db.Integer)