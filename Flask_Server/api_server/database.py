from api_server import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    __tablename__='User'
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
        return '<User %r>' % self.id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Admin(User):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)


class Search(db.Model):
    __tablename__='Search'
    sid = db.Column(db.Integer, primary_key=True)  #Search history ID
    id = db.Column(db.Integer, db.ForeignKey('User.id'))
    item = db.Column(db.String(64))
    time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Search %r>' % self.sid

class Post(db.Model):
    __tablename__='Post'
    tid = db.Column(db.Integer, primary_key=True)  # Post transaction ID
    uid = db.Column(db.Integer, db.ForeignKey('User.id'))  #UserID
    c1_item = db.Column(db.Integer, db.ForeignKey('Currency.cid'))    # The item user wants to sell
    c2_item = db.Column(db.Integer, db.ForeignKey('Currency.cid'))     # The item user wants to get
    c1_number = db.Column(db.Integer)
    c2_number = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Post %r>' % self.tid

class Currency(db.Model):
    __tablename__ = 'Currency'
    cid = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(64), unique=True, nullable=True)

    def __repr__(self):
        return '<Currency %r>' % self.cid



#test for github