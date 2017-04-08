from flask import request, jsonify
from flask_restful import Resource
from ..forms import RegistrationForm
from ..database import User
from api_server import db



class Currency(Resource):
    """
    this is the api for the currency part
    """
    def post(self):
        data = request.get_json()
        pass
