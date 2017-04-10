from flask import jsonify
from flask_restful import Resource
from ..database import User
from api_server import db


class Admin(Resource):
    """
    this is the functions only for the admin
    """

    # decorators = [auth.login_required]

    def get(self, username=None):
        """
        :param username: if provide username, query that single user
                         if note provide username, query all the users
        :return: 
        """
        if username:
            return jsonify(User.query.filter_by(name=username).first().as_dict())
        else:
            return jsonify([n.as_dict() for n in User.query.all()])

    def delete(self, username):
        """
        :param username: the username that need to be delete
        :return: 
        """
        user = User.query.filter_by(name=username).first()
        db.session.delete(user)
        return jsonify({"delete_status": "Success"})
