from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_bcrypt import Bcrypt
config_instance=Config

app = Flask(__name__)

with app.app_context():
    app.config.from_object(config_instance)

    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)    

import archivy.routes