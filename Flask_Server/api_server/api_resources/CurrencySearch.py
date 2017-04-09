from flask import request, jsonify
from flask_restful import Resource
from ..database import Currency


class CurrencySearch(Resource):
    """
    this is the api for the currency part
    """
    def get(self, name):
        if name == None:
            return jsonify([n.as_dict() for n in Currency.query.all()])
        else:
            ret = Currency.query.filter_by(cnanme=name).first().as_dict()
            return jsonify(ret)
