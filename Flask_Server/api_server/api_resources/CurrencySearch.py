from flask import request, jsonify
from flask_restful import Resource
from ..database import Post
from ..database import Currency
from ..forms import CurrencySearchForm


class CurrencySearch(Resource):
    """
    this is the api for the currency part
    """

    def get(self, currency_name=None):
        if not currency_name:
            return jsonify([n.as_dict() for n in Currency.query.all()])
        else:
            ret = Currency.query.filter_by(cnanme=currency_name).first().as_dict()
            return jsonify(ret)

    def post(self):
        form = CurrencySearchForm.from_json(request.get_json())
        if form.validate_on_submit():
            search_currency_post = Post.query.filter_by(c1_item=form.currency_name.data)
            return jsonify([n.as_dict() for n in search_currency_post])
        return jsonify({"post_search_status": False, "message": form.errors})