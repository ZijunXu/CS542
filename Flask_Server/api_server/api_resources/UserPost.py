from flask import request ,jsonify
from flask_restful import Resource
from ..forms import PostTradeForm
from ..database import Post


class UserPost(Resource):
    """
    this is the API for getting user searching history    
    """
    def get(self):
        """
        :return: user post history 
        """
        form = PostTradeForm.from_json(request.get_json())
        if form.validate_on_submit():
            history = Post.query.filter_by(id=form.user_id)
            return jsonify([n.as_dict() for n in history])
        return jsonify({"search_status": False, "message": form.errors})
