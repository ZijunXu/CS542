from flask import request, jsonify
from flask_restful import Resource
from ..forms import RegistrationForm
from ..database import User
from api_server import db


class UserInfoUpdate(Resource):
    """
    this is the API for user update information
    """
    # decorators = [auth.login_required]
    def put(self):
        """
        register_form is what we get to insert into the database
        register_form should has the following value
        name, email, password
        """
        form = RegistrationForm.from_json(request.get_json())
        if form.validate_on_submit():
            new_user = User(name=form.username.data, email=form.email.data, password=form.password.data)
            db.session.update(new_user)
            return jsonify({"update_status": True})
        return jsonify({"update_status": False, "message": form.errors})
