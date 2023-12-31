from sqlalchemy import Text
from archivy import db 

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(500), nullable=False)
    conversations = db.relationship('Conversation', backref='project', lazy=True)

