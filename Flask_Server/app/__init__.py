from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import flask_login

app = Flask(__name__)
app.config.from_object(config['dev'])
db = SQLAlchemy(app)
login_manager = flask_login.LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

from app import views

