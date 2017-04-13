from flask import request, jsonify
from flask_restful import Resource
from api_server import db
from ..forms import UserHistoryForm
from ..database import Search
import datetime
import sys


class UserSearchHistory(Resource):
    # decorators = [auth.login_required]
    def get(self, sid=None):
        if sid:
            return jsonify({"retrive_search_status": False, "message": "Wrong usage"})
        form = UserHistoryForm.from_json(request.get_json())
        if request.get_json() == None:
            history = Search.query.all()
            return jsonify([n.as_dict() for n in history])
        else:
            if form.validate_on_submit():
                history = Search.query.filter_by(id=form.user_id, item=form.item_name)
                return jsonify([n.as_dict() for n in history])
            return jsonify({"retrive_search_status": False, "message": form.errors})

    def post(self, sid=None):
        """
        :param data: the data from the user query 
        :return: add new search history to the db
        """
        if sid:
            return jsonify({"new_search_status": False, "message": "Wrong usage"})
        form = UserHistoryForm.from_json(request.get_json())
        if form.validate_on_submit():
            # form.user_id should be token, then we translate the token into user_id
            search_history = Search(item=form.item_name.data, time=datetime.datetime.now(), id=form.user_id.data)
            db.session.add(search_history)
            return jsonify({"record_history_status": True})
        return jsonify({"record_history_status": False, "message": form.errors})

    def delete(self, sid):
        try:
            search_history = Search.query.filter_by(sid=sid).first()
            db.session.delete(search_history)
            return jsonify({"delete_history_status": "Success"})
        except:
            return jsonify({"delete_history_status": False, "message": sys.exc_info()[0]})
