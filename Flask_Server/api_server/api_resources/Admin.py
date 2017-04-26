from flask import jsonify, request, g
from flask_restful import Resource
from ..database import User, Post, Search
from ..database import Admin as Admindb
from ..forms import RegistrationForm
from api_server import db
import sys
from .GetToken import auth


class Admin(Resource):
    """
    this is the functions only for the admin
    """

    decorators = [auth.login_required]

    def __init__(self):
        self.admin = Admindb.query.filter_by(id=g.user.id).first()

    def not_permitted(self):
        return jsonify({"message": "Wrong Page"})

    def get(self, username=None):
        """
        :param username: if provide username, query that single user
                         if note provide username, query all the users
        :return: 
        """
        if not self.admin:
            return self.not_permitted()
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
        if not self.admin:
            return self.not_permitted()
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
        if not self.admin:
            return self.not_permitted()
        user = User.query.filter_by(name=username).first()
        if user:
            try:
                self.delete_other_user_related_info(user.id)
                db.session.delete(user)
                db.session.commit()
                return jsonify({"delete_status": "Success"})
            except:
                return jsonify({"delete_status": "Fail"})
        else:
            return jsonify({"delete_status": "Fail", "message": "User not exist"})

    def delete_other_user_related_info(self, userid):
        if not self.admin:
            return self.not_permitted()
        Post.query.filter_by(uid=userid).delete()
        Search.query.filter_by(id=userid).delete()
        db.session.commit()
