from api_server import db
from .database import User

db.create_all()

db.session.add(User(1,'aaa','aaa@ccc.com','dfsfsdfd','dsd'))
db.session.add(User(1,'sdad','sds@ccc.com','ddsfd','saw'))

db.session.commit()