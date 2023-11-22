from sqlalchemy import Text
from archivy import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname=db.Column(db.String(40),nullable=False)
    lastname=db.Column(db.String(40),nullable=False)
    email=db.Column(db.String(40),nullable=False,unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    hasAnswered = db.Column(db.Integer, nullable=False)
    user_info = db.relationship('UserInfo', backref='user',lazy=True )
    projects = db.relationship('Project', backref='user', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(500), nullable=False)
    conversations = db.relationship('Conversation', backref='project', lazy=True)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    json = db.Column(Text(length=16777215), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry = db.Column(db.String(40), nullable=False)
    jurisdiction = db.Column(db.String(40), nullable=False)
    main_project_type = db.Column(db.String(40), nullable=False)
    organization_size = db.Column(db.String(40), nullable=False)
    building_code_1 = db.Column(db.String(40), nullable=False)
    building_code_2 = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

