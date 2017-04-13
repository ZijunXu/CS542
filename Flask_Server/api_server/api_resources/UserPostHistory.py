from flask import request, jsonify
from flask_restful import Resource
from ..forms import PostTradeForm
from ..database import Post
from api_server import db
import sys
import datetime


class UserPostHistory(Resource):
    """
    this is the API for getting user searching history    
    """

    def get(self, tid=None):
        """
        :return: user post history 
        """
        if tid:
            return jsonify({"get_post_status": False, "message": "Wrong usage"})
        form = PostTradeForm.from_json(request.get_json())
        if request.get_json() == None:
            history = Post.query.all()
            return jsonify([n.as_dict() for n in history])
        else:
            if form.validate_on_submit():
                history = Post.query.filter_by(id=form.user_id)
                return jsonify([n.as_dict() for n in history])
            return jsonify({"search_status": False, "message": form.errors})

    def post(self, tid=None):
        """
        :param data: the data from the user query 
        :return: add new search history to the db
        """
        if tid:
            return jsonify({"new_post_status": False, "message": "Wrong usage"})
        form = PostTradeForm.from_json(request.get_json())
        if form.validate_on_submit():
            # form.user_id should be token, then we translate the token into user_id
            search_history = Post(c1_item=form.c1_item.data, c2_item=form.c2_item.data, c1_number=form.c1_number.data,
                                  c2_number=form.c2_number.data, uid=form.user_id.data, time=datetime.datetime.now())
            db.session.add(search_history)
            return jsonify({"record_history_status": True})
        return jsonify({"record_history_status": False, "message": form.errors})

    def delete(self, tid):
        try:
            search_history = Post.query.filter_by(tid=tid).first()
            db.session.delete(search_history)
            return jsonify({"delete_status": "Success"})
        except:
            return jsonify({"delete_history_status": False, "message": sys.exc_info()[0]})
