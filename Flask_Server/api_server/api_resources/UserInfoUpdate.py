from flask import request, jsonify,g
from flask_restful import Resource
from ..forms import UpdateForm
from ..database import User
from api_server import db
from .GetToken import auth

class UserInfoUpdate(Resource):
    """
    this is the API for user update information
    """
    decorators = [auth.login_required]

    def put(self):
        """
        register_form is what we get to insert into the database
        register_form should has the following value
        name, email, password
        """
        form = UpdateForm.from_json(request.get_json())

        if not g.user:
            return jsonify({"login_staus": False, "message": "Please login"})

        if form.validate_on_submit():
            current_user = User.query.filter_by(id=g.user.id).first()
            if form.email.data:
                current_user.email = form.email.data
            if form.new_password.data:
                current_user.password = form.new_password.data
            db.session.commit()
            return jsonify({"update_status": True})
        return jsonify({"update_status": False, "message": form.errors})
