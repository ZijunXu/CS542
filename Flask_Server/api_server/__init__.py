from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_restful import Api
from config import config
import wtforms_json

db = SQLAlchemy()
mongo = PyMongo()
api = Api()
main = Blueprint('main',__name__)


def CreateApp(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    mongo.init_app(app)
    wtforms_json.init()
    app.register_blueprint(main)
    app.add_url_rule('/', 'index', lambda: app.send_static_file('index.html'))
    from api_server import assign_resources
    api.init_app(app)
    return app
