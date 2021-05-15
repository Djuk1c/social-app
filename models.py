from flask_login import UserMixin
from sqlalchemy.orm import backref
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(16))

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posterName = db.Column(db.String(16))
    content = db.Column(db.String(1000))
    postTime = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    likes = db.Column(db.String)
    image = db.Column(db.String, default='none')
    comments = db.relationship('Comments', backref='originalPost')

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posterName = db.Column(db.String(16))
    content = db.Column(db.String(1000))
    postTime = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))