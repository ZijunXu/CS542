from flask import request, jsonify, g
from flask_restful import Resource
from ..forms import PostTradeForm
from ..database import Post
from api_server import db
import datetime
from .GetToken import auth
import sys


class UserCurrencyPostManagement(Resource):
    """
    This is the api class for the user post, update, delete and get trade information
    """
    decorators = [auth.login_required]

    def put(self, tid):
        """
        this is the function for user to update their trades info
        :param tid: the post that need to be modified
        :return: 
        """
        form = PostTradeForm.from_json(request.get_json())
        if form.validate_on_submit():
            old_post = Post.query.filter_by(tid=tid).first()
            if old_post and old_post.uid == g.user.id:
                old_post.c1_item = form.c1_item.data
                old_post.c2_item = form.c2_item.data
                old_post.c1_number = form.c1_number.data
                old_post.c2_number = form.c2_number.data
                old_post.time = datetime.datetime.now()
                db.session.commit()
                return jsonify({"post_update_status": True})
            else:
                return jsonify({"post_update_status": False, "Message": "Trade Not Exists"})
        return jsonify({"post_update_status": False, "message": form.errors})

    def post(self, tid=None):
        """
        this is the function for user to post their trade
        :return: 
        """
        if tid:
            return jsonify({"new_post_status": False, "message": "Wrong usage"})

        if not g.user:
            return jsonify({"login_staus": False, "message": "Please login"})

        form = PostTradeForm.from_json(request.get_json())
        if form.validate_on_submit():
            post = Post(uid=g.user.id, c1_item=form.c1_item.data, c2_item=form.c2_item.data,
                        c1_number=form.c1_number.data, c2_number=form.c2_number.data, league=form.league.data, name=form.user_name.data, time=datetime.datetime.now())
            db.session.add(post)
            db.session.commit()
            return jsonify({"post_status": True})
        return jsonify({"post_status": False, "message": form.errors})

    def delete(self, tid):
        """
        this is the function for user to delete their trade
        :param tradeid: the trade that need to be deleted
        :return: 
        """
        try:
            trade = Post.query.filter_by(tid=tid).first()
            if trade and trade.uid == g.user.id:
                db.session.delete(trade)
                db.session.commit()
            return jsonify({"delete_post_status": "Success"})
        except:
            return jsonify({"delete_post_status": False, "message": sys.exc_info()[0]})


    def get(self, tid=None):
        """
        this is the function for getting a user"s posts
        :param userid: 
        :return: 
        """
        if tid:
            return jsonify({"retrieve_post_status": False, "message": "Wrong usage"})
        else:
            if not g.user:
                return jsonify({"login_staus": False, "message": "Please login"})

            history = Post.query.filter_by(uid=g.user.id).order_by(Post.time.desc())
            for n in history:
                print(n.time)
            return jsonify([n.as_dict() for n in history])
