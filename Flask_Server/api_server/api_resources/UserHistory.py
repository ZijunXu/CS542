from flask import request, jsonify
from flask_restful import Resource
from ..forms import UserHistoryForm
from ..database import Search


class UserHistory(Resource):
    """
    this is the API for getting user searching history    
    """
    def get(self):
        """
        :return: user search history 
        """
        form = UserHistoryForm.from_json(request.get_json())
        if form.validate_on_submit():
            history = Search.query.filter_by(id=form.user_id, item=form.item_name)
            return jsonify([n.as_dict() for n in history])
        return jsonify({"search_status": False, "message": form.errors})