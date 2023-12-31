from archivy import db 

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry = db.Column(db.String(40), nullable=False)
    jurisdiction = db.Column(db.String(40), nullable=False)
    main_project_type = db.Column(db.String(40), nullable=False)
    organization_size = db.Column(db.String(40), nullable=False)
    building_code_1 = db.Column(db.String(40), nullable=False)
    building_code_2 = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

