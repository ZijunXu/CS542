from flask import request, jsonify
from flask_restful import Resource
from ..forms import PostTradeForm
from ..database import Post
from api_server import db
import datetime


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
            post = Post(uid=form.username.data, c1item=form.c1_item.data, c2item=form.c2_item.data,
                        c1_number=form.c1_item.data, c2_number=form.c2_item.data, time=datetime.datetime.now())
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
            post = Post(uid=form.username.data, c1item=form.c1_item.data, c2item=form.c2_item.data,
                        c1_number=form.c1_item.data, c2_number=form.c2_item.data, time=datetime.datetime.now())
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
