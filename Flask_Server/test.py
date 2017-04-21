from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config.from_object(config['test'])
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
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
        except SignatureExpired as e:
            return e  # valid token, but expired
        except BadSignature as e:
            return e  # invalid token
        user = User.query.get(data['id'])
        return user


class Admin(db.Model):
    __tablename__ = 'Admin'
    aid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Search(db.Model):
    __tablename__ = 'Search'
    sid = db.Column(db.Integer, primary_key=True)  # Search history ID
    id = db.Column(db.Integer, db.ForeignKey('User.id'))
    item = db.Column(db.String(64))
    time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Search %r>' % self.sid

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Post(db.Model):
    __tablename__ = 'Post'
    tid = db.Column(db.Integer, primary_key=True)  # Post transaction ID
    uid = db.Column(db.Integer, db.ForeignKey('User.id'))  # UserID
    c1_item = db.Column(db.Integer, db.ForeignKey('Currency.cid'))  # The item user wants to sell
    c2_item = db.Column(db.Integer, db.ForeignKey('Currency.cid'))  # The item user wants to get
    c1_number = db.Column(db.Integer)
    c2_number = db.Column(db.Integer)
    league = db.Column(db.String(64))
    name = db.Column(db.String(64))
    time = db.Column(db.DateTime)


    def __repr__(self):
        return '<Post %r>' % self.tid

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Currency(db.Model):
    __tablename__ = 'Currency'
    cid = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(64), unique=True, nullable=True)

    def __repr__(self):
        return '<Currency %r>' % self.cid

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Here you can specify your customize data!

db.drop_all()
db.create_all()
admin1 = User(name='admin1', email='admin1@poe.com', password='a')
admin2 = User(name='admin2', email='admin2@poe.com', password='a')
db.session.add(admin1)
db.session.add(admin2)
db.session.add(User(name='b', email='b@b.com', password='b'))
db.session.add(User(name='bob', email='bob@gmail.com', password='111111'))
db.session.add(User(name='you zhou', email='zhouyou66666@gmail.com', password='111111'))
db.session.add(User(name='shi he', email='she4@wpi.edu', password='111111'))
db.session.add(User(name='zi jun', email='zjxu4@wpi.edu', password='111111'))
db.session.add(User(name='Zz', email='zz5@wpi.edu', password='111111'))
db.session.add(User(name='haha', email='haha@usc.edu', password='111111'))
db.session.commit()

db.session.add(Admin(id=User.query.filter_by(email=admin1.email).first().id))
db.session.add(Admin(id=User.query.filter_by(email=admin2.email).first().id))
db.session.commit()

db.session.add(Search(id=1, item='name: Ancient Waystones Crimson Jewel', time=datetime.datetime.now()))
db.session.add(Search(id=2, item='league: Standard', time=datetime.datetime.now()))
db.session.add(Search(id=3, item='scokets min: 6, rarity: Magic, identified: Yes', time=datetime.datetime.now()))
db.session.add(Search(id=4, item='scokets min: 7, rarity: Normal, identified: Yes', time=datetime.datetime.now()))
db.session.add(Search(id=5, item='quality max: 10, corrupted: No, identified: No', time=datetime.datetime.now()))
db.session.commit()

db.session.add(Post(uid=1, c1_item='Orb', c2_item='LGD', c1_number=1, c2_number=2, league='Standard', time=datetime.datetime.now()))
db.session.add(Post(uid=1, c1_item='Fusing', c2_item='Orb of Alchemy', c1_number=2, c2_number=4, league='Standard', name='abc', time=datetime.datetime.now()))
db.session.add(Post(uid=2, c1_item='Scouring', c2_item='Eber key', c1_number=4, c2_number=8, league='Standard',  name='c', time=datetime.datetime.now()))
db.session.add(Post(uid=2, c1_item='Shaper set', c2_item='Eber key', c1_number=7, c2_number=1, league='Standard',  name='c', time=datetime.datetime.now()))
db.session.add(Post(uid=2, c1_item='Blessing', c2_item='Blessed orb', c1_number=7, c2_number=1, league='Standard',  name='c',time=datetime.datetime.now()))
db.session.commit()

db.session.add(Currency(cname='Orb', cid=1))
db.session.add(Currency(cname='LGD', cid=2))
db.session.add(Currency(cname='Fusing', cid=3))
db.session.add(Currency(cname='Orb of Alchemy', cid=4))
db.session.add(Currency(cname='Eber key', cid=5))
db.session.add(Currency(cname='Scouring', cid=6))
db.session.add(Currency(cname='Shaper set', cid=7))
db.session.add(Currency(cname='Blessing', cid=8))
db.session.add(Currency(cname='Blessed orb', cid=9))
db.session.commit()