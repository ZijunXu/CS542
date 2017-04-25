from flask import request, jsonify
from flask_restful import Resource
from ..database import Post
from ..database import Currency
from ..forms import CurrencySearchForm


class UserCurrencyPostSearch(Resource):
    """
    this is the api for the currency part
    """

    def get(self, currency_name=None):
        if not currency_name:
            return jsonify([n.as_dict() for n in Currency.query.all()])

    def post(self):
        form = CurrencySearchForm.from_json(request.get_json())
        if form.validate_on_submit():
            search_currency_post = Post.query.filter_by(c1_item=form.c1_item.data, c2_item=form.c2_item.data,
                                                        league=form.league.data)
            search_currency_post = search_currency_post.order_by(Post.time)
            return jsonify([n.as_dict() for n in search_currency_post])
        return jsonify({"post_search_status": False, "message": form.errors})
