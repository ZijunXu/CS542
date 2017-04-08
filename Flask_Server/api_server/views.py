from flask import request, jsonify, g
from flask_restful import Resource
from api_server import app, db, mongo, api
from .database import User, Post
from .forms import LoginForm, RegistrationForm, ItemQueryForm, PostTradeForm
from flask_httpauth import HTTPTokenAuth
import datetime

auth = HTTPTokenAuth(scheme="Token")


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
    the content validation should be done in the both front-end and back-end
    front-end transfer the json to the back-end
    and back-end will do the validation again
    """
    def post(self):
        form = LoginForm.from_json(request.get_json())
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                token = user.generate_auth_token()
                return jsonify({"login_status": True, "token": token.decode("ascii")})
            elif not user:
                return jsonify({"login_status": False, "error": "User not exist"})
            else:
                return jsonify({"login_status": False, "error": "Wrong password"})
        else:
            return jsonify({"login_status": False, "error": "Something wrong with your submit data"})


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
            new_user = User(name=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            return jsonify({"register_status": True})
        return jsonify({"register_status": False, "message": form.errors})


class UserUpdate(Resource):
    """
    this is the API for user to update their information
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
            return jsonify({"register_status": True})
        return jsonify({"register_status": False, "message": form.errors})


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


class GetToken(Resource):
    """
    Usage:
    for browser to request a token
    """
    decorators = [auth.login_required]

    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({"token": token.decode("ascii")})


class ItemSearch(Resource):
    """
    search in the mongodb
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
    """
    # decorators = [auth.login_required]
    def put(self, tradeid):
        """
        this is the function for user to update their trades info
        :param tradeid: the trade post that need to be modified
        :return: 
        """
        form = PostTradeForm.from_json(request.get_json())
        if form.validate_on_submit():
            post = Post(uid=form.username.data, c1item=form.c1_item.data, c2item=form.c2_item.data, c1_number=form.c1_item.data, c2_number=form.c2_item.data, time = datetime.datetime.now())
            db.session.add(post)
            return jsonify({"post_status": True})
        return jsonify({"post_status": False, "message": "Something Wrong on the server side"})

    def post(self):
        """
        this is the function for user to post their trade
        :return: 
        """
        form = PostTradeForm.from_json(request.get_json())
        if form.validate_on_submit():
            post = Post(uid=form.username.data, c1item=form.c1_item.data, c2item=form.c2_item.data, c1_number=form.c1_item.data, c2_number=form.c2_item.data, time = datetime.datetime.now())
            db.session.add(post)
            return jsonify({"post_status": True})
        return jsonify({"post_status": False, "message": "Something Wrong on the server side"})

    def delete(self, tradeid):
        """
        this is the function for user to delete their trade
        :param tradeid: the trade that need to be deleted
        :return: 
        """
        trade = Post.query.filter_by(uid=tradeid).first()
        db.session.delete(trade)
        db.commit()

    def get(self, userid):
        """
        this is the function for getting a user"s posts
        :param userid: 
        :return: 
        """
        if userid:
            return jsonify(Post.query.filter_by(uid=userid).first().as_dict())


class Currency(Resource):
    """
    this is the api for the currency part
    """
    def post(self):
        data = request.get_json()
        pass


api.add_resource(UserLogin, "/api/authenticate")
api.add_resource(UserRegister, "/api/reg")
api.add_resource(Admin, "/api/users/<username>", "/api/users/")
api.add_resource(GetToken, "/api/token")
api.add_resource(ItemSearch, "/api/item")


# Handling the error
@app.errorhandler(404)
def not_found(error=None):
    message = {"status": 404, "message": "Not found" + request.url, }
    res = jsonify(message)
    res.status_code = 404
    return res
