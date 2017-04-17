from . import api

from .api_resources.UserLogin import UserLogin
from .api_resources.UserRegister import UserRegister
from .api_resources.Admin import Admin
from .api_resources.GetToken import GetToken
from .api_resources.UserItemSearchHistory import UserItemSearchHistory
from .api_resources.UserCurrencyPostManagement import UserCurrencyPostManagement
from .api_resources.UserCurrencyPostSearch import UserCurrencyPostSearch
from .api_resources.ItemSearch import ItemSearch
from .api_resources.UserInfoUpdate import UserInfoUpdate

api.add_resource(UserLogin, "/api/authenticate")
api.add_resource(UserRegister, "/api/reg")
api.add_resource(UserItemSearchHistory, "/api/user/search", "/api/user/search/<sid>")
api.add_resource(UserCurrencyPostManagement, "/api/user/post", "/api/user/post/<tid>")
api.add_resource(UserInfoUpdate, "/api/user/update")
api.add_resource(Admin, "/api/admin/<username>", "/api/admin")
api.add_resource(GetToken, "/api/token")
api.add_resource(UserCurrencyPostSearch, "/api/currency/<currency_name>", "/api/currency")
api.add_resource(ItemSearch, "/api/item")
