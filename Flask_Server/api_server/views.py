from flask import request, jsonify, g
from flask_restful import Resource
from api_server import app, db, mongo, api
from .database import User, Post
from .forms import LoginForm, RegistrationForm, ItemQueryForm, PostTradeForm
from flask_httpauth import HTTPTokenAuth
import datetime

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    # first try to authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


class UserLogin(Resource):
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
        return login status, if success return the token
        """
        form = LoginForm.from_json(request.get_json())
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                token = user.generate_auth_token()
                return jsonify({"login_status": True, 'token': token.decode('ascii')})
        return jsonify({"login_status": False})


class UserRegister(Resource):
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


class UserQuery(Resource):
    """
    this is the functions for the admin
    """
    # decorators = [auth.login_required]

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


class GetToken(Resource):
    """
    Usage:
    for browser to request a token
    """
    decorators = [auth.login_required]

    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})


class ItemSearch(Resource):
    """
    we need to first determine whether the user is login or not
    if user login we record the search
    else we do not
    """
    def post(self):
        form = ItemQueryForm.from_json(request.get_json())
        if form.validate_on_submit():
            results = mongo.db.item.find(form)
            return results


class UserSearchHistory(Resource):
    # decorators = [auth.login_required]
    def get(self, userid):
        if userid:
            result = User.query.filter_by(name=userid).first().as_dict()
            return jsonify(result)


class UserTrade(Resource):
    """
    This is the api class for the user post, update, delete and get trade information
    TBD
    """
    # decorators = [auth.login_required]
    def put(self, tradeid):
        form = PostTradeForm.from_json(request.get_json())
        if form.validate_on_submit():
            post = Post(uid=form.username.data, c1item=form.c1_item.data, c2item=form.c2_item.data, c1_number=form.c1_item.data, c2_number=form.c2_item.data, time = datetime.datetime.now())
            db.session.add(post)
            return jsonify({"post_status": True})
        return jsonify({"post_status": False, "message": "Something Wrong on the server side"})

    def post(self):
        form = PostTradeForm.from_json(request.get_json())
        if form.validate_on_submit():
            post = Post(uid=form.username.data, c1item=form.c1_item.data, c2item=form.c2_item.data, c1_number=form.c1_item.data, c2_number=form.c2_item.data, time = datetime.datetime.now())
            db.session.add(post)
            return jsonify({"post_status": True})
        return jsonify({"post_status": False, "message": "Something Wrong on the server side"})

    def delete(self, tradeid):
        trade = Post.query.filter_by(uid=tradeid).first()
        db.session.delete(trade)
        db.commit()

    def get(self, userid):
        if userid:
            return jsonify(Post.query.filter_by(uid=userid).first().as_dict())


class Currency(Resource):
    def post(self):
        data = request.get_json()
        pass


api.add_resource(UserLogin, '/api/authenticate')
api.add_resource(UserRegister, '/api/reg')
api.add_resource(UserQuery, '/api/users/<username>', '/api/users/')
api.add_resource(GetToken, '/api/token')
api.add_resource(ItemSearch, '/api/item')


# Handling the error
@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not found' + request.url, }
    res = jsonify(message)
    res.status_code = 404
    return res
