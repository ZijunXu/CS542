from flask import request, jsonify
from pymongo import MongoClient
from flask_restful import Resource
from ..forms import ItemQueryForm
from .mongoSearchFormParser import parser


class mongoQuery(Resource):
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
