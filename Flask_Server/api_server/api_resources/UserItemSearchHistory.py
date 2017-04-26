from flask import jsonify, g
from flask_restful import Resource
from api_server import db
from ..database import Search
import sys
from .GetToken import auth


class UserItemSearchHistory(Resource):
    decorators = [auth.login_required]

    # get current users search history
    def get(self, sid=None):
        if sid:
            return jsonify({"retrieve_search_status": False, "message": "Wrong usage"})
        else:

            if not g.user:
                return jsonify({"login_staus": False, "message": "Please login"})

            history = Search.query.filter_by(id=g.user.id)
            return jsonify([n.as_dict() for n in history])

    def delete(self, sid):
        try:
            search_history = Search.query.filter_by(sid=sid).first()
            print(search_history)
            db.session.delete(search_history)
            db.session.commit()
            return jsonify({"delete_history_status": "Success"})
        except:
            print(sys.exc_info())
            return jsonify({"delete_history_status": False, "message": sys.exc_info()[1]})
