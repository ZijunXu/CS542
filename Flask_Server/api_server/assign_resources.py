from . import api

from .api_resources.UserLogin import UserLogin
from .api_resources.UserRegister import UserRegister
from .api_resources.Admin import Admin
from .api_resources.GetToken import GetToken
from .api_resources.UserSearchHistory import UserSearchHistory
from .api_resources.UserPost import UserPost
from .api_resources.CurrencySearch import CurrencySearch
from .api_resources.mongoQuery import mongoQuery

api.add_resource(UserLogin, "/api/authenticate")
api.add_resource(UserRegister, "/api/reg")
api.add_resource(UserSearchHistory, "/api/user/search")
api.add_resource(UserPost, "/api/user/post")
api.add_resource(Admin, "/api/users/<username>", "/api/users/")
api.add_resource(GetToken, "/api/token")
api.add_resource(CurrencySearch, "/api/currency")
api.add_resource(mongoQuery, "/api/item")
