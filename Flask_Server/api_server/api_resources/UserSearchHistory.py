from flask import request, jsonify
from flask_restful import Resource
from api_server import db
from ..forms import UserHistoryForm
from ..database import Search
import datetime


class UserSearchHistory(Resource):
    # decorators = [auth.login_required]
    def get(self):
        form = UserHistoryForm.from_json(request.get_json())
        if request.get_json() == None:
            history = Search.query.all()
            return jsonify([n.as_dict() for n in history])
        else:
            if form.validate_on_submit():
                history = Search.query.filter_by(id=form.user_id, item=form.item_name)
                return jsonify([n.as_dict() for n in history])
            return jsonify({"search_status": False, "message": form.errors})

    def post(self, data):
        """
        :param data: the data from the user query 
        :return: add new search history to the db
        """
        search_history = Search(item=data.name.data, time=datetime.datetime.now(), id=data.token.data)
        db.session.add(search_history)
        return jsonify({"register_status": True})

    def delete(self, sid):
        search_history = Search.query.filter_by(sid=sid).first()
        db.session.delete(search_history)
        return jsonify({"delete_status": "Success"})
