from flask import request, jsonify, g
from pymongo import MongoClient
from flask_restful import Resource
from ..forms import ItemQueryForm
from ..database import Search
from api_server import db
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
        print(request.get_json())
        form = ItemQueryForm.from_json(request.get_json())
        if form.validate_on_submit():
            query_and = parser(form)
            print(query_and)
            posts = self.db.posts.find({"$and": query_and}).limit(50)
            ans = []
            for n in posts:
                n["_id"] = str(n["_id"])
                ans.append(n)
            try:
                if g.user and form.name.data:
                    self.add_to_history(form)
                return jsonify(ans)
            except:
                return jsonify(ans)

        else:
            posts = self.db.posts.find().limit(50)
            ans = []
            for n in posts:
                n["_id"] = str(n["_id"])
                ans.append(n)
            return jsonify(ans)

    def add_to_history(self, form):
            if form.validate():
                search_history = Search(item=form.item_name.data, time=datetime.datetime.now(), id=g.user.id)
                db.session.add(search_history)
                db.session.commit()
                return True
            return False
