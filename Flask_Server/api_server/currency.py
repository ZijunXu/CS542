from flask import request, jsonify
from flask_restful import Resource


class Currency(Resource):
    def post(self):
        data = request.get_json()
        pass