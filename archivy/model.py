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

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(500), nullable=False)
    conversations = db.relationship('Conversation', backref='project', lazy=True)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    projectid = db.Column(db.Integer, db.ForeignKey('project.id'))
