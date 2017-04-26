from flask import request, jsonify, g
from pymongo import MongoClient, ASCENDING
from flask_restful import Resource
from ..forms import ItemQueryForm
from ..database import Search
from api_server import db
from .mongoSearchFormParser import parser
import datetime
from .GetToken import verify_token


class ItemSearch(Resource):
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017/")
        self.db = client.project_542
        self.dic = {"blessed": "http://poe.trade/static/currency/blessed.png",
                    "chisel": "http://poe.trade/static/currency/chisel.png",
                    "chaos": "http://poe.trade/static/currency/chaos.png",
                    "chrom": "http://poe.trade/static/currency/chromatic.png",
                    "divine": "http://poe.trade/static/currency/divine.png",
                    "exalted": "http://poe.trade/static/currency/exalted.png",
                    "exa": "http://poe.trade/static/currency/exalted.png",
                    "ex": "http://poe.trade/static/currency/exalted.png",
                    "exalt": "http://poe.trade/static/currency/exalted.png",
                    "gcp": "http://poe.trade/static/currency/gcp.png",
                    "jew": "http://poe.trade/static/currency/jewellers.png",
                    "alch": "http://poe.trade/static/currency/alchemy.png",
                    "alt": "http://poe.trade/static/currency/alteration.png",
                    "chance": "http://poe.trade/static/currency/chance.png",
                    "fuse": "http://poe.trade/static/currency/fusing.png",
                    "regret": "http://poe.trade/static/currency/regret.png",
                    "scour": "http://poe.trade/static/currency/scouring.png",
                    "regal": "http://poe.trade/static/currency/regal.png",
                    "vaal": "http://poe.trade/static/currency/vaal.png"}

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
            posts = self.db.posts.find({"$and": query_and}).limit(50).sort("Price.Number", ASCENDING)
            ans = []
            for n in posts:
                n["_id"] = str(n["_id"])
                n["Price"]['icon'] = self.dic[n["Price"]['Currency'].lower()]
                ans.append(n)
            if 'Authorization' in request.headers:
                if verify_token(request.headers['Authorization'].split(" ")[1]) and form.name.data:
                    self.add_to_history(form)
            return jsonify(ans)
        else:
            print(form.errors)
            posts = self.db.posts.find().limit(50)
            ans = []
            for n in posts:
                n["_id"] = str(n["_id"])
                n["Price"]['icon'] = self.dic[n["Price"]['Currency'].lower()]
                ans.append(n)
            return jsonify(ans)

    def add_to_history(self, form):
        if form.validate():
            search_history = Search(item=form.name.data, time=datetime.datetime.now(), id=g.user.id)
            db.session.add(search_history)
            db.session.commit()
            return True
        return False
