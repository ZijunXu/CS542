from flask import request, jsonify
from flask_restful import Resource
from ..forms import RegistrationForm
from ..database import User
from api_server import db

class UserRegister(Resource):
    """
    the content validation should be done in the both ends
    front-end transfer the json to the back-end
    and back-end will do the validation again
    """
    def post(self):
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
