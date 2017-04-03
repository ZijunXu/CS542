from api_server import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import datetime

class User(db.Model):
    __tablename__='User'

    id = db.Column(db.Integer, primary_key=True)
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



class Currency(db.Model):
    __tablename__ = 'Currency'
    cid = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(64), unique=True, nullable=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'Currency ID': self.cid, 'Currency Name': self.cname}



#test for github


class Currency_Post(db.Model):
    __tablename__='Post'
    tid = db.Column(db.Integer, primary_key=True)  # Post transaction ID
    uid = db.Column(db.Integer, db.ForeignKey('User.id'))  #UserID
    c1_item = db.Column(db.Integer, db.ForeignKey('Currency.cid'))    # The item user wants to sell
    c2_item = db.Column(db.Integer, db.ForeignKey('Currency.cid'))     # The item user wants to get
    c1_number = db.Column(db.Integer)
    c2_number = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def __init__(self, uid, c1_item, c2_item, c1_number, c2_number):
        self.uid = uid
        self.c1_item = c1_item
        self.c2_item = c2_item
        self.c1_number = c1_number
        self.c2_number = c2_number
        self.time = datetime.datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {"tid": self.tid}