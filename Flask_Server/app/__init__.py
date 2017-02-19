from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


login_manager = flask_login.LoginManager()

login_manager.init_app(app)

from app import views, models
