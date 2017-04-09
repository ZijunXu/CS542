from flask import jsonify
from flask_restful import Resource
from . import db
from ..database import User, Search
import datetime


class UserSearchHistory(Resource):
    # decorators = [auth.login_required]
    def get(self, userid):
        if userid:
            result = User.query.filter_by(name=userid).first().as_dict()
            return jsonify(result)

    def post(self, data):
        """
        :param data: the data from the user query 
        :return: add new search history to the db
        """
        search_history = Search(item=data.name.data, time=datetime.datetime.now(), id=data.token.data)
        db.session.add(search_history)
        return jsonify({"register_status": True})

    def delete(self, sid):
        search_history = Search.query.filter_by(sid=sid).first()
        db.session.delete(search_history)
        return jsonify({"delete_status": "Success"})
