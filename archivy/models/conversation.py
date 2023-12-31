from sqlalchemy import Text
from archivy import db 

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    json = db.Column(Text(length=16777215), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))



