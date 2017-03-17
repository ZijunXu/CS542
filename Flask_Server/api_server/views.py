from flask import render_template, flash, redirect, request, url_for, jsonify
from flask_login import login_user
from flask_restful import Resource
from api_server import app, db, mongo, api
from .database import User
from .forms import LoginForm, RegistrationForm, ItemQueryForm

todos = {"123":123}

class Login(Resource):
    """the content validation should be done in the front-end"""
    def __init__(self):


    def get(self, login_form):
        """Usage:
        login_form is what we get to validate in the database
        login_form should has the following value
        name,password
        """
        user = User.query.filter_by(name=login_form['name']).first()
        if user is not None and user.verify_password(login_form['password']):
            login_user(user, login_form['remember_me'])
            flash('Thanks for login')
            return jsonify({"login_status":True})
        return jsonify({"login_status": False})


class Register(Resource):
    """the content validation should be done in the front-end"""
    def get(self,register_form):
        """Usage:
        register_form is what we get to insert into the database
        register_form should has the following value
        name,email,password
        """
        user = User(name=register_form['name'], email=register_form['email'],
                    password=register_form['password'])
        db.session.add(user)
        return jsonify({"register_status": True})



api.add_resource(Login, '/login')
api.add_resource(Register, '/reg')

@app.errorhandler(404)
def not_found(error=None):
    message = {'status':404,'message':'Not found' + request.url,}
    res = jsonify(message)
    res.status_code = 404
    return res

