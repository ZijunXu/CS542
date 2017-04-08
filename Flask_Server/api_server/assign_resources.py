from . import api

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
