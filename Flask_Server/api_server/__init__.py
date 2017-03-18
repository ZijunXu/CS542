from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_restful import Api
from config import config
import flask_login
import wtforms_json

app = Flask(__name__)
app.config.from_object(config['dev'])
db = SQLAlchemy(app)
mongo = PyMongo(app)


login_manager = flask_login.LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

api = Api(app)
wtforms_json.init()

app.add_url_rule('/','index',lambda:app.send_static_file('index.html'))
from api_server import views
