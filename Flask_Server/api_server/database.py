from api_server import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Role %r>' % self.name

    def as_dict(self):
        return {c.name:getattr(self, c.name) for c in self.__table__.columns}
