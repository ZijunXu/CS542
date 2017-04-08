from flask import request, jsonify
from api_server import app, db, mongo, api

from .api_resources.UserLogin import UserLogin
from .api_resources.UserRegister import UserRegister
from .api_resources.Admin import Admin
from .api_resources.GetToken import GetToken
from .api_resources.ItemSearch import ItemSearch


api.add_resource(UserLogin, "/api/authenticate")
api.add_resource(UserRegister, "/api/reg")
api.add_resource(Admin, "/api/users/<username>", "/api/users/")
api.add_resource(GetToken, "/api/token")
api.add_resource(ItemSearch, "/api/item")


# Handling the error
@app.errorhandler(404)
def not_found(error=None):
    message = {"status": 404, "message": "Not found" + request.url, }
    res = jsonify(message)
    res.status_code = 404
    return res
