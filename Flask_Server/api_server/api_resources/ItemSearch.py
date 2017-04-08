from flask import request
from flask_restful import Resource
from ..forms import ItemQueryForm
from api_server import mongo


class ItemSearch(Resource):
    """
    search in the mongodb
    """
    def post(self):
        form = ItemQueryForm.from_json(request.get_json())
        if form.validate_on_submit():
            results = mongo.db.item.find(form)
            return results
