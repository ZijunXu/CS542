from flask import request, jsonify
from flask_restful import Resource
from api_server import app, db, mongo, api
from .database import User
from .forms import LoginForm, RegistrationForm, ItemQueryForm
from flask_httpauth import HTTPTokenAuth


auth = HTTPTokenAuth(scheme='Token')

class Login(Resource):
    """
    the content validation should be done in the both ends
    front-end transfer the json to the back-end
    and back-end will do the validation again
    """
    def post(self):
        """
        Usage:
        login_form is what we get to validate in the database
        login_form should has the following value
        username,password,remember_me(default as None)
        """
        form = LoginForm.from_json(request.get_json())
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                token = user.generate_auth_token()
                return jsonify({"login_status": True, 'token': token.decode('ascii')})
        return jsonify({"login_status": False})


class Register(Resource):
    """
    the content validation should be done in the both ends
    front-end transfer the json to the back-end
    and back-end will do the validation again
    """
    def post(self):
        """
        Usage:
        register_form is what we get to insert into the database
        register_form should has the following value
        name, email, password
        """
        form = RegistrationForm.from_json(request.get_json())
        if form.validate_on_submit():
            user = User(name=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            return jsonify({"register_status": True})
        return jsonify({"register_status": False, "message": "Something Wrong on the server side"})


class User_List(Resource):
    decorators = [auth.login_required]

    def get(self, username=None):
        """
        Usage:
        if provide username, query that single user
        if note provide username, query all the users
        """
        if username:
            return jsonify(User.query.filter_by(name=username).first().as_dict())
        else:
            return jsonify([n.as_dict() for n in User.query.all()])

    def delete(self, username):
        """
        Usage:
        delete the user with the same username
        """
        user = User.query.filter_by(name=username).first()
        db.session.delete(user)
        return jsonify({'status': "Delete Success"})

api.add_resource(Login, '/api/authenticate')
api.add_resource(Register, '/api/reg')
api.add_resource(User_List, '/api/users/<username>', '/api/users/')


# Handling the error
@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not found' + request.url, }
    res = jsonify(message)
    res.status_code = 404
    return res
