from flask import jsonify, request
from flask_restful import Resource
from ..database import User
from ..forms import RegistrationForm
from api_server import db
import sys
from .GetToken import auth


class Admin(Resource):
    """
    this is the functions only for the admin
    """

    decorators = [auth.login_required]

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

    def post(self, username=None):
        """
        register_form is what we get to insert into the database
        register_form should has the following value
        name, email, password
        """
        form = RegistrationForm.from_json(request.get_json())
        if form.validate_on_submit():
            new_user = User(name=form.name.data, email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            return jsonify({"register_status": True})
        error_message = [form.errors[n] for n in form.errors][0]
        return jsonify({"register_status": False, "message": error_message})


    def delete(self, username):
        """
        :param username: the username that need to be delete
        :return: 
        """
        user = User.query.filter_by(name=username).first()
        if user:
            try:
                db.session.delete(user)
                return jsonify({"delete_status": "Success"})
            except:
                return jsonify({"delete_status": "Success", "message": sys.exc_info()[0]})
        else:
            return jsonify({"delete_status": "Success", "message": "User not exist"})
