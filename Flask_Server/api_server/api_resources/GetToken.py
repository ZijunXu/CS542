from flask import request, jsonify
from flask_restful import Resource
from flask_httpauth import HTTPTokenAuth
auth = HTTPTokenAuth(scheme="Token")


@auth.verify_token
def verify_token(token):
    # first try to authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


class GetToken(Resource):
    """
    Usage:
    for browser to request a token
    """
    decorators = [auth.login_required]

    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({"token": token.decode("ascii")})
