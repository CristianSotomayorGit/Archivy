from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bcrypt import Bcrypt
config_instance=Config

app = Flask(__name__)

with app.app_context():
    app.config.from_object(config_instance)

    print(config_instance.SQLALCHEMY_DATABASE_URI)
    print(config_instance.SECRET_KEY)
    print(config_instance.OPEN_AI_SECRET_KEY)


    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)    

import archivy.routes