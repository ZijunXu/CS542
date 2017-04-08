from flask import jsonify
from flask_restful import Resource
from ..database import User


class UserSearchHistory(Resource):
    # decorators = [auth.login_required]
    def get(self, userid):
        if userid:
            result = User.query.filter_by(name=userid).first().as_dict()
            return jsonify(result)
