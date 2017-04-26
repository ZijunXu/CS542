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
        self.dic = {"blessed": "poe.trade/static/currency/blessed.png",
                    "chisel": "poe.trade/static/currency/chisel.png",
                    "chaos": "poe.trade/static/currency/chaos.png",
                    "chrom": "poe.trade/static/currency/chromatic.png",
                    "divine": "poe.trade/static/currency/divine.png",
                    "exalted": "poe.trade/static/currency/exalted.png",
                    "exa": "poe.trade/static/currency/exalted.png",
                    "exalt": "poe.trade/static/currency/exalted.png",
                    "gcp": "http://poe.trade/static/currency/gcp.png",
                    "jew": "poe.trade/static/currency/jewellers.png",
                    "alch": "poe.trade/static/currency/alchemy.png",
                    "alt": "poe.trade/static/currency/alteration.png",
                    "chance": "poe.trade/static/currency/chance.png",
                    "fuse": "poe.trade/static/currency/fusing.png",
                    "regret": "poe.trade/static/currency/regret.png",
                    "scour": "poe.trade/static/currency/scouring.png",
                    "regal": "poe.trade/static/currency/regal.png",
                    "vaal": "poe.trade/static/currency/vaal.png"}

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
                n["Price"]['icon'] = self.dic[n["Price"]['Currency']]
                ans.append(n)
            if 'Authorization' in request.headers:
                if verify_token(request.headers['Authorization'].split(" ")[1]) and form.name.data:
                    self.add_to_history(form)
            return jsonify(ans)
        else:
            posts = self.db.posts.find().limit(50)
            ans = []
            for n in posts:
                n["_id"] = str(n["_id"])
                n["Price"]['icon'] = self.dic[n["Price"]['Currency']]
                ans.append(n)
            return jsonify(ans)

    def add_to_history(self, form):
        if form.validate():
            search_history = Search(item=form.name.data, time=datetime.datetime.now(), id=g.user.id)
            db.session.add(search_history)
            db.session.commit()
            return True
        return False
