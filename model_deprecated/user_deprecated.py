from archivy import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname=db.Column(db.String(40),nullable=False)
    lastname=db.Column(db.String(40),nullable=False)
    email=db.Column(db.String(40),nullable=False,unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    projects = db.relationship('Project', backref='user', lazy=True)
