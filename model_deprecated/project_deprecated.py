from archivy import db 

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.column(db.string(500), nullable=False)