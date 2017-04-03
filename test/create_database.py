from app import db
from models import User

db.create_all()

db.session.add(User('dick','aaa@ccc.com'))
db.session.add(User('dick2','aaa@ccc2.com'))

db.session.commit()