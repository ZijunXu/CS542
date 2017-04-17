from flask import request, jsonify
from pymongo import MongoClient
from flask_restful import Resource
from ..forms import ItemQueryForm, UserHistoryForm
from .mongoSearchFormParser import parser
import datetime


class ItemSearch(Resource):
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client.project_542

    def post(self):
        """
        how to parse the form is tricky
        :return: mongodb query results
        """
        form = ItemQueryForm.from_json(request.get_json())
        if form.validate_on_submit():
            query_and = parser(form)
            posts = self.db.posts.find({"$and": query_and})
            ans = []
            for n in posts:
                n["_id"] = str(n["_id"])
                ans.append(n)
            return jsonify(ans)
        else:
            posts = self.db.posts.find().limit(20)
            ans = []
            for n in posts:
                n["_id"] = str(n["_id"])
                ans.append(n)
            return jsonify(ans)

    def add_to_history(self):
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
