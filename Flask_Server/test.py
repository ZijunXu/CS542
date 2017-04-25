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
admin3 = User(name='admin3', email='admin3@poe.com', password='a')
db.session.add(admin1)
db.session.add(admin2)
db.session.add(admin3)
db.session.add(User(name='b', email='b@b.com', password='b'))
db.session.add(User(name='bob', email='bob@gmail.com', password='111111'))
db.session.add(User(name='you zhou', email='zhouyou66666@gmail.com', password='111111'))
db.session.add(User(name='shi he', email='she4@wpi.edu', password='111111'))
db.session.add(User(name='zi jun', email='zjxu4@wpi.edu', password='111111'))
db.session.add(User(name='Zz', email='zz5@wpi.edu', password='111111'))
db.session.add(User(name='haha', email='haha@usc.edu', password='111111'))
db.session.add(User(name='Alex', email='alex3@usc.edu', password='111111'))
db.session.add(User(name='Hyper', email='Hyper@usc.edu', password='111111'))
db.session.add(User(name='Prometheus', email='Prometheus@usc.edu', password='111111'))
db.session.add(User(name='Sexual Chocolate', email='Sexual Chocolate@usc.edu', password='111111'))
db.session.add(User(name='Freak', email='Freak@usc.edu', password='111111'))
db.session.add(User(name='bar', email='bar@163.com', password='bar'))
db.session.add(User(name='book', email='book@gmail.com', password='111111'))
db.session.add(User(name='wang zhou', email='zhouyou666@gmail.com', password='111111'))
db.session.add(User(name='hem', email='dddd@wpi.edu', password='111111'))
db.session.add(User(name='ziking', email='zj@wpi.edu', password='111111'))
db.session.add(User(name='Zoom', email='zom@wpi.edu', password='111111'))
db.session.add(User(name='h1b', email='h1b@usc.edu', password='111111'))
db.session.add(User(name='Alex Wang', email='alexw@usc.edu', password='111111'))
db.session.add(User(name='Herb', email='Herb1995@usc.edu', password='111111'))
db.session.add(User(name='alibaba', email='alibaba@usc.edu', password='111111'))
db.session.add(User(name='Chocolate', email='Chocolate@usc.edu', password='111111'))
db.session.add(User(name='Funky', email='poppin@163.com', password='111111'))

db.session.commit()

db.session.add(Admin(id=User.query.filter_by(email=admin1.email).first().id))
db.session.add(Admin(id=User.query.filter_by(email=admin2.email).first().id))
db.session.add(Admin(id=User.query.filter_by(email=admin3.email).first().id))
db.session.commit()

db.session.add(Search(id=1, item='Ancient Waystones Crimson Jewel', time=datetime.datetime.now()))
db.session.add(Search(id=2, item='Abyssal Axe', time=datetime.datetime.now()))
db.session.add(Search(id=3, item='Battle Hammer', time=datetime.datetime(2016, 1, 7, 9, 51, 54)))
db.session.add(Search(id=3, item='A Firm Foothold', time=datetime.datetime(2017, 1, 1, 3, 25, 40)))
db.session.add(Search(id=4, item='Dagger Axe', time=datetime.datetime(2016, 1, 4, 14, 18, 50)))
db.session.add(Search(id=5, item='Fragment of the Hydra', time=datetime.datetime(2016, 7, 26, 15, 38, 5)))
db.session.add(Search(id=1, item='Ancient Waystones Crimson Jewel', time=datetime.datetime(2017, 2, 4, 4, 30, 04)))
db.session.add(Search(id=2, item='Abyssal Axe', time=datetime.datetime.now(2017, 2, 4, 4, 36, 44)))
db.session.add(Search(id=3, item='Battle Hammer', time=datetime.datetime(2016, 1, 5, 12, 05, 33)))
db.session.add(Search(id=3, item='A Firm Foothold', time=datetime.datetime(2017, 1, 11, 3, 01, 40)))
db.session.add(Search(id=4, item='Dagger Axe', time=datetime.datetime(2016, 4, 8, 19, 20, 59)))
db.session.add(Search(id=5, item='Fragment of the Hydra', time=datetime.datetime(2016, 7, 17, 15, 11, 03)))

db.session.commit()

db.session.add(
    Post(uid=0, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=313, c2_number=181, league="Legacy",
         name="101",
         time=datetime.datetime(2016, 6, 1, 16, 24, 40)))
db.session.add(
    Post(uid=1, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=209, c2_number=52, league="Legacy",
         name="Houston", time=datetime.datetime(2016, 5, 2, 20, 14, 31)))
db.session.add(Post(uid=2, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=151, c2_number=279, league="Legacy",
                    name="Pinball Wizard", time=datetime.datetime(2016, 1, 10, 9, 44, 55)))
db.session.add(
    Post(uid=3, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=310, c2_number=249, league="Legacy",
         name="Accidental Genius", time=datetime.datetime(2016, 10, 2, 9, 48, 9)))
db.session.add(Post(uid=4, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=267, c2_number=282, league="Legacy",
                    name="Hyper", time=datetime.datetime(2016, 12, 22, 9, 3, 27)))
db.session.add(Post(uid=5, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=209, c2_number=141, league="Legacy",
                    name="Pluto", time=datetime.datetime(2016, 2, 23, 16, 52, 2)))
db.session.add(
    Post(uid=6, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=147, c2_number=180, league="Legacy",
         name="Alpha", time=datetime.datetime(2016, 10, 16, 4, 50, 57)))
db.session.add(
    Post(uid=7, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=113, c2_number=236, league="Legacy",
         name="Jester", time=datetime.datetime(2016, 6, 5, 11, 48, 5)))
db.session.add(Post(uid=8, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=74, c2_number=85, league="Legacy",
                    name="Pogue", time=datetime.datetime(2016, 5, 8, 20, 0, 50)))
db.session.add(
    Post(uid=9, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=150, c2_number=190, league="Legacy",
         name="Airport Hobo", time=datetime.datetime(2016, 12, 4, 21, 17, 42)))
db.session.add(
    Post(uid=10, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=195, c2_number=271, league="Legacy",
         name="Jigsaw", time=datetime.datetime(2016, 4, 4, 17, 40, 58)))
db.session.add(
    Post(uid=11, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=43, c2_number=295, league="Legacy",
         name="Prometheus", time=datetime.datetime(2016, 4, 24, 22, 49, 6)))
db.session.add(
    Post(uid=12, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=257, c2_number=220, league="Legacy",
         name="Bearded Angler", time=datetime.datetime(2016, 4, 19, 19, 0, 46)))
db.session.add(
    Post(uid=13, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=89, c2_number=274, league="Legacy",
         name="Joker's Grin", time=datetime.datetime(2016, 9, 14, 22, 44, 10)))
db.session.add(Post(uid=14, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=173, c2_number=290, league="Legacy",
                    name="Psycho Thinker", time=datetime.datetime(2016, 11, 25, 8, 38, 14)))
db.session.add(Post(uid=15, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=180, c2_number=207, league="Legacy",
                    name="Beetle King", time=datetime.datetime(2016, 9, 19, 5, 57, 0)))
db.session.add(
    Post(uid=16, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=152, c2_number=56, league="Legacy",
         name="Judge", time=datetime.datetime(2016, 5, 14, 9, 44, 0)))
db.session.add(Post(uid=17, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=204, c2_number=150, league="Legacy",
                    name="Pusher", time=datetime.datetime(2016, 9, 3, 18, 5, 40)))
db.session.add(
    Post(uid=18, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=219, c2_number=183, league="Legacy",
         name="Bitmap", time=datetime.datetime(2016, 5, 17, 19, 39, 2)))
db.session.add(
    Post(uid=19, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=21, c2_number=247,
         league="Legacy", name="Junkyard Dog", time=datetime.datetime(2016, 11, 7, 6, 21, 38)))
db.session.add(
    Post(uid=20, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=306, c2_number=152, league="Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 2, 7, 14, 2, 28)))
db.session.add(
    Post(uid=21, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=85, c2_number=119, league="Legacy",
         name="Blister", time=datetime.datetime(2016, 11, 28, 19, 51, 30)))
db.session.add(
    Post(uid=22, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=304, c2_number=221, league="Legacy",
         name="K-9", time=datetime.datetime(2016, 6, 3, 21, 43, 26)))
db.session.add(
    Post(uid=23, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=39, c2_number=26, league="Legacy",
         name="Roadblock", time=datetime.datetime(2016, 2, 10, 11, 9, 48)))
db.session.add(Post(uid=24, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=187, c2_number=120,
                    league="Legacy", name="Bowie", time=datetime.datetime(2016, 4, 21, 0, 42, 35)))
db.session.add(Post(uid=25, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=313, c2_number=50,
                    league="Legacy", name="Keystone", time=datetime.datetime(2016, 6, 23, 12, 39, 22)))
db.session.add(Post(uid=26, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=68, c2_number=231,
                    league="Legacy", name="Rooster", time=datetime.datetime(2016, 10, 11, 22, 6, 47)))
db.session.add(Post(uid=27, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=52, c2_number=200,
                    league="Legacy", name="Bowler", time=datetime.datetime(2016, 6, 19, 12, 32, 27)))
db.session.add(Post(uid=28, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=251, c2_number=183,
                    league="Legacy", name="Kickstart", time=datetime.datetime(2016, 6, 2, 19, 41, 13)))
db.session.add(
    Post(uid=29, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=94, c2_number=210, league="Legacy",
         name="Sandbox", time=datetime.datetime(2016, 7, 13, 22, 29, 51)))
db.session.add(
    Post(uid=30, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=113, c2_number=65, league="Legacy",
         name="Breadmaker", time=datetime.datetime(2016, 7, 27, 1, 50, 7)))
db.session.add(Post(uid=31, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=277, c2_number=108,
                    league="Legacy", name="Kill Switch", time=datetime.datetime(2016, 1, 23, 17, 13, 46)))
db.session.add(
    Post(uid=32, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=136, c2_number=133, league="Legacy",
         name="Scrapper", time=datetime.datetime(2016, 10, 17, 10, 52, 47)))
db.session.add(
    Post(uid=33, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=214, c2_number=205, league="Legacy",
         name="Broomspun", time=datetime.datetime(2016, 12, 3, 16, 9, 52)))
db.session.add(Post(uid=34, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=288, c2_number=266,
                    league="Legacy", name="Kingfisher", time=datetime.datetime(2016, 7, 26, 17, 11, 45)))
db.session.add(
    Post(uid=35, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=101, c2_number=308, league="Legacy",
         name="Screwtape", time=datetime.datetime(2016, 6, 2, 0, 25, 55)))
db.session.add(Post(uid=36, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=46, c2_number=44, league="Legacy",
                    name="Buckshot", time=datetime.datetime(2016, 2, 11, 1, 57, 8)))
db.session.add(
    Post(uid=37, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=297, c2_number=97, league="Legacy",
         name="Kitchen", time=datetime.datetime(2016, 1, 5, 6, 25, 5)))
db.session.add(Post(uid=38, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=306, c2_number=309, league="Legacy",
                    name="Sexual Chocolate", time=datetime.datetime(2016, 11, 4, 3, 11, 30)))
db.session.add(Post(uid=39, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=74, c2_number=29, league="Legacy",
                    name="Bugger", time=datetime.datetime(2016, 11, 12, 12, 8, 42)))
db.session.add(Post(uid=40, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=24, c2_number=22, league="Legacy",
                    name="Knuckles", time=datetime.datetime(2016, 5, 23, 15, 20, 29)))
db.session.add(Post(uid=41, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=228, c2_number=285, league="Legacy",
                    name="Shadow Chaser", time=datetime.datetime(2016, 8, 2, 5, 35, 45)))
db.session.add(
    Post(uid=42, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=121, c2_number=276, league="Legacy",
         name="Cabbie", time=datetime.datetime(2016, 11, 28, 7, 58, 17)))
db.session.add(
    Post(uid=43, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=260, c2_number=147, league="Legacy",
         name="Lady Killer", time=datetime.datetime(2016, 8, 9, 5, 9, 52)))
db.session.add(Post(uid=44, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=44, c2_number=285, league="Legacy",
                    name="Sherwood Gladiator", time=datetime.datetime(2016, 6, 6, 21, 14, 51)))
db.session.add(
    Post(uid=45, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=97, c2_number=146, league="Legacy",
         name="Candy Butcher", time=datetime.datetime(2016, 9, 4, 21, 43, 45)))
db.session.add(Post(uid=46, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=202, c2_number=84, league="Legacy",
                    name="Liquid Science", time=datetime.datetime(2016, 10, 15, 21, 19, 14)))
db.session.add(Post(uid=47, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=43, c2_number=152, league="Legacy",
                    name="Shooter", time=datetime.datetime(2016, 7, 7, 4, 10, 12)))
db.session.add(Post(uid=48, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=43, c2_number=275, league="Legacy",
                    name="Capital F", time=datetime.datetime(2016, 2, 14, 3, 10, 14)))
db.session.add(Post(uid=49, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=65, c2_number=27, league="Legacy",
                    name="Little Cobra", time=datetime.datetime(2016, 9, 6, 21, 5, 5)))
db.session.add(Post(uid=50, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=74, c2_number=306, league="Legacy",
                    name="Sidewalk Enforcer", time=datetime.datetime(2016, 3, 2, 18, 36, 23)))
db.session.add(Post(uid=51, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=187, c2_number=82, league="Legacy",
                    name="Captain Peroxide", time=datetime.datetime(2016, 9, 1, 11, 11, 17)))
db.session.add(Post(uid=52, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=136, c2_number=114, league="Legacy",
                    name="Little General", time=datetime.datetime(2016, 7, 23, 17, 23, 23)))
db.session.add(Post(uid=53, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=159, c2_number=82, league="Legacy",
                    name="Skull Crusher", time=datetime.datetime(2016, 1, 6, 9, 21, 20)))
db.session.add(
    Post(uid=54, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=262, c2_number=161, league="Legacy",
         name="Celtic Charger", time=datetime.datetime(2016, 4, 5, 13, 24, 12)))
db.session.add(Post(uid=55, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=100, c2_number=314,
                    league="Legacy", name="Lord Nikon", time=datetime.datetime(2016, 6, 23, 21, 12, 12)))
db.session.add(Post(uid=56, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=306, c2_number=287, league="Legacy",
                    name="Sky Bully", time=datetime.datetime(2016, 12, 7, 19, 7, 18)))
db.session.add(
    Post(uid=57, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=112, c2_number=148, league="Legacy",
         name="Cereal Killer", time=datetime.datetime(2016, 9, 3, 14, 1, 4)))
db.session.add(
    Post(uid=58, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=279, c2_number=291, league="Legacy",
         name="Lord Pistachio", time=datetime.datetime(2016, 3, 5, 12, 57, 53)))
db.session.add(
    Post(uid=59, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=243, c2_number=24, league="Legacy",
         name="Slow Trot", time=datetime.datetime(2016, 5, 8, 2, 27, 21)))
db.session.add(
    Post(uid=60, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=116, c2_number=30, league="Legacy",
         name="Chicago Blackout", time=datetime.datetime(2016, 4, 5, 7, 14, 47)))
db.session.add(
    Post(uid=61, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=34, c2_number=156, league="Legacy",
         name="Mad Irishman", time=datetime.datetime(2016, 12, 16, 8, 13, 5)))
db.session.add(
    Post(uid=62, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=48, c2_number=121, league="Legacy",
         name="Snake Eyes", time=datetime.datetime(2016, 6, 16, 2, 18, 7)))
db.session.add(
    Post(uid=63, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=21, c2_number=280, league="Legacy",
         name="Chocolate Thunder", time=datetime.datetime(2016, 10, 20, 9, 55, 58)))
db.session.add(
    Post(uid=64, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=247, c2_number=68, league="Legacy",
         name="Mad Jack", time=datetime.datetime(2016, 6, 22, 5, 5, 48)))
db.session.add(
    Post(uid=65, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=139, c2_number=80, league="Legacy",
         name="Snow Hound", time=datetime.datetime(2016, 2, 3, 3, 36, 17)))
db.session.add(
    Post(uid=66, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=74, c2_number=41, league="Legacy",
         name="Chuckles", time=datetime.datetime(2016, 3, 11, 0, 32, 47)))
db.session.add(
    Post(uid=67, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=26, c2_number=294, league="Legacy",
         name="Mad Rascal", time=datetime.datetime(2016, 12, 20, 0, 38, 19)))
db.session.add(Post(uid=68, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=81, c2_number=95, league="Legacy",
                    name="Sofa King", time=datetime.datetime(2016, 2, 11, 19, 30, 10)))
db.session.add(Post(uid=69, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=145, c2_number=85, league="Legacy",
                    name="Commando", time=datetime.datetime(2016, 3, 1, 11, 22, 8)))
db.session.add(
    Post(uid=70, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=38, c2_number=202, league="Legacy",
         name="Manimal", time=datetime.datetime(2016, 3, 19, 8, 13, 49)))
db.session.add(
    Post(uid=71, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=222, c2_number=121, league="Legacy",
         name="Speedwell", time=datetime.datetime(2016, 10, 11, 7, 33, 5)))
db.session.add(Post(uid=72, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=123, c2_number=73, league="Legacy",
                    name="Cool Whip", time=datetime.datetime(2016, 10, 12, 17, 3, 57)))
db.session.add(
    Post(uid=73, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=31, c2_number=305, league="Legacy",
         name="Marbles", time=datetime.datetime(2016, 3, 10, 21, 7, 23)))
db.session.add(Post(uid=74, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=70, c2_number=42, league="Legacy",
                    name="Spider Fuji", time=datetime.datetime(2016, 2, 17, 20, 30, 56)))
db.session.add(
    Post(uid=75, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=292, c2_number=107, league="Legacy",
         name="Cosmo", time=datetime.datetime(2016, 7, 5, 20, 6, 38)))
db.session.add(Post(uid=76, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=81, c2_number=31, league="Legacy",
                    name="Married Man", time=datetime.datetime(2016, 11, 1, 7, 1, 31)))
db.session.add(Post(uid=77, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=190, c2_number=295, league="Legacy",
                    name="Springheel Jack", time=datetime.datetime(2016, 7, 25, 3, 22, 0)))
db.session.add(
    Post(uid=78, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=237, c2_number=99, league="Legacy",
         name="Crash Override", time=datetime.datetime(2016, 10, 2, 4, 14, 31)))
db.session.add(
    Post(uid=79, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=102, c2_number=273, league="Legacy",
         name="Marshmallow", time=datetime.datetime(2016, 8, 19, 13, 2, 28)))
db.session.add(
    Post(uid=80, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=277, c2_number=299, league="Legacy",
         name="Squatch", time=datetime.datetime(2016, 8, 9, 5, 47, 35)))
db.session.add(
    Post(uid=81, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=44, c2_number=52, league="Legacy",
         name="Crash Test", time=datetime.datetime(2016, 10, 17, 20, 5, 6)))
db.session.add(
    Post(uid=82, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=280, c2_number=162, league="Legacy",
         name="Mental", time=datetime.datetime(2016, 3, 25, 3, 21, 18)))
db.session.add(Post(uid=83, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=202, c2_number=60, league="Legacy",
                    name="Stacker of Wheat", time=datetime.datetime(2016, 6, 26, 21, 47, 55)))
db.session.add(Post(uid=84, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=84, c2_number=244, league="Legacy",
                    name="Crazy Eights", time=datetime.datetime(2016, 1, 21, 5, 41, 26)))
db.session.add(
    Post(uid=85, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=183, c2_number=174, league="Legacy",
         name="Mercury Reborn", time=datetime.datetime(2016, 3, 18, 9, 0, 44)))
db.session.add(Post(uid=86, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=276, c2_number=250, league="Legacy",
                    name="Sugar Man", time=datetime.datetime(2016, 4, 13, 6, 6, 26)))
db.session.add(Post(uid=87, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=319, c2_number=195, league="Legacy",
                    name="Criss Cross", time=datetime.datetime(2016, 4, 8, 7, 15, 36)))
db.session.add(
    Post(uid=88, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=156, c2_number=162, league="Legacy",
         name="Midas", time=datetime.datetime(2016, 12, 5, 9, 50, 24)))
db.session.add(Post(uid=89, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=226, c2_number=118, league="Legacy",
                    name="Suicide Jockey", time=datetime.datetime(2016, 10, 24, 17, 43, 52)))
db.session.add(Post(uid=90, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=217, c2_number=58, league="Legacy",
                    name="Cross Thread", time=datetime.datetime(2016, 11, 18, 7, 19, 28)))
db.session.add(
    Post(uid=91, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=250, c2_number=82, league="Legacy",
         name="Midnight Rambler", time=datetime.datetime(2016, 12, 10, 11, 34, 26)))
db.session.add(Post(uid=92, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=223, c2_number=210, league="Legacy",
                    name="Swampmasher", time=datetime.datetime(2016, 3, 5, 6, 40, 45)))
db.session.add(
    Post(uid=93, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=225, c2_number=97, league="Legacy",
         name="Cujo", time=datetime.datetime(2016, 12, 22, 12, 34, 13)))
db.session.add(Post(uid=94, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=51, c2_number=156, league="Legacy",
                    name="Midnight Rider", time=datetime.datetime(2016, 1, 16, 17, 43, 23)))
db.session.add(Post(uid=95, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=176, c2_number=316, league="Legacy",
                    name="Swerve", time=datetime.datetime(2016, 9, 17, 4, 33, 0)))
db.session.add(
    Post(uid=96, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=81, c2_number=153, league="Legacy",
         name="Dancing Madman", time=datetime.datetime(2016, 12, 2, 16, 18, 14)))
db.session.add(
    Post(uid=97, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=257, c2_number=196, league="Legacy",
         name="Mindless Bobcat", time=datetime.datetime(2016, 3, 6, 6, 25, 19)))
db.session.add(
    Post(uid=98, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=102, c2_number=47, league="Legacy",
         name="Tacklebox", time=datetime.datetime(2016, 7, 8, 10, 45, 16)))
db.session.add(
    Post(uid=99, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=246, c2_number=273, league="Legacy",
         name="Dangle", time=datetime.datetime(2016, 11, 5, 21, 23, 48)))
db.session.add(
    Post(uid=100, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=142, c2_number=65, league="Legacy",
         name="Mr. 44", time=datetime.datetime(2016, 1, 6, 1, 42, 36)))
db.session.add(
    Post(uid=101, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=291, c2_number=291, league="Legacy",
         name="Take Away", time=datetime.datetime(2016, 4, 10, 5, 5, 46)))
db.session.add(
    Post(uid=102, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=77, c2_number=310, league="Legacy",
         name="Dark Horse", time=datetime.datetime(2016, 12, 26, 18, 22, 50)))
db.session.add(
    Post(uid=103, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=266, c2_number=52, league="Legacy",
         name="Mr. Fabulous", time=datetime.datetime(2016, 6, 25, 13, 26, 58)))
db.session.add(Post(uid=104, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=144, c2_number=40, league="Legacy",
                    name="Tan Stallion", time=datetime.datetime(2016, 1, 7, 7, 26, 35)))
db.session.add(Post(uid=105, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=118, c2_number=27, league="Legacy",
                    name="Day Hawk", time=datetime.datetime(2016, 8, 23, 10, 40, 36)))
db.session.add(
    Post(uid=106, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=238, c2_number=71, league="Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 10, 14, 8, 0, 26)))
db.session.add(
    Post(uid=107, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=166, c2_number=155, league="Legacy",
         name="The China Wall", time=datetime.datetime(2016, 12, 18, 21, 24, 56)))
db.session.add(
    Post(uid=108, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=237, c2_number=199, league="Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 11, 25, 19, 22, 28)))
db.session.add(Post(uid=109, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=168, c2_number=157,
                    league="Legacy", name="Mr. Lucky", time=datetime.datetime(2016, 2, 28, 6, 29, 18)))
db.session.add(
    Post(uid=110, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=161, c2_number=28, league="Legacy",
         name="The Dude", time=datetime.datetime(2016, 11, 8, 6, 40, 47)))
db.session.add(
    Post(uid=111, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=173, c2_number=24, league="Legacy",
         name="Digger", time=datetime.datetime(2016, 3, 25, 18, 23, 15)))
db.session.add(
    Post(uid=112, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=249, c2_number=153, league="Legacy",
         name="Mr. Peppermint", time=datetime.datetime(2016, 7, 22, 21, 16, 22)))
db.session.add(
    Post(uid=113, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=263, c2_number=221, league="Legacy",
         name="The Flying Mouse", time=datetime.datetime(2016, 5, 2, 10, 2, 2)))
db.session.add(Post(uid=114, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=221, c2_number=176,
                    league="Legacy", name="Disco Thunder", time=datetime.datetime(2016, 12, 24, 20, 15, 48)))
db.session.add(
    Post(uid=115, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=297, c2_number=299, league="Legacy",
         name="Mr. Spy", time=datetime.datetime(2016, 9, 22, 5, 17, 43)))
db.session.add(
    Post(uid=116, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=186, c2_number=41, league="Legacy",
         name="The Happy Jock", time=datetime.datetime(2016, 9, 28, 22, 2, 10)))
db.session.add(Post(uid=117, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=80, c2_number=254,
                    league="Legacy", name="Disco Potato", time=datetime.datetime(2016, 5, 28, 5, 55, 43)))
db.session.add(
    Post(uid=118, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=180, c2_number=318, league="Legacy",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 12, 5, 0, 49, 44)))
db.session.add(
    Post(uid=119, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=52, c2_number=220, league="Legacy",
         name="The Howling Swede", time=datetime.datetime(2016, 12, 10, 10, 18, 41)))
db.session.add(
    Post(uid=120, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=35, c2_number=74, league="Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 9, 14, 11, 37, 53)))
db.session.add(
    Post(uid=121, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=65, c2_number=198, league="Legacy",
         name="Mr. Wholesome", time=datetime.datetime(2016, 7, 16, 1, 3, 50)))
db.session.add(
    Post(uid=122, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=22, c2_number=277, league="Legacy",
         name="Thrasher", time=datetime.datetime(2016, 2, 14, 14, 2, 45)))
db.session.add(
    Post(uid=123, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=224, c2_number=204, league="Legacy",
         name="Dredd", time=datetime.datetime(2016, 4, 9, 7, 46, 4)))
db.session.add(
    Post(uid=124, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=109, c2_number=278, league="Legacy",
         name="Mud Pie Man", time=datetime.datetime(2016, 10, 1, 15, 34, 54)))
db.session.add(
    Post(uid=125, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=194, c2_number=228, league="Legacy",
         name="Toe", time=datetime.datetime(2016, 12, 1, 4, 55, 8)))
db.session.add(
    Post(uid=126, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=263, c2_number=315, league="Legacy",
         name="Dropkick", time=datetime.datetime(2016, 8, 21, 6, 33, 55)))
db.session.add(Post(uid=127, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=226, c2_number=268,
                    league="Legacy", name="Mule Skinner", time=datetime.datetime(2016, 9, 16, 21, 49, 28)))
db.session.add(
    Post(uid=128, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=152, c2_number=222, league="Legacy",
         name="Toolmaker", time=datetime.datetime(2016, 2, 27, 5, 18, 25)))
db.session.add(
    Post(uid=129, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=277, c2_number=59, league="Legacy",
         name="Drop Stone", time=datetime.datetime(2016, 12, 14, 10, 4, 50)))
db.session.add(
    Post(uid=130, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=239, c2_number=91, league="Legacy",
         name="Murmur", time=datetime.datetime(2016, 10, 17, 9, 39, 10)))
db.session.add(
    Post(uid=131, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=158, c2_number=147, league="Legacy",
         name="Tough Nut", time=datetime.datetime(2016, 1, 14, 4, 25, 35)))
db.session.add(
    Post(uid=132, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=180, c2_number=248, league="Legacy",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 11, 26, 2, 0, 52)))
db.session.add(
    Post(uid=133, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=280, c2_number=118, league="Legacy",
         name="Nacho", time=datetime.datetime(2016, 9, 23, 22, 37, 17)))
db.session.add(
    Post(uid=134, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=95, c2_number=183, league="Legacy",
         name="Trip", time=datetime.datetime(2016, 3, 26, 4, 41, 11)))
db.session.add(
    Post(uid=135, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=263, c2_number=317, league="Legacy",
         name="Easy Sweep", time=datetime.datetime(2016, 8, 10, 11, 25, 17)))
db.session.add(
    Post(uid=136, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=169, c2_number=208, league="Legacy",
         name="Natural Mess", time=datetime.datetime(2016, 1, 25, 12, 11, 36)))
db.session.add(
    Post(uid=137, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=299, c2_number=76, league="Legacy",
         name="Troubadour", time=datetime.datetime(2016, 2, 27, 16, 27, 8)))
db.session.add(
    Post(uid=138, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=116, c2_number=154, league="Legacy",
         name="Electric Player", time=datetime.datetime(2016, 8, 23, 20, 0, 53)))
db.session.add(
    Post(uid=139, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=84, c2_number=124, league="Legacy",
         name="Necromancer", time=datetime.datetime(2016, 3, 13, 6, 24, 54)))
db.session.add(
    Post(uid=140, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=306, c2_number=314, league="Legacy",
         name="Turnip King", time=datetime.datetime(2016, 6, 21, 21, 50, 53)))
db.session.add(
    Post(uid=141, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=270, c2_number=297, league="Legacy",
         name="Esquire", time=datetime.datetime(2016, 2, 11, 10, 42, 5)))
db.session.add(
    Post(uid=142, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=180, c2_number=62, league="Legacy",
         name="Neophyte Believer", time=datetime.datetime(2016, 10, 3, 8, 40, 14)))
db.session.add(
    Post(uid=143, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=233, c2_number=155, league="Legacy",
         name="Twitch", time=datetime.datetime(2016, 11, 10, 8, 20, 37)))
db.session.add(
    Post(uid=144, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=140, c2_number=190, league="Legacy",
         name="Fast Draw", time=datetime.datetime(2016, 1, 15, 13, 47, 52)))
db.session.add(Post(uid=145, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=67, c2_number=270,
                    league="Legacy", name="Nessie", time=datetime.datetime(2016, 5, 4, 6, 36, 38)))
db.session.add(
    Post(uid=146, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=71, c2_number=144, league="Legacy",
         name="Vagabond Warrior", time=datetime.datetime(2016, 3, 25, 20, 38, 12)))
db.session.add(
    Post(uid=147, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=91, c2_number=154, league="Legacy",
         name="Flakes", time=datetime.datetime(2016, 10, 20, 19, 23, 18)))
db.session.add(
    Post(uid=148, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=45, c2_number=182, league="Legacy",
         name="New Cycle", time=datetime.datetime(2016, 5, 15, 20, 56, 8)))
db.session.add(
    Post(uid=149, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=153, c2_number=121, league="Legacy",
         name="Voluntary", time=datetime.datetime(2016, 11, 19, 5, 24, 17)))
db.session.add(
    Post(uid=150, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=149, c2_number=285, league="Legacy",
         name="Flint", time=datetime.datetime(2016, 7, 1, 18, 5, 18)))
db.session.add(
    Post(uid=151, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=65, c2_number=296, league="Legacy",
         name="Nickname Master", time=datetime.datetime(2016, 3, 17, 1, 33, 55)))
db.session.add(
    Post(uid=152, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=52, c2_number=154, league="Legacy",
         name="Vortex", time=datetime.datetime(2016, 11, 8, 18, 10, 35)))
db.session.add(
    Post(uid=153, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=199, c2_number=207, league="Legacy",
         name="Freak", time=datetime.datetime(2016, 7, 26, 12, 56, 36)))
db.session.add(
    Post(uid=154, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=280, c2_number=99, league="Legacy",
         name="Nightmare King", time=datetime.datetime(2016, 5, 4, 15, 2, 18)))
db.session.add(
    Post(uid=155, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=201, c2_number=314, league="Legacy",
         name="Washer", time=datetime.datetime(2016, 11, 22, 11, 58, 5)))
db.session.add(
    Post(uid=156, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=203, c2_number=145, league="Legacy",
         name="Gas Man", time=datetime.datetime(2016, 1, 12, 1, 32, 1)))
db.session.add(
    Post(uid=157, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=88, c2_number=279, league="Legacy",
         name="Night Train", time=datetime.datetime(2016, 6, 15, 16, 6, 28)))
db.session.add(
    Post(uid=158, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=97, c2_number=132, league="Legacy",
         name="Waylay Dave", time=datetime.datetime(2016, 1, 24, 10, 53, 21)))
db.session.add(
    Post(uid=159, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=134, c2_number=116, league="Legacy",
         name="Glyph", time=datetime.datetime(2016, 8, 22, 11, 30, 20)))
db.session.add(
    Post(uid=160, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=146, c2_number=217, league="Legacy",
         name="Old Man Winter", time=datetime.datetime(2016, 3, 18, 10, 29, 15)))
db.session.add(
    Post(uid=161, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=146, c2_number=138, league="Legacy",
         name="Wheels", time=datetime.datetime(2016, 3, 27, 6, 20, 29)))
db.session.add(
    Post(uid=162, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=123, c2_number=280, league="Legacy",
         name="Grave Digger", time=datetime.datetime(2016, 12, 11, 6, 14, 38)))
db.session.add(Post(uid=163, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=217, c2_number=133,
                    league="Legacy", name="Old Orange Eyes", time=datetime.datetime(2016, 6, 3, 21, 29, 15)))
db.session.add(
    Post(uid=164, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=161, c2_number=255, league="Legacy",
         name="Wooden Man", time=datetime.datetime(2016, 3, 10, 17, 19, 44)))
db.session.add(
    Post(uid=165, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=223, c2_number=94, league="Legacy",
         name="Guillotine", time=datetime.datetime(2016, 12, 3, 11, 2, 22)))
db.session.add(
    Post(uid=166, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=176, c2_number=169, league="Legacy",
         name="Old Regret", time=datetime.datetime(2016, 4, 9, 18, 37, 22)))
db.session.add(
    Post(uid=167, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=53, c2_number=232, league="Legacy",
         name="Woo Woo", time=datetime.datetime(2016, 9, 3, 18, 55, 24)))
db.session.add(Post(uid=168, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=59, c2_number=305,
                    league="Legacy", name="Gunhawk", time=datetime.datetime(2016, 11, 24, 19, 37, 27)))
db.session.add(
    Post(uid=169, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=163, c2_number=162, league="Legacy",
         name="Onion King", time=datetime.datetime(2016, 11, 16, 3, 12, 11)))
db.session.add(
    Post(uid=170, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=61, c2_number=26, league="Legacy",
         name="Yellow Menace", time=datetime.datetime(2016, 5, 18, 12, 27, 10)))
db.session.add(Post(uid=171, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=160, c2_number=53,
                    league="Legacy", name="High Kingdom Warrior", time=datetime.datetime(2016, 9, 28, 19, 37, 6)))
db.session.add(
    Post(uid=172, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=310, c2_number=54, league="Legacy",
         name="Osprey", time=datetime.datetime(2016, 4, 22, 8, 48, 4)))
db.session.add(
    Post(uid=173, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=58, c2_number=291, league="Legacy",
         name="Zero Charisma", time=datetime.datetime(2016, 2, 19, 0, 18, 31)))
db.session.add(
    Post(uid=174, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=81, c2_number=193, league="Legacy",
         name="Highlander Monk", time=datetime.datetime(2016, 8, 7, 11, 0, 22)))
db.session.add(
    Post(uid=175, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=178, c2_number=144, league="Legacy",
         name="Overrun", time=datetime.datetime(2016, 2, 19, 16, 18, 48)))
db.session.add(
    Post(uid=176, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=256, c2_number=70, league="Legacy",
         name="Zesty Dragon", time=datetime.datetime(2016, 8, 15, 9, 24, 9)))
db.session.add(
    Post(uid=177, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=76, c2_number=190, league="Legacy",
         name="Zod", time=datetime.datetime(2016, 7, 11, 16, 55, 58)))
db.session.add(
    Post(uid=0, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=124, c2_number=211, league="Legacy",
         name="101", time=datetime.datetime(2016, 4, 20, 2, 20, 28)))
db.session.add(
    Post(uid=1, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=151, c2_number=242, league="Legacy",
         name="Houston", time=datetime.datetime(2016, 2, 23, 21, 38, 42)))
db.session.add(
    Post(uid=2, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=189, c2_number=318, league="Legacy",
         name="Pinball Wizard", time=datetime.datetime(2016, 9, 20, 9, 43, 5)))
db.session.add(
    Post(uid=3, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=286, c2_number=255, league="Legacy",
         name="Accidental Genius", time=datetime.datetime(2016, 6, 7, 4, 11, 18)))
db.session.add(Post(uid=4, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=118, c2_number=94, league="Legacy",
                    name="Hyper", time=datetime.datetime(2016, 10, 18, 22, 47, 8)))
db.session.add(
    Post(uid=5, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=201, c2_number=281, league="Legacy",
         name="Pluto", time=datetime.datetime(2016, 10, 25, 16, 0, 1)))
db.session.add(Post(uid=6, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=229, c2_number=239, league="Legacy",
                    name="Alpha", time=datetime.datetime(2016, 12, 13, 2, 33, 29)))
db.session.add(
    Post(uid=7, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=212, c2_number=228, league="Legacy",
         name="Jester", time=datetime.datetime(2016, 11, 16, 7, 16, 7)))
db.session.add(
    Post(uid=8, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=28, c2_number=177, league="Legacy",
         name="Pogue", time=datetime.datetime(2016, 7, 6, 2, 51, 15)))
db.session.add(
    Post(uid=9, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=178, c2_number=219, league="Legacy",
         name="Airport Hobo", time=datetime.datetime(2016, 3, 21, 5, 1, 43)))
db.session.add(
    Post(uid=10, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=59, c2_number=294, league="Legacy",
         name="Jigsaw", time=datetime.datetime(2016, 7, 24, 18, 45, 31)))
db.session.add(
    Post(uid=11, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=200, c2_number=136, league="Legacy",
         name="Prometheus", time=datetime.datetime(2016, 8, 3, 20, 25, 40)))
db.session.add(
    Post(uid=12, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=222, c2_number=285, league="Legacy",
         name="Bearded Angler", time=datetime.datetime(2016, 2, 5, 19, 39, 52)))
db.session.add(
    Post(uid=13, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=129, c2_number=238, league="Legacy",
         name="Joker's Grin", time=datetime.datetime(2016, 11, 12, 20, 28, 27)))
db.session.add(
    Post(uid=14, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=88, c2_number=108, league="Legacy",
         name="Psycho Thinker", time=datetime.datetime(2016, 11, 11, 22, 29, 12)))
db.session.add(
    Post(uid=15, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=33, c2_number=317, league="Legacy",
         name="Beetle King", time=datetime.datetime(2016, 1, 9, 16, 7, 42)))
db.session.add(Post(uid=16, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=35, c2_number=230, league="Legacy",
                    name="Judge", time=datetime.datetime(2016, 5, 5, 4, 17, 51)))
db.session.add(Post(uid=17, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=237, c2_number=118, league="Legacy",
                    name="Pusher", time=datetime.datetime(2016, 12, 11, 5, 33, 49)))
db.session.add(
    Post(uid=18, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=265, c2_number=143, league="Legacy",
         name="Bitmap", time=datetime.datetime(2016, 9, 4, 0, 45, 34)))
db.session.add(
    Post(uid=19, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=46, c2_number=260, league="Legacy",
         name="Junkyard Dog", time=datetime.datetime(2016, 6, 22, 8, 57, 5)))
db.session.add(
    Post(uid=20, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=278, c2_number=182, league="Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 8, 4, 16, 13, 24)))
db.session.add(
    Post(uid=21, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=269, c2_number=70, league="Legacy",
         name="Blister", time=datetime.datetime(2016, 3, 22, 13, 38, 44)))
db.session.add(
    Post(uid=22, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=188, c2_number=45, league="Legacy", name="K-9",
         time=datetime.datetime(2016, 5, 12, 8, 17, 22)))
db.session.add(
    Post(uid=23, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=278, c2_number=105, league="Legacy",
         name="Roadblock", time=datetime.datetime(2016, 5, 23, 19, 33, 16)))
db.session.add(Post(uid=24, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=234, c2_number=99, league="Legacy",
                    name="Bowie", time=datetime.datetime(2016, 3, 19, 7, 14, 2)))
db.session.add(
    Post(uid=25, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=237, c2_number=304, league="Legacy",
         name="Keystone", time=datetime.datetime(2016, 1, 10, 8, 37, 30)))
db.session.add(
    Post(uid=26, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=267, c2_number=101, league="Legacy",
         name="Rooster", time=datetime.datetime(2016, 10, 18, 14, 55, 9)))
db.session.add(
    Post(uid=27, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=80, c2_number=278, league="Legacy",
         name="Bowler", time=datetime.datetime(2016, 9, 13, 0, 27, 30)))
db.session.add(
    Post(uid=28, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=59, c2_number=215, league="Legacy",
         name="Kickstart", time=datetime.datetime(2016, 6, 20, 19, 14, 13)))
db.session.add(
    Post(uid=29, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=242, c2_number=204, league="Legacy",
         name="Sandbox", time=datetime.datetime(2016, 3, 25, 13, 9, 41)))
db.session.add(
    Post(uid=30, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=131, c2_number=224, league="Legacy",
         name="Breadmaker", time=datetime.datetime(2016, 3, 1, 14, 40, 7)))
db.session.add(
    Post(uid=31, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=96, c2_number=215, league="Legacy",
         name="Kill Switch", time=datetime.datetime(2016, 7, 24, 5, 24, 21)))
db.session.add(
    Post(uid=32, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=212, c2_number=112, league="Legacy",
         name="Scrapper", time=datetime.datetime(2016, 4, 12, 1, 19, 23)))
db.session.add(
    Post(uid=33, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=28, c2_number=28, league="Legacy",
         name="Broomspun", time=datetime.datetime(2016, 10, 25, 14, 50, 32)))
db.session.add(Post(uid=34, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=220, c2_number=237, league="Legacy",
                    name="Kingfisher", time=datetime.datetime(2016, 7, 15, 5, 5, 23)))
db.session.add(Post(uid=35, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=125, c2_number=247, league="Legacy",
                    name="Screwtape", time=datetime.datetime(2016, 10, 5, 6, 17, 32)))
db.session.add(
    Post(uid=36, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=177, c2_number=318, league="Legacy",
         name="Buckshot", time=datetime.datetime(2016, 6, 8, 21, 42, 53)))
db.session.add(
    Post(uid=37, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=124, c2_number=68, league="Legacy",
         name="Kitchen", time=datetime.datetime(2016, 7, 2, 4, 0, 30)))
db.session.add(
    Post(uid=38, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=69, c2_number=145, league="Legacy",
         name="Sexual Chocolate", time=datetime.datetime(2016, 3, 17, 22, 55, 29)))
db.session.add(Post(uid=39, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=245, c2_number=164,
                    league="Legacy", name="Bugger", time=datetime.datetime(2016, 11, 14, 22, 20, 47)))
db.session.add(Post(uid=40, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=234, c2_number=133, league="Legacy",
                    name="Knuckles", time=datetime.datetime(2016, 6, 12, 12, 29, 45)))
db.session.add(
    Post(uid=41, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=271, c2_number=65, league="Legacy",
         name="Shadow Chaser", time=datetime.datetime(2016, 11, 4, 11, 30, 54)))
db.session.add(
    Post(uid=42, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=269, c2_number=262, league="Legacy",
         name="Cabbie", time=datetime.datetime(2016, 9, 4, 6, 39, 34)))
db.session.add(
    Post(uid=43, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=262, c2_number=225, league="Legacy",
         name="Lady Killer", time=datetime.datetime(2016, 2, 15, 21, 57, 55)))
db.session.add(
    Post(uid=44, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=131, c2_number=223, league="Legacy",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 10, 6, 2, 48, 36)))
db.session.add(
    Post(uid=45, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=278, c2_number=156, league="Legacy",
         name="Candy Butcher", time=datetime.datetime(2016, 11, 27, 7, 53, 16)))
db.session.add(
    Post(uid=46, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=92, c2_number=193, league="Legacy",
         name="Liquid Science", time=datetime.datetime(2016, 4, 24, 16, 43, 29)))
db.session.add(
    Post(uid=47, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=84, c2_number=222, league="Legacy",
         name="Shooter", time=datetime.datetime(2016, 5, 9, 14, 24, 45)))
db.session.add(
    Post(uid=48, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=53, c2_number=156, league="Legacy",
         name="Capital F", time=datetime.datetime(2016, 8, 26, 7, 13, 53)))
db.session.add(
    Post(uid=49, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=160, c2_number=289, league="Legacy",
         name="Little Cobra", time=datetime.datetime(2016, 1, 23, 1, 26, 4)))
db.session.add(
    Post(uid=50, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=269, c2_number=118, league="Legacy",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 8, 13, 19, 7, 48)))
db.session.add(
    Post(uid=51, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=301, c2_number=130, league="Legacy",
         name="Captain Peroxide", time=datetime.datetime(2016, 7, 6, 1, 29, 57)))
db.session.add(Post(uid=52, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=67, c2_number=52, league="Legacy",
                    name="Little General", time=datetime.datetime(2016, 4, 15, 0, 26, 30)))
db.session.add(Post(uid=53, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=113, c2_number=281, league="Legacy",
                    name="Skull Crusher", time=datetime.datetime(2016, 3, 4, 18, 26, 32)))
db.session.add(
    Post(uid=54, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=156, c2_number=36, league="Legacy",
         name="Celtic Charger", time=datetime.datetime(2016, 11, 17, 13, 34, 7)))
db.session.add(
    Post(uid=55, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=163, c2_number=23, league="Legacy",
         name="Lord Nikon", time=datetime.datetime(2016, 10, 14, 4, 37, 32)))
db.session.add(
    Post(uid=56, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=224, c2_number=167, league="Legacy",
         name="Sky Bully", time=datetime.datetime(2016, 6, 3, 6, 8, 54)))
db.session.add(Post(uid=57, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=85, c2_number=269,
                    league="Legacy", name="Cereal Killer", time=datetime.datetime(2016, 11, 28, 1, 12, 0)))
db.session.add(Post(uid=58, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=38, c2_number=64, league="Legacy",
                    name="Lord Pistachio", time=datetime.datetime(2016, 3, 5, 4, 3, 15)))
db.session.add(
    Post(uid=59, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=296, c2_number=191, league="Legacy",
         name="Slow Trot", time=datetime.datetime(2016, 2, 25, 10, 33, 54)))
db.session.add(
    Post(uid=60, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=113, c2_number=83, league="Legacy",
         name="Chicago Blackout", time=datetime.datetime(2016, 3, 24, 5, 21, 31)))
db.session.add(
    Post(uid=61, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=302, c2_number=72, league="Legacy",
         name="Mad Irishman", time=datetime.datetime(2016, 9, 19, 4, 35, 47)))
db.session.add(
    Post(uid=62, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=110, c2_number=81, league="Legacy",
         name="Snake Eyes", time=datetime.datetime(2016, 9, 16, 9, 24, 53)))
db.session.add(
    Post(uid=63, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=119, c2_number=284, league="Legacy",
         name="Chocolate Thunder", time=datetime.datetime(2016, 7, 3, 21, 56, 38)))
db.session.add(
    Post(uid=64, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=89, c2_number=307, league="Legacy",
         name="Mad Jack", time=datetime.datetime(2016, 11, 16, 15, 43, 27)))
db.session.add(
    Post(uid=65, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=270, c2_number=298, league="Legacy",
         name="Snow Hound", time=datetime.datetime(2016, 12, 14, 8, 48, 20)))
db.session.add(
    Post(uid=66, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=27, c2_number=212, league="Legacy",
         name="Chuckles", time=datetime.datetime(2016, 12, 7, 9, 57, 34)))
db.session.add(
    Post(uid=67, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=224, c2_number=291, league="Legacy",
         name="Mad Rascal", time=datetime.datetime(2016, 1, 7, 20, 51, 57)))
db.session.add(
    Post(uid=68, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=144, c2_number=148, league="Legacy",
         name="Sofa King", time=datetime.datetime(2016, 2, 28, 9, 41, 38)))
db.session.add(
    Post(uid=69, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=142, c2_number=33, league="Legacy",
         name="Commando", time=datetime.datetime(2016, 5, 22, 16, 24, 51)))
db.session.add(
    Post(uid=70, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=317, c2_number=21, league="Legacy",
         name="Manimal", time=datetime.datetime(2016, 3, 7, 11, 17, 14)))
db.session.add(
    Post(uid=71, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=210, c2_number=270, league="Legacy",
         name="Speedwell", time=datetime.datetime(2016, 12, 4, 22, 33, 50)))
db.session.add(
    Post(uid=72, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=152, c2_number=302, league="Legacy",
         name="Cool Whip", time=datetime.datetime(2016, 9, 16, 9, 18, 37)))
db.session.add(
    Post(uid=73, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=40, c2_number=280, league="Legacy",
         name="Marbles", time=datetime.datetime(2016, 7, 5, 7, 15, 35)))
db.session.add(Post(uid=74, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=249, c2_number=202, league="Legacy",
                    name="Spider Fuji", time=datetime.datetime(2016, 9, 28, 14, 44, 8)))
db.session.add(
    Post(uid=75, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=319, c2_number=182, league="Legacy",
         name="Cosmo", time=datetime.datetime(2016, 6, 6, 7, 6, 37)))
db.session.add(Post(uid=76, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=277, c2_number=68, league="Legacy",
                    name="Married Man", time=datetime.datetime(2016, 5, 27, 15, 57, 51)))
db.session.add(Post(uid=77, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=115, c2_number=57, league="Legacy",
                    name="Springheel Jack", time=datetime.datetime(2016, 8, 9, 20, 54, 50)))
db.session.add(Post(uid=78, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=174, c2_number=260, league="Legacy",
                    name="Crash Override", time=datetime.datetime(2016, 11, 3, 4, 25, 34)))
db.session.add(Post(uid=79, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=249, c2_number=215, league="Legacy",
                    name="Marshmallow", time=datetime.datetime(2016, 5, 27, 4, 39, 14)))
db.session.add(
    Post(uid=80, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=170, c2_number=234, league="Legacy",
         name="Squatch", time=datetime.datetime(2016, 3, 3, 0, 11, 2)))
db.session.add(Post(uid=81, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=308, c2_number=39, league="Legacy",
                    name="Crash Test", time=datetime.datetime(2016, 5, 27, 5, 37, 58)))
db.session.add(Post(uid=82, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=196, c2_number=20, league="Legacy",
                    name="Mental", time=datetime.datetime(2016, 9, 19, 9, 1, 49)))
db.session.add(
    Post(uid=83, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=54, c2_number=221, league="Legacy",
         name="Stacker of Wheat", time=datetime.datetime(2016, 7, 21, 20, 13, 31)))
db.session.add(Post(uid=84, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=24, c2_number=243, league="Legacy",
                    name="Crazy Eights", time=datetime.datetime(2016, 2, 27, 20, 48, 9)))
db.session.add(Post(uid=85, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=318, c2_number=173, league="Legacy",
                    name="Mercury Reborn", time=datetime.datetime(2016, 2, 26, 18, 24, 57)))
db.session.add(Post(uid=86, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=278, c2_number=74, league="Legacy",
                    name="Sugar Man", time=datetime.datetime(2016, 5, 13, 3, 52, 4)))
db.session.add(
    Post(uid=87, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=239, c2_number=308, league="Legacy",
         name="Criss Cross", time=datetime.datetime(2016, 10, 13, 9, 56, 9)))
db.session.add(
    Post(uid=88, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=234, c2_number=285, league="Legacy", name="Midas",
         time=datetime.datetime(2016, 12, 24, 0, 56, 29)))
db.session.add(Post(uid=89, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=260, c2_number=137, league="Legacy",
                    name="Suicide Jockey", time=datetime.datetime(2016, 4, 13, 21, 44, 50)))
db.session.add(Post(uid=90, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=153, c2_number=74, league="Legacy",
                    name="Cross Thread", time=datetime.datetime(2016, 12, 3, 11, 11, 47)))
db.session.add(Post(uid=91, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=96, c2_number=255, league="Legacy",
                    name="Midnight Rambler", time=datetime.datetime(2016, 1, 10, 7, 51, 3)))
db.session.add(Post(uid=92, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=132, c2_number=55, league="Legacy",
                    name="Swampmasher", time=datetime.datetime(2016, 5, 16, 16, 19, 24)))
db.session.add(
    Post(uid=93, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=157, c2_number=260, league="Legacy",
         name="Cujo", time=datetime.datetime(2016, 5, 22, 21, 48, 17)))
db.session.add(Post(uid=94, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=305, c2_number=277, league="Legacy",
                    name="Midnight Rider", time=datetime.datetime(2016, 2, 10, 16, 45, 28)))
db.session.add(Post(uid=95, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=185, c2_number=180, league="Legacy",
                    name="Swerve", time=datetime.datetime(2016, 2, 2, 3, 26, 45)))
db.session.add(Post(uid=96, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=190, c2_number=174, league="Legacy",
                    name="Dancing Madman", time=datetime.datetime(2016, 11, 11, 5, 2, 19)))
db.session.add(Post(uid=97, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=302, c2_number=297, league="Legacy",
                    name="Mindless Bobcat", time=datetime.datetime(2016, 1, 12, 13, 12, 17)))
db.session.add(
    Post(uid=98, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=176, c2_number=210, league="Legacy",
         name="Tacklebox", time=datetime.datetime(2016, 7, 6, 11, 42, 17)))
db.session.add(Post(uid=99, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=279, c2_number=58, league="Legacy",
                    name="Dangle", time=datetime.datetime(2016, 6, 16, 6, 30, 16)))
db.session.add(
    Post(uid=100, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=109, c2_number=248, league="Legacy",
         name="Mr. 44", time=datetime.datetime(2016, 9, 25, 13, 38, 6)))
db.session.add(
    Post(uid=101, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=297, c2_number=61, league="Legacy",
         name="Take Away", time=datetime.datetime(2016, 3, 16, 21, 42, 31)))
db.session.add(Post(uid=102, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=276, c2_number=177, league="Legacy",
                    name="Dark Horse", time=datetime.datetime(2016, 6, 5, 9, 41, 23)))
db.session.add(Post(uid=103, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=268, c2_number=257, league="Legacy",
                    name="Mr. Fabulous", time=datetime.datetime(2016, 8, 8, 19, 33, 49)))
db.session.add(Post(uid=104, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=52, c2_number=251, league="Legacy",
                    name="Tan Stallion", time=datetime.datetime(2016, 3, 22, 19, 22, 14)))
db.session.add(
    Post(uid=105, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=300, c2_number=78, league="Legacy",
         name="Day Hawk", time=datetime.datetime(2016, 2, 14, 12, 36, 33)))
db.session.add(Post(uid=106, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=291, c2_number=120, league="Legacy",
                    name="Mr. Gadget", time=datetime.datetime(2016, 7, 4, 9, 49, 25)))
db.session.add(Post(uid=107, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=175, c2_number=295, league="Legacy",
                    name="The China Wall", time=datetime.datetime(2016, 3, 3, 11, 15, 56)))
db.session.add(Post(uid=108, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=94, c2_number=193, league="Legacy",
                    name="Desert Haze", time=datetime.datetime(2016, 8, 1, 8, 10, 1)))
db.session.add(Post(uid=109, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=161, c2_number=289, league="Legacy",
                    name="Mr. Lucky", time=datetime.datetime(2016, 10, 25, 7, 19, 7)))
db.session.add(
    Post(uid=110, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=148, c2_number=38, league="Legacy",
         name="The Dude", time=datetime.datetime(2016, 10, 2, 2, 47, 53)))
db.session.add(Post(uid=111, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=196, c2_number=76,
                    league="Legacy", name="Digger", time=datetime.datetime(2016, 10, 16, 0, 20, 36)))
db.session.add(Post(uid=112, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=200, c2_number=37, league="Legacy",
                    name="Mr. Peppermint", time=datetime.datetime(2016, 6, 28, 20, 24, 13)))
db.session.add(
    Post(uid=113, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=204, c2_number=247, league="Legacy",
         name="The Flying Mouse", time=datetime.datetime(2016, 5, 5, 19, 19, 38)))
db.session.add(
    Post(uid=114, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=147, c2_number=70, league="Legacy",
         name="Disco Thunder", time=datetime.datetime(2016, 11, 9, 8, 4, 49)))
db.session.add(
    Post(uid=115, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=256, c2_number=69, league="Legacy",
         name="Mr. Spy", time=datetime.datetime(2016, 3, 8, 16, 33, 50)))
db.session.add(
    Post(uid=116, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=227, c2_number=254, league="Legacy",
         name="The Happy Jock", time=datetime.datetime(2016, 1, 19, 21, 19, 21)))
db.session.add(
    Post(uid=117, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=183, c2_number=286, league="Legacy",
         name="Disco Potato", time=datetime.datetime(2016, 2, 9, 1, 17, 22)))
db.session.add(
    Post(uid=118, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=149, c2_number=205, league="Legacy",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 10, 19, 8, 49, 27)))
db.session.add(
    Post(uid=119, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=253, c2_number=165, league="Legacy",
         name="The Howling Swede", time=datetime.datetime(2016, 8, 14, 14, 30, 0)))
db.session.add(
    Post(uid=120, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=253, c2_number=229, league="Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 7, 28, 8, 54, 53)))
db.session.add(
    Post(uid=121, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=51, c2_number=47, league="Legacy",
         name="Mr. Wholesome", time=datetime.datetime(2016, 7, 15, 22, 49, 38)))
db.session.add(
    Post(uid=122, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=306, c2_number=61, league="Legacy",
         name="Thrasher", time=datetime.datetime(2016, 3, 3, 13, 49, 2)))
db.session.add(
    Post(uid=123, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=179, c2_number=72, league="Legacy",
         name="Dredd", time=datetime.datetime(2016, 5, 18, 4, 28, 25)))
db.session.add(Post(uid=124, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=39, c2_number=309, league="Legacy",
                    name="Mud Pie Man", time=datetime.datetime(2016, 1, 20, 19, 2, 11)))
db.session.add(
    Post(uid=125, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=172, c2_number=93, league="Legacy", name="Toe",
         time=datetime.datetime(2016, 5, 2, 7, 27, 28)))
db.session.add(
    Post(uid=126, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=226, c2_number=140, league="Legacy",
         name="Dropkick", time=datetime.datetime(2016, 2, 21, 16, 39, 28)))
db.session.add(
    Post(uid=127, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=30, c2_number=42, league="Legacy",
         name="Mule Skinner", time=datetime.datetime(2016, 3, 17, 17, 22, 27)))
db.session.add(Post(uid=128, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=71, c2_number=184, league="Legacy",
                    name="Toolmaker", time=datetime.datetime(2016, 10, 7, 15, 35, 26)))
db.session.add(
    Post(uid=129, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=294, c2_number=51, league="Legacy",
         name="Drop Stone", time=datetime.datetime(2016, 6, 6, 14, 50, 5)))
db.session.add(Post(uid=130, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=277, c2_number=90, league="Legacy",
                    name="Murmur", time=datetime.datetime(2016, 3, 6, 6, 19, 21)))
db.session.add(
    Post(uid=131, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=129, c2_number=43, league="Legacy",
         name="Tough Nut", time=datetime.datetime(2016, 8, 11, 18, 40, 38)))
db.session.add(Post(uid=132, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=156, c2_number=292, league="Legacy",
                    name="Drugstore Cowboy", time=datetime.datetime(2016, 8, 13, 16, 25, 56)))
db.session.add(
    Post(uid=133, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=142, c2_number=154, league="Legacy",
         name="Nacho", time=datetime.datetime(2016, 2, 7, 13, 31, 25)))
db.session.add(
    Post(uid=134, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=313, c2_number=80, league="Legacy",
         name="Trip", time=datetime.datetime(2016, 7, 3, 5, 39, 52)))
db.session.add(
    Post(uid=135, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=203, c2_number=280, league="Legacy",
         name="Easy Sweep", time=datetime.datetime(2016, 4, 21, 20, 18, 28)))
db.session.add(
    Post(uid=136, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=127, c2_number=70, league="Legacy",
         name="Natural Mess", time=datetime.datetime(2016, 9, 4, 8, 1, 47)))
db.session.add(
    Post(uid=137, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=195, c2_number=253, league="Legacy",
         name="Troubadour", time=datetime.datetime(2016, 7, 8, 19, 22, 25)))
db.session.add(
    Post(uid=138, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=108, c2_number=81, league="Legacy",
         name="Electric Player", time=datetime.datetime(2016, 12, 9, 19, 30, 40)))
db.session.add(
    Post(uid=139, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=113, c2_number=317, league="Legacy",
         name="Necromancer", time=datetime.datetime(2016, 8, 25, 3, 54, 42)))
db.session.add(
    Post(uid=140, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=280, c2_number=277, league="Legacy",
         name="Turnip King", time=datetime.datetime(2016, 7, 12, 17, 58, 21)))
db.session.add(
    Post(uid=141, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=210, c2_number=32, league="Legacy",
         name="Esquire", time=datetime.datetime(2016, 4, 4, 19, 36, 22)))
db.session.add(Post(uid=142, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=199, c2_number=317, league="Legacy",
                    name="Neophyte Believer", time=datetime.datetime(2016, 2, 11, 4, 32, 48)))
db.session.add(Post(uid=143, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=186, c2_number=152, league="Legacy",
                    name="Twitch", time=datetime.datetime(2016, 7, 7, 6, 42, 9)))
db.session.add(
    Post(uid=144, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=43, c2_number=150, league="Legacy",
         name="Fast Draw", time=datetime.datetime(2016, 10, 14, 22, 43, 50)))
db.session.add(
    Post(uid=145, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=171, c2_number=233, league="Legacy",
         name="Nessie", time=datetime.datetime(2016, 12, 5, 12, 45, 10)))
db.session.add(
    Post(uid=146, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=202, c2_number=205, league="Hardcore Legacy",
         name="Vagabond Warrior", time=datetime.datetime(2016, 11, 8, 15, 22, 8)))
db.session.add(Post(uid=147, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=278, c2_number=212,
                    league="Hardcore Legacy", name="Flakes", time=datetime.datetime(2016, 8, 25, 10, 25, 32)))
db.session.add(
    Post(uid=148, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=114, c2_number=88, league="Hardcore Legacy",
         name="New Cycle", time=datetime.datetime(2016, 9, 7, 20, 29, 10)))
db.session.add(
    Post(uid=149, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=73, c2_number=24, league="Hardcore Legacy",
         name="Voluntary", time=datetime.datetime(2016, 2, 8, 10, 2, 54)))
db.session.add(
    Post(uid=150, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=276, c2_number=63, league="Hardcore Legacy",
         name="Flint", time=datetime.datetime(2016, 4, 7, 5, 43, 55)))
db.session.add(
    Post(uid=151, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=181, c2_number=135, league="Hardcore Legacy",
         name="Nickname Master", time=datetime.datetime(2016, 2, 7, 1, 7, 39)))
db.session.add(Post(uid=152, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=196, c2_number=224,
                    league="Hardcore Legacy", name="Vortex", time=datetime.datetime(2016, 6, 10, 7, 23, 0)))
db.session.add(Post(uid=153, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=296, c2_number=211,
                    league="Hardcore Legacy", name="Freak", time=datetime.datetime(2016, 2, 8, 19, 10, 16)))
db.session.add(Post(uid=154, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=29, c2_number=301,
                    league="Hardcore Legacy", name="Nightmare King", time=datetime.datetime(2016, 9, 4, 13, 30, 52)))
db.session.add(Post(uid=155, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=312, c2_number=172,
                    league="Hardcore Legacy", name="Washer", time=datetime.datetime(2016, 12, 5, 0, 21, 41)))
db.session.add(
    Post(uid=156, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=25, c2_number=30, league="Hardcore Legacy",
         name="Gas Man", time=datetime.datetime(2016, 11, 21, 12, 31, 28)))
db.session.add(Post(uid=157, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=211, c2_number=317,
                    league="Hardcore Legacy", name="Night Train", time=datetime.datetime(2016, 8, 9, 22, 44, 20)))
db.session.add(
    Post(uid=158, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=291, c2_number=43, league="Hardcore Legacy",
         name="Waylay Dave", time=datetime.datetime(2016, 10, 11, 0, 14, 19)))
db.session.add(Post(uid=159, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=304, c2_number=54,
                    league="Hardcore Legacy", name="Glyph", time=datetime.datetime(2016, 6, 21, 6, 47, 20)))
db.session.add(
    Post(uid=160, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=219, c2_number=254, league="Hardcore Legacy",
         name="Old Man Winter", time=datetime.datetime(2016, 1, 11, 22, 15, 53)))
db.session.add(
    Post(uid=161, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=91, c2_number=57, league="Hardcore Legacy",
         name="Wheels", time=datetime.datetime(2016, 1, 27, 0, 2, 4)))
db.session.add(Post(uid=162, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=127, c2_number=168,
                    league="Hardcore Legacy", name="Grave Digger", time=datetime.datetime(2016, 12, 14, 7, 12, 16)))
db.session.add(
    Post(uid=163, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=235, c2_number=289, league="Hardcore Legacy",
         name="Old Orange Eyes", time=datetime.datetime(2016, 11, 27, 21, 22, 55)))
db.session.add(Post(uid=164, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=156, c2_number=174,
                    league="Hardcore Legacy", name="Wooden Man", time=datetime.datetime(2016, 6, 14, 19, 4, 32)))
db.session.add(
    Post(uid=165, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=81, c2_number=202,
         league="Hardcore Legacy", name="Guillotine", time=datetime.datetime(2016, 11, 18, 18, 19, 37)))
db.session.add(Post(uid=166, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=232, c2_number=133,
                    league="Hardcore Legacy", name="Old Regret", time=datetime.datetime(2016, 10, 17, 22, 46, 46)))
db.session.add(Post(uid=167, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=49, c2_number=190,
                    league="Hardcore Legacy", name="Woo Woo", time=datetime.datetime(2016, 11, 14, 18, 38, 44)))
db.session.add(Post(uid=168, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=70, c2_number=245,
                    league="Hardcore Legacy", name="Gunhawk", time=datetime.datetime(2016, 6, 15, 0, 34, 39)))
db.session.add(Post(uid=169, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=52, c2_number=34,
                    league="Hardcore Legacy", name="Onion King", time=datetime.datetime(2016, 8, 13, 21, 41, 46)))
db.session.add(Post(uid=170, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=136, c2_number=201,
                    league="Hardcore Legacy", name="Yellow Menace", time=datetime.datetime(2016, 2, 26, 0, 41, 3)))
db.session.add(Post(uid=171, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=194, c2_number=161,
                    league="Hardcore Legacy", name="High Kingdom Warrior",
                    time=datetime.datetime(2016, 9, 8, 8, 55, 29)))
db.session.add(Post(uid=172, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=65, c2_number=230,
                    league="Hardcore Legacy", name="Osprey", time=datetime.datetime(2016, 6, 7, 9, 46, 22)))
db.session.add(Post(uid=173, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=96, c2_number=243,
                    league="Hardcore Legacy", name="Zero Charisma", time=datetime.datetime(2016, 7, 4, 17, 19, 0)))
db.session.add(Post(uid=174, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=23, c2_number=239,
                    league="Hardcore Legacy", name="Highlander Monk", time=datetime.datetime(2016, 2, 8, 10, 29, 51)))
db.session.add(Post(uid=175, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=228, c2_number=180,
                    league="Hardcore Legacy", name="Overrun", time=datetime.datetime(2016, 11, 17, 0, 52, 5)))
db.session.add(Post(uid=176, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=44, c2_number=252,
                    league="Hardcore Legacy", name="Zesty Dragon", time=datetime.datetime(2016, 10, 21, 17, 32, 43)))
db.session.add(Post(uid=177, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=303, c2_number=187,
                    league="Hardcore Legacy", name="Zod", time=datetime.datetime(2016, 9, 26, 15, 47, 1)))
db.session.add(Post(uid=0, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=102, c2_number=81,
                    league="Hardcore Legacy", name="101", time=datetime.datetime(2016, 9, 14, 8, 17, 45)))
db.session.add(Post(uid=1, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=232, c2_number=45,
                    league="Hardcore Legacy", name="Houston", time=datetime.datetime(2016, 12, 24, 4, 56, 54)))
db.session.add(Post(uid=2, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=112, c2_number=298,
                    league="Hardcore Legacy", name="Pinball Wizard", time=datetime.datetime(2016, 12, 13, 14, 49, 28)))
db.session.add(Post(uid=3, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=110, c2_number=176,
                    league="Hardcore Legacy", name="Accidental Genius", time=datetime.datetime(2016, 8, 8, 7, 37, 20)))
db.session.add(
    Post(uid=4, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=198, c2_number=85, league="Hardcore Legacy",
         name="Hyper", time=datetime.datetime(2016, 9, 16, 11, 23, 20)))
db.session.add(Post(uid=5, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=297, c2_number=187,
                    league="Hardcore Legacy", name="Pluto", time=datetime.datetime(2016, 4, 14, 11, 8, 36)))
db.session.add(
    Post(uid=6, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=124, c2_number=250, league="Hardcore Legacy",
         name="Alpha", time=datetime.datetime(2016, 8, 14, 4, 41, 51)))
db.session.add(
    Post(uid=7, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=272, c2_number=211, league="Hardcore Legacy",
         name="Jester", time=datetime.datetime(2016, 4, 23, 15, 40, 22)))
db.session.add(
    Post(uid=8, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=35, c2_number=237, league="Hardcore Legacy",
         name="Pogue", time=datetime.datetime(2016, 12, 1, 0, 34, 2)))
db.session.add(
    Post(uid=9, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=166, c2_number=39, league="Hardcore Legacy",
         name="Airport Hobo", time=datetime.datetime(2016, 6, 14, 0, 51, 55)))
db.session.add(Post(uid=10, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=243, c2_number=179,
                    league="Hardcore Legacy", name="Jigsaw", time=datetime.datetime(2016, 8, 26, 19, 26, 28)))
db.session.add(
    Post(uid=11, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=134, c2_number=80, league="Hardcore Legacy",
         name="Prometheus", time=datetime.datetime(2016, 4, 22, 7, 54, 26)))
db.session.add(
    Post(uid=12, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=105, c2_number=241, league="Hardcore Legacy",
         name="Bearded Angler", time=datetime.datetime(2016, 1, 25, 18, 43, 32)))
db.session.add(Post(uid=13, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=262, c2_number=207,
                    league="Hardcore Legacy", name="Joker's Grin", time=datetime.datetime(2016, 9, 25, 10, 27, 5)))
db.session.add(
    Post(uid=14, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=37, c2_number=270, league="Hardcore Legacy",
         name="Psycho Thinker", time=datetime.datetime(2016, 8, 24, 3, 24, 29)))
db.session.add(
    Post(uid=15, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=25, c2_number=151, league="Hardcore Legacy",
         name="Beetle King", time=datetime.datetime(2016, 4, 11, 15, 23, 43)))
db.session.add(
    Post(uid=16, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=23, c2_number=57, league="Hardcore Legacy",
         name="Judge", time=datetime.datetime(2016, 4, 21, 3, 53, 41)))
db.session.add(
    Post(uid=17, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=127, c2_number=82, league="Hardcore Legacy",
         name="Pusher", time=datetime.datetime(2016, 8, 13, 5, 10, 46)))
db.session.add(
    Post(uid=18, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=244, c2_number=88, league="Hardcore Legacy",
         name="Bitmap", time=datetime.datetime(2016, 2, 4, 19, 24, 47)))
db.session.add(
    Post(uid=19, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=87, c2_number=135, league="Hardcore Legacy",
         name="Junkyard Dog", time=datetime.datetime(2016, 6, 6, 16, 24, 17)))
db.session.add(
    Post(uid=20, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=128, c2_number=228, league="Hardcore Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 7, 5, 22, 35, 0)))
db.session.add(
    Post(uid=21, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=210, c2_number=65, league="Hardcore Legacy",
         name="Blister", time=datetime.datetime(2016, 3, 7, 4, 6, 13)))
db.session.add(
    Post(uid=22, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=234, c2_number=97, league="Hardcore Legacy",
         name="K-9", time=datetime.datetime(2016, 4, 15, 12, 27, 8)))
db.session.add(Post(uid=23, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=116, c2_number=26,
                    league="Hardcore Legacy", name="Roadblock", time=datetime.datetime(2016, 11, 17, 3, 21, 39)))
db.session.add(
    Post(uid=24, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=225, c2_number=102, league="Hardcore Legacy",
         name="Bowie", time=datetime.datetime(2016, 5, 11, 12, 39, 47)))
db.session.add(Post(uid=25, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=227, c2_number=60,
                    league="Hardcore Legacy", name="Keystone", time=datetime.datetime(2016, 1, 26, 15, 1, 58)))
db.session.add(
    Post(uid=26, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=249, c2_number=297, league="Hardcore Legacy",
         name="Rooster", time=datetime.datetime(2016, 2, 22, 11, 19, 10)))
db.session.add(
    Post(uid=27, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=227, c2_number=75, league="Hardcore Legacy",
         name="Bowler", time=datetime.datetime(2016, 1, 16, 12, 32, 31)))
db.session.add(Post(uid=28, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=145, c2_number=73,
                    league="Hardcore Legacy", name="Kickstart", time=datetime.datetime(2016, 8, 23, 7, 33, 15)))
db.session.add(Post(uid=29, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=215, c2_number=290,
                    league="Hardcore Legacy", name="Sandbox", time=datetime.datetime(2016, 3, 18, 18, 6, 56)))
db.session.add(Post(uid=30, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=207, c2_number=284,
                    league="Hardcore Legacy", name="Breadmaker", time=datetime.datetime(2016, 11, 9, 15, 47, 17)))
db.session.add(Post(uid=31, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=118, c2_number=78,
                    league="Hardcore Legacy", name="Kill Switch", time=datetime.datetime(2016, 11, 28, 1, 44, 31)))
db.session.add(Post(uid=32, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=200, c2_number=49,
                    league="Hardcore Legacy", name="Scrapper", time=datetime.datetime(2016, 3, 15, 16, 21, 2)))
db.session.add(Post(uid=33, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=53, c2_number=263,
                    league="Hardcore Legacy", name="Broomspun", time=datetime.datetime(2016, 7, 26, 1, 37, 24)))
db.session.add(Post(uid=34, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=46, c2_number=310,
                    league="Hardcore Legacy", name="Kingfisher", time=datetime.datetime(2016, 4, 14, 4, 20, 58)))
db.session.add(Post(uid=35, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=122, c2_number=100,
                    league="Hardcore Legacy", name="Screwtape", time=datetime.datetime(2016, 4, 13, 7, 13, 58)))
db.session.add(
    Post(uid=36, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=270, c2_number=98, league="Hardcore Legacy",
         name="Buckshot", time=datetime.datetime(2016, 11, 20, 6, 9, 46)))
db.session.add(
    Post(uid=37, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=128, c2_number=285, league="Hardcore Legacy",
         name="Kitchen", time=datetime.datetime(2016, 3, 19, 0, 11, 40)))
db.session.add(Post(uid=38, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=236, c2_number=24,
                    league="Hardcore Legacy", name="Sexual Chocolate", time=datetime.datetime(2016, 7, 25, 5, 21, 39)))
db.session.add(
    Post(uid=39, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=64, c2_number=176, league="Hardcore Legacy",
         name="Bugger", time=datetime.datetime(2016, 1, 24, 7, 52, 52)))
db.session.add(
    Post(uid=40, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=47, c2_number=81, league="Hardcore Legacy",
         name="Knuckles", time=datetime.datetime(2016, 9, 8, 12, 15, 12)))
db.session.add(Post(uid=41, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=225, c2_number=120,
                    league="Hardcore Legacy", name="Shadow Chaser", time=datetime.datetime(2016, 10, 5, 1, 17, 5)))
db.session.add(
    Post(uid=42, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=294, c2_number=30, league="Hardcore Legacy",
         name="Cabbie", time=datetime.datetime(2016, 6, 6, 11, 36, 36)))
db.session.add(
    Post(uid=43, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=78, c2_number=293, league="Hardcore Legacy",
         name="Lady Killer", time=datetime.datetime(2016, 1, 14, 18, 49, 3)))
db.session.add(
    Post(uid=44, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=115, c2_number=76, league="Hardcore Legacy",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 2, 16, 7, 34, 25)))
db.session.add(
    Post(uid=45, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=35, c2_number=139, league="Hardcore Legacy",
         name="Candy Butcher", time=datetime.datetime(2016, 10, 14, 0, 16, 1)))
db.session.add(Post(uid=46, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=109, c2_number=86,
                    league="Hardcore Legacy", name="Liquid Science", time=datetime.datetime(2016, 10, 26, 22, 11, 12)))
db.session.add(
    Post(uid=47, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=303, c2_number=251, league="Hardcore Legacy",
         name="Shooter", time=datetime.datetime(2016, 10, 8, 17, 38, 13)))
db.session.add(
    Post(uid=48, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=255, c2_number=289, league="Hardcore Legacy",
         name="Capital F", time=datetime.datetime(2016, 5, 21, 8, 15, 26)))
db.session.add(Post(uid=49, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=242, c2_number=126,
                    league="Hardcore Legacy", name="Little Cobra", time=datetime.datetime(2016, 6, 13, 17, 20, 16)))
db.session.add(
    Post(uid=50, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=157, c2_number=89, league="Hardcore Legacy",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 10, 28, 18, 39, 17)))
db.session.add(
    Post(uid=51, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=306, c2_number=155, league="Hardcore Legacy",
         name="Captain Peroxide", time=datetime.datetime(2016, 6, 10, 20, 8, 50)))
db.session.add(
    Post(uid=52, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=106, c2_number=169, league="Hardcore Legacy",
         name="Little General", time=datetime.datetime(2016, 12, 24, 18, 47, 35)))
db.session.add(Post(uid=53, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=141, c2_number=219,
                    league="Hardcore Legacy", name="Skull Crusher", time=datetime.datetime(2016, 4, 24, 5, 44, 38)))
db.session.add(
    Post(uid=54, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=155, c2_number=203, league="Hardcore Legacy",
         name="Celtic Charger", time=datetime.datetime(2016, 3, 21, 4, 21, 15)))
db.session.add(
    Post(uid=55, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=248, c2_number=120, league="Hardcore Legacy",
         name="Lord Nikon", time=datetime.datetime(2016, 1, 20, 21, 17, 20)))
db.session.add(
    Post(uid=56, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=192, c2_number=252, league="Hardcore Legacy",
         name="Sky Bully", time=datetime.datetime(2016, 1, 13, 8, 10, 45)))
db.session.add(
    Post(uid=57, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=116, c2_number=218, league="Hardcore Legacy",
         name="Cereal Killer", time=datetime.datetime(2016, 8, 2, 7, 33, 33)))
db.session.add(
    Post(uid=58, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=318, c2_number=36, league="Hardcore Legacy",
         name="Lord Pistachio", time=datetime.datetime(2016, 8, 23, 12, 33, 11)))
db.session.add(Post(uid=59, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=101, c2_number=278,
                    league="Hardcore Legacy", name="Slow Trot", time=datetime.datetime(2016, 1, 23, 1, 40, 48)))
db.session.add(
    Post(uid=60, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=21, c2_number=153, league="Hardcore Legacy",
         name="Chicago Blackout", time=datetime.datetime(2016, 12, 8, 13, 0, 31)))
db.session.add(
    Post(uid=61, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=127, c2_number=278, league="Hardcore Legacy",
         name="Mad Irishman", time=datetime.datetime(2016, 10, 2, 18, 22, 15)))
db.session.add(
    Post(uid=62, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=101, c2_number=183, league="Hardcore Legacy",
         name="Snake Eyes", time=datetime.datetime(2016, 7, 19, 10, 23, 8)))
db.session.add(
    Post(uid=63, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=76, c2_number=128, league="Hardcore Legacy",
         name="Chocolate Thunder", time=datetime.datetime(2016, 5, 1, 10, 21, 42)))
db.session.add(Post(uid=64, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=89, c2_number=114,
                    league="Hardcore Legacy", name="Mad Jack", time=datetime.datetime(2016, 9, 18, 15, 33, 45)))
db.session.add(Post(uid=65, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=175, c2_number=264,
                    league="Hardcore Legacy", name="Snow Hound", time=datetime.datetime(2016, 11, 21, 22, 40, 12)))
db.session.add(
    Post(uid=66, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=23, c2_number=118, league="Hardcore Legacy",
         name="Chuckles", time=datetime.datetime(2016, 2, 10, 6, 30, 31)))
db.session.add(Post(uid=67, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=283, c2_number=91,
                    league="Hardcore Legacy", name="Mad Rascal", time=datetime.datetime(2016, 4, 16, 1, 29, 14)))
db.session.add(
    Post(uid=68, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=226, c2_number=85, league="Hardcore Legacy",
         name="Sofa King", time=datetime.datetime(2016, 8, 27, 9, 7, 51)))
db.session.add(
    Post(uid=69, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=176, c2_number=140, league="Hardcore Legacy",
         name="Commando", time=datetime.datetime(2016, 9, 18, 19, 23, 40)))
db.session.add(
    Post(uid=70, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=37, c2_number=257, league="Hardcore Legacy",
         name="Manimal", time=datetime.datetime(2016, 7, 7, 1, 25, 41)))
db.session.add(Post(uid=71, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=306, c2_number=229,
                    league="Hardcore Legacy", name="Speedwell", time=datetime.datetime(2016, 7, 24, 11, 35, 51)))
db.session.add(
    Post(uid=72, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=290, c2_number=83, league="Hardcore Legacy",
         name="Cool Whip", time=datetime.datetime(2016, 11, 3, 20, 55, 43)))
db.session.add(
    Post(uid=73, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=69, c2_number=299, league="Hardcore Legacy",
         name="Marbles", time=datetime.datetime(2016, 9, 21, 22, 48, 43)))
db.session.add(
    Post(uid=74, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=272, c2_number=89, league="Hardcore Legacy",
         name="Spider Fuji", time=datetime.datetime(2016, 4, 25, 21, 5, 20)))
db.session.add(
    Post(uid=75, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=202, c2_number=159, league="Hardcore Legacy",
         name="Cosmo", time=datetime.datetime(2016, 1, 7, 4, 57, 31)))
db.session.add(Post(uid=76, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=46, c2_number=259,
                    league="Hardcore Legacy", name="Married Man", time=datetime.datetime(2016, 1, 21, 14, 40, 46)))
db.session.add(Post(uid=77, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=271, c2_number=244,
                    league="Hardcore Legacy", name="Springheel Jack", time=datetime.datetime(2016, 8, 22, 17, 58, 47)))
db.session.add(Post(uid=78, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=33, c2_number=198,
                    league="Hardcore Legacy", name="Crash Override", time=datetime.datetime(2016, 10, 10, 9, 55, 41)))
db.session.add(Post(uid=79, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=165, c2_number=275,
                    league="Hardcore Legacy", name="Marshmallow", time=datetime.datetime(2016, 2, 28, 13, 58, 23)))
db.session.add(Post(uid=80, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=72, c2_number=100,
                    league="Hardcore Legacy", name="Squatch", time=datetime.datetime(2016, 11, 13, 10, 46, 34)))
db.session.add(Post(uid=81, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=216, c2_number=287,
                    league="Hardcore Legacy", name="Crash Test", time=datetime.datetime(2016, 11, 17, 9, 22, 43)))
db.session.add(Post(uid=82, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=162, c2_number=29,
                    league="Hardcore Legacy", name="Mental", time=datetime.datetime(2016, 6, 23, 11, 33, 45)))
db.session.add(Post(uid=83, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=216, c2_number=136,
                    league="Hardcore Legacy", name="Stacker of Wheat", time=datetime.datetime(2016, 9, 22, 11, 22, 26)))
db.session.add(Post(uid=84, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=88, c2_number=177,
                    league="Hardcore Legacy", name="Crazy Eights", time=datetime.datetime(2016, 11, 17, 13, 30, 9)))
db.session.add(Post(uid=85, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=116, c2_number=85,
                    league="Hardcore Legacy", name="Mercury Reborn", time=datetime.datetime(2016, 9, 11, 3, 31, 43)))
db.session.add(Post(uid=86, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=164, c2_number=89,
                    league="Hardcore Legacy", name="Sugar Man", time=datetime.datetime(2016, 3, 15, 8, 50, 7)))
db.session.add(Post(uid=87, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=308, c2_number=177,
                    league="Hardcore Legacy", name="Criss Cross", time=datetime.datetime(2016, 12, 10, 2, 22, 13)))
db.session.add(Post(uid=88, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=163, c2_number=71,
                    league="Hardcore Legacy", name="Midas", time=datetime.datetime(2016, 10, 4, 21, 51, 1)))
db.session.add(Post(uid=89, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=281, c2_number=214,
                    league="Hardcore Legacy", name="Suicide Jockey", time=datetime.datetime(2016, 1, 23, 22, 35, 14)))
db.session.add(Post(uid=90, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=133, c2_number=71,
                    league="Hardcore Legacy", name="Cross Thread", time=datetime.datetime(2016, 1, 9, 16, 42, 9)))
db.session.add(
    Post(uid=91, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=198, c2_number=65, league="Hardcore Legacy",
         name="Midnight Rambler", time=datetime.datetime(2016, 3, 18, 2, 33, 35)))
db.session.add(Post(uid=92, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=97, c2_number=208,
                    league="Hardcore Legacy", name="Swampmasher", time=datetime.datetime(2016, 9, 2, 19, 48, 34)))
db.session.add(Post(uid=93, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=312, c2_number=162,
                    league="Hardcore Legacy", name="Cujo", time=datetime.datetime(2016, 4, 17, 16, 12, 23)))
db.session.add(
    Post(uid=94, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=33, c2_number=294, league="Hardcore Legacy",
         name="Midnight Rider", time=datetime.datetime(2016, 8, 17, 10, 46, 45)))
db.session.add(Post(uid=95, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=180, c2_number=173,
                    league="Hardcore Legacy", name="Swerve", time=datetime.datetime(2016, 5, 9, 20, 16, 15)))
db.session.add(
    Post(uid=96, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=308, c2_number=164, league="Hardcore Legacy",
         name="Dancing Madman", time=datetime.datetime(2016, 4, 27, 11, 49, 21)))
db.session.add(Post(uid=97, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=162, c2_number=139,
                    league="Hardcore Legacy", name="Mindless Bobcat", time=datetime.datetime(2016, 7, 16, 6, 32, 13)))
db.session.add(
    Post(uid=98, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=190, c2_number=257, league="Hardcore Legacy",
         name="Tacklebox", time=datetime.datetime(2016, 12, 12, 20, 21, 36)))
db.session.add(Post(uid=99, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=317, c2_number=217,
                    league="Hardcore Legacy", name="Dangle", time=datetime.datetime(2016, 7, 21, 6, 14, 55)))
db.session.add(Post(uid=100, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=218, c2_number=121,
                    league="Hardcore Legacy", name="Mr. 44", time=datetime.datetime(2016, 10, 14, 18, 38, 17)))
db.session.add(Post(uid=101, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=117, c2_number=220,
                    league="Hardcore Legacy", name="Take Away", time=datetime.datetime(2016, 11, 16, 18, 40, 30)))
db.session.add(Post(uid=102, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=277, c2_number=81,
                    league="Hardcore Legacy", name="Dark Horse", time=datetime.datetime(2016, 1, 10, 18, 11, 40)))
db.session.add(Post(uid=103, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=198, c2_number=313,
                    league="Hardcore Legacy", name="Mr. Fabulous", time=datetime.datetime(2016, 9, 11, 14, 41, 36)))
db.session.add(Post(uid=104, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=65, c2_number=182,
                    league="Hardcore Legacy", name="Tan Stallion", time=datetime.datetime(2016, 8, 19, 5, 41, 26)))
db.session.add(Post(uid=105, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=33, c2_number=252,
                    league="Hardcore Legacy", name="Day Hawk", time=datetime.datetime(2016, 1, 28, 11, 38, 3)))
db.session.add(Post(uid=106, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=95, c2_number=279,
                    league="Hardcore Legacy", name="Mr. Gadget", time=datetime.datetime(2016, 5, 7, 13, 20, 14)))
db.session.add(Post(uid=107, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=218, c2_number=89,
                    league="Hardcore Legacy", name="The China Wall", time=datetime.datetime(2016, 3, 16, 10, 30, 53)))
db.session.add(
    Post(uid=108, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=107, c2_number=130, league="Hardcore Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 10, 22, 13, 4, 8)))
db.session.add(
    Post(uid=109, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=57, c2_number=165, league="Hardcore Legacy",
         name="Mr. Lucky", time=datetime.datetime(2016, 7, 28, 15, 7, 32)))
db.session.add(Post(uid=110, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=233, c2_number=98,
                    league="Hardcore Legacy", name="The Dude", time=datetime.datetime(2016, 7, 6, 4, 51, 16)))
db.session.add(Post(uid=111, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=118, c2_number=134,
                    league="Hardcore Legacy", name="Digger", time=datetime.datetime(2016, 6, 8, 15, 20, 51)))
db.session.add(Post(uid=112, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=22, c2_number=101,
                    league="Hardcore Legacy", name="Mr. Peppermint", time=datetime.datetime(2016, 7, 18, 3, 13, 45)))
db.session.add(Post(uid=113, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=272, c2_number=118,
                    league="Hardcore Legacy", name="The Flying Mouse", time=datetime.datetime(2016, 1, 8, 1, 41, 41)))
db.session.add(
    Post(uid=114, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=245, c2_number=164, league="Hardcore Legacy",
         name="Disco Thunder", time=datetime.datetime(2016, 7, 3, 1, 31, 36)))
db.session.add(Post(uid=115, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=281, c2_number=297,
                    league="Hardcore Legacy", name="Mr. Spy", time=datetime.datetime(2016, 4, 27, 8, 18, 36)))
db.session.add(Post(uid=116, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=287, c2_number=263,
                    league="Hardcore Legacy", name="The Happy Jock", time=datetime.datetime(2016, 11, 11, 17, 3, 25)))
db.session.add(Post(uid=117, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=59, c2_number=169,
                    league="Hardcore Legacy", name="Disco Potato", time=datetime.datetime(2016, 9, 2, 4, 45, 15)))
db.session.add(Post(uid=118, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=65, c2_number=197,
                    league="Hardcore Legacy", name="Mr. Thanksgiving", time=datetime.datetime(2016, 12, 16, 15, 8, 13)))
db.session.add(Post(uid=119, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=310, c2_number=193,
                    league="Hardcore Legacy", name="The Howling Swede", time=datetime.datetime(2016, 7, 1, 22, 21, 5)))
db.session.add(Post(uid=120, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=77, c2_number=24,
                    league="Hardcore Legacy", name="Dr. Cocktail", time=datetime.datetime(2016, 3, 8, 7, 0, 51)))
db.session.add(Post(uid=121, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=56, c2_number=303,
                    league="Hardcore Legacy", name="Mr. Wholesome", time=datetime.datetime(2016, 10, 17, 15, 4, 39)))
db.session.add(Post(uid=122, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=193, c2_number=319,
                    league="Hardcore Legacy", name="Thrasher", time=datetime.datetime(2016, 5, 4, 0, 32, 19)))
db.session.add(Post(uid=123, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=38, c2_number=61,
                    league="Hardcore Legacy", name="Dredd", time=datetime.datetime(2016, 6, 11, 3, 36, 13)))
db.session.add(Post(uid=124, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=60, c2_number=247,
                    league="Hardcore Legacy", name="Mud Pie Man", time=datetime.datetime(2016, 4, 14, 1, 27, 53)))
db.session.add(Post(uid=125, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=42, c2_number=198,
                    league="Hardcore Legacy", name="Toe", time=datetime.datetime(2016, 10, 21, 8, 37, 42)))
db.session.add(
    Post(uid=126, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=192, c2_number=58, league="Hardcore Legacy",
         name="Dropkick", time=datetime.datetime(2016, 9, 5, 7, 44, 32)))
db.session.add(
    Post(uid=127, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=148, c2_number=290, league="Hardcore Legacy",
         name="Mule Skinner", time=datetime.datetime(2016, 3, 24, 18, 29, 49)))
db.session.add(Post(uid=128, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=219, c2_number=271,
                    league="Hardcore Legacy", name="Toolmaker", time=datetime.datetime(2016, 6, 4, 13, 44, 25)))
db.session.add(Post(uid=129, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=127, c2_number=29,
                    league="Hardcore Legacy", name="Drop Stone", time=datetime.datetime(2016, 1, 6, 10, 49, 16)))
db.session.add(Post(uid=130, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=268, c2_number=51,
                    league="Hardcore Legacy", name="Murmur", time=datetime.datetime(2016, 8, 11, 5, 51, 5)))
db.session.add(Post(uid=131, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=281, c2_number=139,
                    league="Hardcore Legacy", name="Tough Nut", time=datetime.datetime(2016, 4, 5, 1, 12, 17)))
db.session.add(Post(uid=132, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=130, c2_number=90,
                    league="Hardcore Legacy", name="Drugstore Cowboy", time=datetime.datetime(2016, 8, 17, 4, 12, 35)))
db.session.add(Post(uid=133, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=80, c2_number=150,
                    league="Hardcore Legacy", name="Nacho", time=datetime.datetime(2016, 4, 11, 12, 22, 11)))
db.session.add(Post(uid=134, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=176, c2_number=259,
                    league="Hardcore Legacy", name="Trip", time=datetime.datetime(2016, 2, 24, 4, 2, 17)))
db.session.add(Post(uid=135, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=99, c2_number=86,
                    league="Hardcore Legacy", name="Easy Sweep", time=datetime.datetime(2016, 10, 12, 9, 23, 1)))
db.session.add(Post(uid=136, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=297, c2_number=29,
                    league="Hardcore Legacy", name="Natural Mess", time=datetime.datetime(2016, 12, 24, 9, 10, 38)))
db.session.add(Post(uid=137, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=242, c2_number=179,
                    league="Hardcore Legacy", name="Troubadour", time=datetime.datetime(2016, 8, 18, 3, 25, 1)))
db.session.add(Post(uid=138, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=105, c2_number=312,
                    league="Hardcore Legacy", name="Electric Player", time=datetime.datetime(2016, 12, 14, 6, 35, 18)))
db.session.add(Post(uid=139, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=191, c2_number=175,
                    league="Hardcore Legacy", name="Necromancer", time=datetime.datetime(2016, 1, 1, 4, 50, 48)))
db.session.add(Post(uid=140, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=168, c2_number=89,
                    league="Hardcore Legacy", name="Turnip King", time=datetime.datetime(2016, 10, 28, 4, 36, 4)))
db.session.add(Post(uid=141, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=309, c2_number=53,
                    league="Hardcore Legacy", name="Esquire", time=datetime.datetime(2016, 9, 8, 17, 7, 0)))
db.session.add(Post(uid=142, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=248, c2_number=293,
                    league="Hardcore Legacy", name="Neophyte Believer", time=datetime.datetime(2016, 10, 26, 6, 7, 54)))
db.session.add(Post(uid=143, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=54, c2_number=97,
                    league="Hardcore Legacy", name="Twitch", time=datetime.datetime(2016, 2, 11, 7, 13, 26)))
db.session.add(Post(uid=144, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=170, c2_number=221,
                    league="Hardcore Legacy", name="Fast Draw", time=datetime.datetime(2016, 12, 7, 19, 28, 56)))
db.session.add(Post(uid=145, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=262, c2_number=55,
                    league="Hardcore Legacy", name="Nessie", time=datetime.datetime(2016, 2, 24, 7, 33, 18)))
db.session.add(Post(uid=146, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=288, c2_number=38,
                    league="Hardcore Legacy", name="Vagabond Warrior", time=datetime.datetime(2016, 12, 6, 6, 14, 56)))
db.session.add(Post(uid=147, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=66, c2_number=160,
                    league="Hardcore Legacy", name="Flakes", time=datetime.datetime(2016, 11, 5, 13, 16, 13)))
db.session.add(Post(uid=148, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=252, c2_number=279,
                    league="Hardcore Legacy", name="New Cycle", time=datetime.datetime(2016, 2, 10, 13, 44, 14)))
db.session.add(Post(uid=149, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=261, c2_number=181,
                    league="Hardcore Legacy", name="Voluntary", time=datetime.datetime(2016, 5, 23, 9, 48, 23)))
db.session.add(
    Post(uid=150, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=289, c2_number=30, league="Hardcore Legacy",
         name="Flint", time=datetime.datetime(2016, 6, 26, 7, 7, 8)))
db.session.add(Post(uid=151, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=48, c2_number=234,
                    league="Hardcore Legacy", name="Nickname Master", time=datetime.datetime(2016, 11, 27, 17, 9, 33)))
db.session.add(
    Post(uid=152, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=177, c2_number=171, league="Hardcore Legacy",
         name="Vortex", time=datetime.datetime(2016, 3, 4, 2, 18, 57)))
db.session.add(
    Post(uid=153, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=60, c2_number=77, league="Hardcore Legacy",
         name="Freak", time=datetime.datetime(2016, 11, 21, 17, 26, 32)))
db.session.add(Post(uid=154, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=178, c2_number=94,
                    league="Hardcore Legacy", name="Nightmare King", time=datetime.datetime(2016, 1, 3, 2, 57, 52)))
db.session.add(Post(uid=155, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=223, c2_number=220,
                    league="Hardcore Legacy", name="Washer", time=datetime.datetime(2016, 7, 14, 10, 29, 36)))
db.session.add(Post(uid=156, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=157, c2_number=36,
                    league="Hardcore Legacy", name="Gas Man", time=datetime.datetime(2016, 2, 1, 13, 47, 0)))
db.session.add(Post(uid=157, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=45, c2_number=92,
                    league="Hardcore Legacy", name="Night Train", time=datetime.datetime(2016, 10, 19, 4, 37, 58)))
db.session.add(Post(uid=158, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=179, c2_number=76,
                    league="Hardcore Legacy", name="Waylay Dave", time=datetime.datetime(2016, 11, 27, 17, 33, 55)))
db.session.add(Post(uid=159, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=262, c2_number=304,
                    league="Hardcore Legacy", name="Glyph", time=datetime.datetime(2016, 1, 13, 16, 13, 35)))
db.session.add(Post(uid=160, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=163, c2_number=172,
                    league="Hardcore Legacy", name="Old Man Winter", time=datetime.datetime(2016, 12, 27, 18, 30, 27)))
db.session.add(Post(uid=161, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=124, c2_number=158,
                    league="Hardcore Legacy", name="Wheels", time=datetime.datetime(2016, 2, 11, 14, 17, 24)))
db.session.add(
    Post(uid=162, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=60, c2_number=130, league="Hardcore Legacy",
         name="Grave Digger", time=datetime.datetime(2016, 1, 11, 19, 31, 16)))
db.session.add(
    Post(uid=163, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=221, c2_number=197, league="Hardcore Legacy",
         name="Old Orange Eyes", time=datetime.datetime(2016, 2, 28, 14, 10, 52)))
db.session.add(Post(uid=164, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=163, c2_number=73,
                    league="Hardcore Legacy", name="Wooden Man", time=datetime.datetime(2016, 1, 23, 0, 15, 11)))
db.session.add(Post(uid=165, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=190, c2_number=181,
                    league="Hardcore Legacy", name="Guillotine", time=datetime.datetime(2016, 12, 6, 11, 10, 24)))
db.session.add(Post(uid=166, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=108, c2_number=165,
                    league="Hardcore Legacy", name="Old Regret", time=datetime.datetime(2016, 4, 13, 3, 38, 0)))
db.session.add(Post(uid=167, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=290, c2_number=98,
                    league="Hardcore Legacy", name="Woo Woo", time=datetime.datetime(2016, 8, 6, 8, 27, 7)))
db.session.add(
    Post(uid=168, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=158, c2_number=283, league="Hardcore Legacy",
         name="Gunhawk", time=datetime.datetime(2016, 7, 24, 17, 29, 29)))
db.session.add(Post(uid=169, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=20, c2_number=100,
                    league="Hardcore Legacy", name="Onion King", time=datetime.datetime(2016, 7, 23, 13, 48, 57)))
db.session.add(
    Post(uid=170, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=245, c2_number=124, league="Hardcore Legacy",
         name="Yellow Menace", time=datetime.datetime(2016, 11, 27, 22, 37, 37)))
db.session.add(Post(uid=171, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=215, c2_number=259,
                    league="Hardcore Legacy", name="High Kingdom Warrior",
                    time=datetime.datetime(2016, 6, 25, 7, 6, 34)))
db.session.add(Post(uid=172, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=223, c2_number=202,
                    league="Hardcore Legacy", name="Osprey", time=datetime.datetime(2016, 7, 7, 20, 14, 42)))
db.session.add(Post(uid=173, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=41, c2_number=107,
                    league="Hardcore Legacy", name="Zero Charisma", time=datetime.datetime(2016, 1, 27, 10, 49, 5)))
db.session.add(Post(uid=174, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=90, c2_number=209,
                    league="Hardcore Legacy", name="Highlander Monk", time=datetime.datetime(2016, 9, 10, 3, 56, 43)))
db.session.add(Post(uid=175, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=126, c2_number=38,
                    league="Hardcore Legacy", name="Overrun", time=datetime.datetime(2016, 7, 13, 2, 33, 49)))
db.session.add(Post(uid=176, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=187, c2_number=122,
                    league="Hardcore Legacy", name="Zesty Dragon", time=datetime.datetime(2016, 5, 10, 14, 40, 13)))
db.session.add(Post(uid=177, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=307, c2_number=291,
                    league="Hardcore Legacy", name="Zod", time=datetime.datetime(2016, 12, 27, 22, 19, 47)))
db.session.add(Post(uid=0, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=311, c2_number=144,
                    league="Hardcore Legacy", name="101", time=datetime.datetime(2016, 1, 20, 16, 16, 38)))
db.session.add(Post(uid=1, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=32, c2_number=273,
                    league="Hardcore Legacy", name="Houston", time=datetime.datetime(2016, 1, 15, 1, 7, 39)))
db.session.add(
    Post(uid=2, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=103, c2_number=48, league="Hardcore Legacy",
         name="Pinball Wizard", time=datetime.datetime(2016, 7, 2, 8, 4, 40)))
db.session.add(
    Post(uid=3, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=67, c2_number=246, league="Hardcore Legacy",
         name="Accidental Genius", time=datetime.datetime(2016, 8, 24, 10, 10, 16)))
db.session.add(Post(uid=4, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=122, c2_number=272,
                    league="Hardcore Legacy", name="Hyper", time=datetime.datetime(2016, 10, 16, 18, 36, 29)))
db.session.add(
    Post(uid=5, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=303, c2_number=147, league="Hardcore Legacy",
         name="Pluto", time=datetime.datetime(2016, 11, 22, 9, 22, 49)))
db.session.add(
    Post(uid=6, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=61, c2_number=314, league="Hardcore Legacy",
         name="Alpha", time=datetime.datetime(2016, 4, 12, 22, 10, 51)))
db.session.add(Post(uid=7, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=141, c2_number=208,
                    league="Hardcore Legacy", name="Jester", time=datetime.datetime(2016, 11, 12, 11, 23, 15)))
db.session.add(
    Post(uid=8, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=259, c2_number=83, league="Hardcore Legacy",
         name="Pogue", time=datetime.datetime(2016, 11, 14, 16, 48, 44)))
db.session.add(
    Post(uid=9, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=51, c2_number=225, league="Hardcore Legacy",
         name="Airport Hobo", time=datetime.datetime(2016, 6, 5, 2, 53, 34)))
db.session.add(
    Post(uid=10, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=187, c2_number=139, league="Hardcore Legacy",
         name="Jigsaw", time=datetime.datetime(2016, 10, 26, 20, 20, 10)))
db.session.add(
    Post(uid=11, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=309, c2_number=65, league="Hardcore Legacy",
         name="Prometheus", time=datetime.datetime(2016, 10, 14, 7, 32, 0)))
db.session.add(Post(uid=12, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=103, c2_number=41,
                    league="Hardcore Legacy", name="Bearded Angler", time=datetime.datetime(2016, 12, 3, 19, 17, 3)))
db.session.add(Post(uid=13, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=191, c2_number=265,
                    league="Hardcore Legacy", name="Joker's Grin", time=datetime.datetime(2016, 1, 12, 19, 56, 57)))
db.session.add(Post(uid=14, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=83, c2_number=25,
                    league="Hardcore Legacy", name="Psycho Thinker", time=datetime.datetime(2016, 7, 10, 13, 13, 53)))
db.session.add(Post(uid=15, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=212, c2_number=49,
                    league="Hardcore Legacy", name="Beetle King", time=datetime.datetime(2016, 11, 3, 16, 13, 43)))
db.session.add(Post(uid=16, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=34, c2_number=232,
                    league="Hardcore Legacy", name="Judge", time=datetime.datetime(2016, 8, 10, 4, 19, 13)))
db.session.add(Post(uid=17, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=208, c2_number=173,
                    league="Hardcore Legacy", name="Pusher", time=datetime.datetime(2016, 9, 17, 19, 24, 1)))
db.session.add(Post(uid=18, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=302, c2_number=209,
                    league="Hardcore Legacy", name="Bitmap", time=datetime.datetime(2016, 12, 14, 12, 39, 43)))
db.session.add(Post(uid=19, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=199, c2_number=30,
                    league="Hardcore Legacy", name="Junkyard Dog", time=datetime.datetime(2016, 4, 28, 13, 8, 14)))
db.session.add(
    Post(uid=20, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=177, c2_number=239, league="Hardcore Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 8, 10, 5, 23, 8)))
db.session.add(
    Post(uid=21, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=122, c2_number=40, league="Hardcore Legacy",
         name="Blister", time=datetime.datetime(2016, 11, 13, 14, 1, 0)))
db.session.add(
    Post(uid=22, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=63, c2_number=87, league="Hardcore Legacy",
         name="K-9", time=datetime.datetime(2016, 1, 11, 2, 41, 33)))
db.session.add(
    Post(uid=23, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=72, c2_number=141, league="Hardcore Legacy",
         name="Roadblock", time=datetime.datetime(2016, 7, 16, 22, 29, 16)))
db.session.add(Post(uid=24, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=215, c2_number=91,
                    league="Hardcore Legacy", name="Bowie", time=datetime.datetime(2016, 7, 18, 16, 36, 10)))
db.session.add(Post(uid=25, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=162, c2_number=58,
                    league="Hardcore Legacy", name="Keystone", time=datetime.datetime(2016, 2, 20, 0, 13, 35)))
db.session.add(
    Post(uid=26, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=318, c2_number=87, league="Hardcore Legacy",
         name="Rooster", time=datetime.datetime(2016, 3, 6, 10, 7, 44)))
db.session.add(Post(uid=27, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=212, c2_number=187,
                    league="Hardcore Legacy", name="Bowler", time=datetime.datetime(2016, 2, 16, 0, 5, 41)))
db.session.add(
    Post(uid=28, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=182, c2_number=65, league="Hardcore Legacy",
         name="Kickstart", time=datetime.datetime(2016, 4, 13, 1, 9, 29)))
db.session.add(Post(uid=29, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=216, c2_number=251,
                    league="Hardcore Legacy", name="Sandbox", time=datetime.datetime(2016, 7, 27, 22, 0, 29)))
db.session.add(Post(uid=30, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=119, c2_number=289,
                    league="Hardcore Legacy", name="Breadmaker", time=datetime.datetime(2016, 10, 10, 20, 30, 55)))
db.session.add(Post(uid=31, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=288, c2_number=22,
                    league="Hardcore Legacy", name="Kill Switch", time=datetime.datetime(2016, 6, 4, 13, 53, 16)))
db.session.add(Post(uid=32, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=193, c2_number=56,
                    league="Hardcore Legacy", name="Scrapper", time=datetime.datetime(2016, 3, 17, 4, 13, 44)))
db.session.add(Post(uid=33, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=110, c2_number=114,
                    league="Hardcore Legacy", name="Broomspun", time=datetime.datetime(2016, 2, 10, 13, 37, 18)))
db.session.add(Post(uid=34, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=23, c2_number=163,
                    league="Hardcore Legacy", name="Kingfisher", time=datetime.datetime(2016, 4, 10, 19, 5, 32)))
db.session.add(Post(uid=35, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=234, c2_number=82,
                    league="Hardcore Legacy", name="Screwtape", time=datetime.datetime(2016, 3, 13, 14, 36, 52)))
db.session.add(Post(uid=36, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=218, c2_number=176,
                    league="Hardcore Legacy", name="Buckshot", time=datetime.datetime(2016, 8, 19, 7, 55, 7)))
db.session.add(Post(uid=37, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=222, c2_number=247,
                    league="Hardcore Legacy", name="Kitchen", time=datetime.datetime(2016, 2, 24, 12, 4, 36)))
db.session.add(
    Post(uid=38, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=228, c2_number=199, league="Hardcore Legacy",
         name="Sexual Chocolate", time=datetime.datetime(2016, 9, 11, 19, 7, 36)))
db.session.add(
    Post(uid=39, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=104, c2_number=64, league="Hardcore Legacy",
         name="Bugger", time=datetime.datetime(2016, 11, 23, 9, 48, 39)))
db.session.add(Post(uid=40, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=93, c2_number=202,
                    league="Hardcore Legacy", name="Knuckles", time=datetime.datetime(2016, 9, 10, 7, 55, 25)))
db.session.add(Post(uid=41, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=304, c2_number=257,
                    league="Hardcore Legacy", name="Shadow Chaser", time=datetime.datetime(2016, 3, 6, 17, 28, 16)))
db.session.add(
    Post(uid=42, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=68, c2_number=40, league="Hardcore Legacy",
         name="Cabbie", time=datetime.datetime(2016, 6, 20, 12, 36, 27)))
db.session.add(Post(uid=43, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=65, c2_number=211,
                    league="Hardcore Legacy", name="Lady Killer", time=datetime.datetime(2016, 12, 20, 13, 0, 27)))
db.session.add(
    Post(uid=44, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=254, c2_number=58, league="Hardcore Legacy",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 7, 6, 4, 26, 20)))
db.session.add(
    Post(uid=45, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=286, c2_number=108, league="Hardcore Legacy",
         name="Candy Butcher", time=datetime.datetime(2016, 7, 27, 7, 46, 41)))
db.session.add(
    Post(uid=46, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=35, c2_number=38, league="Hardcore Legacy",
         name="Liquid Science", time=datetime.datetime(2016, 11, 21, 22, 22, 24)))
db.session.add(
    Post(uid=47, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=293, c2_number=201, league="Hardcore Legacy",
         name="Shooter", time=datetime.datetime(2016, 1, 11, 7, 3, 8)))
db.session.add(Post(uid=48, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=180, c2_number=69,
                    league="Hardcore Legacy", name="Capital F", time=datetime.datetime(2016, 1, 21, 0, 43, 9)))
db.session.add(
    Post(uid=49, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=141, c2_number=235, league="Hardcore Legacy",
         name="Little Cobra", time=datetime.datetime(2016, 6, 5, 14, 8, 15)))
db.session.add(
    Post(uid=50, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=148, c2_number=36, league="Hardcore Legacy",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 12, 17, 11, 4, 30)))
db.session.add(Post(uid=51, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=82, c2_number=204,
                    league="Hardcore Legacy", name="Captain Peroxide", time=datetime.datetime(2016, 3, 20, 13, 8, 1)))
db.session.add(
    Post(uid=52, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=52, c2_number=318, league="Hardcore Legacy",
         name="Little General", time=datetime.datetime(2016, 3, 27, 18, 57, 8)))
db.session.add(
    Post(uid=53, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=226, c2_number=66, league="Hardcore Legacy",
         name="Skull Crusher", time=datetime.datetime(2016, 7, 8, 2, 17, 49)))
db.session.add(
    Post(uid=54, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=240, c2_number=314, league="Hardcore Legacy",
         name="Celtic Charger", time=datetime.datetime(2016, 1, 25, 19, 10, 38)))
db.session.add(
    Post(uid=55, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=247, c2_number=285, league="Hardcore Legacy",
         name="Lord Nikon", time=datetime.datetime(2016, 1, 18, 17, 14, 20)))
db.session.add(
    Post(uid=56, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=292, c2_number=124, league="Hardcore Legacy",
         name="Sky Bully", time=datetime.datetime(2016, 9, 21, 0, 22, 48)))
db.session.add(
    Post(uid=57, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=115, c2_number=277, league="Hardcore Legacy",
         name="Cereal Killer", time=datetime.datetime(2016, 7, 16, 17, 57, 56)))
db.session.add(
    Post(uid=58, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=259, c2_number=68, league="Hardcore Legacy",
         name="Lord Pistachio", time=datetime.datetime(2016, 4, 16, 22, 22, 23)))
db.session.add(
    Post(uid=59, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=140, c2_number=99, league="Hardcore Legacy",
         name="Slow Trot", time=datetime.datetime(2016, 9, 17, 12, 45, 37)))
db.session.add(
    Post(uid=60, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=170, c2_number=118, league="Hardcore Legacy",
         name="Chicago Blackout", time=datetime.datetime(2016, 7, 25, 6, 51, 34)))
db.session.add(Post(uid=61, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=68, c2_number=242,
                    league="Hardcore Legacy", name="Mad Irishman", time=datetime.datetime(2016, 6, 20, 7, 13, 44)))
db.session.add(
    Post(uid=62, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=23, c2_number=201, league="Hardcore Legacy",
         name="Snake Eyes", time=datetime.datetime(2016, 7, 8, 1, 51, 7)))
db.session.add(
    Post(uid=63, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=33, c2_number=70, league="Hardcore Legacy",
         name="Chocolate Thunder", time=datetime.datetime(2016, 10, 18, 6, 24, 47)))
db.session.add(
    Post(uid=64, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=71, c2_number=239, league="Hardcore Legacy",
         name="Mad Jack", time=datetime.datetime(2016, 9, 13, 16, 51, 9)))
db.session.add(
    Post(uid=65, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=141, c2_number=268, league="Hardcore Legacy",
         name="Snow Hound", time=datetime.datetime(2016, 11, 23, 20, 13, 7)))
db.session.add(Post(uid=66, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=139, c2_number=160,
                    league="Hardcore Legacy", name="Chuckles", time=datetime.datetime(2016, 5, 2, 11, 1, 53)))
db.session.add(
    Post(uid=67, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=274, c2_number=58, league="Hardcore Legacy",
         name="Mad Rascal", time=datetime.datetime(2016, 4, 7, 8, 42, 58)))
db.session.add(
    Post(uid=68, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=70, c2_number=140, league="Hardcore Legacy",
         name="Sofa King", time=datetime.datetime(2016, 7, 14, 9, 38, 27)))
db.session.add(Post(uid=69, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=173, c2_number=277,
                    league="Hardcore Legacy", name="Commando", time=datetime.datetime(2016, 7, 19, 16, 41, 22)))
db.session.add(
    Post(uid=70, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=77, c2_number=106, league="Hardcore Legacy",
         name="Manimal", time=datetime.datetime(2016, 11, 9, 6, 22, 44)))
db.session.add(
    Post(uid=71, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=200, c2_number=199, league="Hardcore Legacy",
         name="Speedwell", time=datetime.datetime(2016, 3, 17, 9, 12, 16)))
db.session.add(
    Post(uid=72, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=281, c2_number=220, league="Hardcore Legacy",
         name="Cool Whip", time=datetime.datetime(2016, 10, 18, 22, 28, 17)))
db.session.add(
    Post(uid=73, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=112, c2_number=39, league="Hardcore Legacy",
         name="Marbles", time=datetime.datetime(2016, 9, 8, 6, 14, 57)))
db.session.add(
    Post(uid=74, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=189, c2_number=239, league="Hardcore Legacy",
         name="Spider Fuji", time=datetime.datetime(2016, 12, 9, 3, 57, 52)))
db.session.add(
    Post(uid=75, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=242, c2_number=218, league="Hardcore Legacy",
         name="Cosmo", time=datetime.datetime(2016, 10, 21, 22, 51, 8)))
db.session.add(
    Post(uid=76, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=255, c2_number=224, league="Hardcore Legacy",
         name="Married Man", time=datetime.datetime(2016, 7, 1, 19, 42, 35)))
db.session.add(
    Post(uid=77, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=261, c2_number=279, league="Hardcore Legacy",
         name="Springheel Jack", time=datetime.datetime(2016, 11, 13, 9, 56, 9)))
db.session.add(
    Post(uid=78, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=161, c2_number=170, league="Hardcore Legacy",
         name="Crash Override", time=datetime.datetime(2016, 3, 12, 1, 28, 15)))
db.session.add(Post(uid=79, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=30, c2_number=257,
                    league="Hardcore Legacy", name="Marshmallow", time=datetime.datetime(2016, 5, 7, 12, 9, 40)))
db.session.add(
    Post(uid=80, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=147, c2_number=279, league="Hardcore Legacy",
         name="Squatch", time=datetime.datetime(2016, 9, 11, 12, 12, 20)))
db.session.add(Post(uid=81, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=235, c2_number=147,
                    league="Hardcore Legacy", name="Crash Test", time=datetime.datetime(2016, 11, 8, 0, 27, 16)))
db.session.add(
    Post(uid=82, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=40, c2_number=305, league="Hardcore Legacy",
         name="Mental", time=datetime.datetime(2016, 7, 21, 10, 45, 22)))
db.session.add(
    Post(uid=83, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=113, c2_number=93, league="Hardcore Legacy",
         name="Stacker of Wheat", time=datetime.datetime(2016, 8, 13, 14, 24, 36)))
db.session.add(Post(uid=84, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=92, c2_number=142,
                    league="Hardcore Legacy", name="Crazy Eights", time=datetime.datetime(2016, 8, 19, 3, 18, 8)))
db.session.add(Post(uid=85, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=313, c2_number=94,
                    league="Hardcore Legacy", name="Mercury Reborn", time=datetime.datetime(2016, 7, 2, 19, 47, 12)))
db.session.add(Post(uid=86, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=284, c2_number=291,
                    league="Hardcore Legacy", name="Sugar Man", time=datetime.datetime(2016, 4, 5, 13, 30, 47)))
db.session.add(Post(uid=87, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=70, c2_number=199,
                    league="Hardcore Legacy", name="Criss Cross", time=datetime.datetime(2016, 11, 11, 17, 18, 50)))
db.session.add(Post(uid=88, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=139, c2_number=28,
                    league="Hardcore Legacy", name="Midas", time=datetime.datetime(2016, 3, 23, 1, 47, 45)))
db.session.add(Post(uid=89, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=261, c2_number=189,
                    league="Hardcore Legacy", name="Suicide Jockey", time=datetime.datetime(2016, 11, 10, 16, 25, 20)))
db.session.add(Post(uid=90, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=293, c2_number=311,
                    league="Hardcore Legacy", name="Cross Thread", time=datetime.datetime(2016, 6, 23, 21, 45, 49)))
db.session.add(Post(uid=91, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=296, c2_number=264,
                    league="Hardcore Legacy", name="Midnight Rambler", time=datetime.datetime(2016, 1, 10, 13, 49, 55)))
db.session.add(
    Post(uid=92, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=208, c2_number=296, league="Hardcore Legacy",
         name="Swampmasher", time=datetime.datetime(2016, 6, 3, 3, 24, 0)))
db.session.add(
    Post(uid=93, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=98, c2_number=298, league="Hardcore Legacy",
         name="Cujo", time=datetime.datetime(2016, 8, 23, 8, 44, 19)))
db.session.add(Post(uid=94, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=289, c2_number=170,
                    league="Hardcore Legacy", name="Midnight Rider", time=datetime.datetime(2016, 9, 12, 15, 41, 5)))
db.session.add(
    Post(uid=95, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=164, c2_number=178, league="Hardcore Legacy",
         name="Swerve", time=datetime.datetime(2016, 12, 15, 17, 14, 41)))
db.session.add(
    Post(uid=96, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=206, c2_number=31, league="Hardcore Legacy",
         name="Dancing Madman", time=datetime.datetime(2016, 2, 5, 11, 41, 28)))
db.session.add(Post(uid=97, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=100, c2_number=178,
                    league="Hardcore Legacy", name="Mindless Bobcat", time=datetime.datetime(2016, 3, 21, 6, 55, 40)))
db.session.add(
    Post(uid=98, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=167, c2_number=77, league="Hardcore Legacy",
         name="Tacklebox", time=datetime.datetime(2016, 10, 10, 12, 12, 6)))
db.session.add(
    Post(uid=99, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=60, c2_number=225, league="Hardcore Legacy",
         name="Dangle", time=datetime.datetime(2016, 12, 14, 15, 37, 37)))
db.session.add(
    Post(uid=100, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=73, c2_number=143, league="Hardcore Legacy",
         name="Mr. 44", time=datetime.datetime(2016, 9, 15, 17, 36, 17)))
db.session.add(
    Post(uid=101, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=171, c2_number=248, league="Hardcore Legacy",
         name="Take Away", time=datetime.datetime(2016, 11, 9, 20, 25, 47)))
db.session.add(Post(uid=102, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=200, c2_number=309,
                    league="Hardcore Legacy", name="Dark Horse", time=datetime.datetime(2016, 12, 8, 1, 54, 28)))
db.session.add(Post(uid=103, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=202, c2_number=119,
                    league="Hardcore Legacy", name="Mr. Fabulous", time=datetime.datetime(2016, 7, 13, 18, 4, 32)))
db.session.add(Post(uid=104, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=315, c2_number=164,
                    league="Hardcore Legacy", name="Tan Stallion", time=datetime.datetime(2016, 8, 26, 5, 28, 1)))
db.session.add(Post(uid=105, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=190, c2_number=61,
                    league="Hardcore Legacy", name="Day Hawk", time=datetime.datetime(2016, 7, 9, 21, 2, 58)))
db.session.add(
    Post(uid=106, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=21, c2_number=219, league="Hardcore Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 3, 5, 19, 26, 52)))
db.session.add(
    Post(uid=107, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=297, c2_number=71, league="Hardcore Legacy",
         name="The China Wall", time=datetime.datetime(2016, 11, 5, 6, 37, 13)))
db.session.add(
    Post(uid=108, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=83, c2_number=293, league="Hardcore Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 5, 19, 19, 10, 11)))
db.session.add(Post(uid=109, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=32, c2_number=41,
                    league="Hardcore Legacy", name="Mr. Lucky", time=datetime.datetime(2016, 9, 11, 1, 41, 44)))
db.session.add(
    Post(uid=110, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=145, c2_number=214, league="Hardcore Legacy",
         name="The Dude", time=datetime.datetime(2016, 11, 11, 14, 11, 14)))
db.session.add(
    Post(uid=111, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=39, c2_number=231, league="Hardcore Legacy",
         name="Digger", time=datetime.datetime(2016, 3, 26, 6, 55, 48)))
db.session.add(
    Post(uid=112, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=46, c2_number=144, league="Hardcore Legacy",
         name="Mr. Peppermint", time=datetime.datetime(2016, 10, 16, 10, 43, 4)))
db.session.add(
    Post(uid=113, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=74, c2_number=62, league="Hardcore Legacy",
         name="The Flying Mouse", time=datetime.datetime(2016, 10, 3, 21, 27, 48)))
db.session.add(
    Post(uid=114, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=132, c2_number=68, league="Standard",
         name="Disco Thunder", time=datetime.datetime(2016, 3, 10, 21, 39, 42)))
db.session.add(Post(uid=115, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=114, c2_number=37,
                    league="Standard", name="Mr. Spy", time=datetime.datetime(2016, 4, 2, 20, 30, 49)))
db.session.add(
    Post(uid=116, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=133, c2_number=237, league="Standard",
         name="The Happy Jock", time=datetime.datetime(2016, 8, 8, 20, 46, 46)))
db.session.add(
    Post(uid=117, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=31, c2_number=78, league="Standard",
         name="Disco Potato", time=datetime.datetime(2016, 3, 28, 15, 43, 48)))
db.session.add(
    Post(uid=118, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=273, c2_number=297, league="Standard",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 7, 6, 16, 31, 43)))
db.session.add(
    Post(uid=119, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=249, c2_number=41, league="Standard",
         name="The Howling Swede", time=datetime.datetime(2016, 10, 12, 9, 9, 12)))
db.session.add(
    Post(uid=120, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=77, c2_number=246, league="Standard",
         name="Dr. Cocktail", time=datetime.datetime(2016, 3, 22, 15, 30, 6)))
db.session.add(
    Post(uid=121, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=274, c2_number=97, league="Standard",
         name="Mr. Wholesome", time=datetime.datetime(2016, 1, 8, 9, 41, 6)))
db.session.add(
    Post(uid=122, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=66, c2_number=28, league="Standard",
         name="Thrasher", time=datetime.datetime(2016, 8, 21, 21, 54, 43)))
db.session.add(
    Post(uid=123, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=75, c2_number=50, league="Standard",
         name="Dredd", time=datetime.datetime(2016, 9, 22, 21, 54, 23)))
db.session.add(
    Post(uid=124, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=222, c2_number=191, league="Standard",
         name="Mud Pie Man", time=datetime.datetime(2016, 2, 12, 20, 38, 52)))
db.session.add(
    Post(uid=125, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=179, c2_number=130, league="Standard",
         name="Toe", time=datetime.datetime(2016, 1, 3, 22, 49, 52)))
db.session.add(
    Post(uid=126, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=228, c2_number=260, league="Standard",
         name="Dropkick", time=datetime.datetime(2016, 5, 6, 14, 8, 16)))
db.session.add(
    Post(uid=127, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=28, c2_number=286, league="Standard",
         name="Mule Skinner", time=datetime.datetime(2016, 7, 5, 13, 9, 2)))
db.session.add(Post(uid=128, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=33, c2_number=208, league="Standard",
                    name="Toolmaker", time=datetime.datetime(2016, 12, 7, 3, 40, 13)))
db.session.add(Post(uid=129, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=88, c2_number=173, league="Standard",
                    name="Drop Stone", time=datetime.datetime(2016, 1, 24, 4, 43, 19)))
db.session.add(
    Post(uid=130, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=45, c2_number=273, league="Standard",
         name="Murmur", time=datetime.datetime(2016, 7, 26, 22, 12, 53)))
db.session.add(
    Post(uid=131, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=21, c2_number=25, league="Standard",
         name="Tough Nut", time=datetime.datetime(2016, 12, 23, 22, 3, 35)))
db.session.add(
    Post(uid=132, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=47, c2_number=68, league="Standard",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 12, 16, 0, 15, 38)))
db.session.add(
    Post(uid=133, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=188, c2_number=147,
         league="Standard", name="Nacho", time=datetime.datetime(2016, 2, 16, 4, 38, 28)))
db.session.add(
    Post(uid=134, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=237, c2_number=311, league="Standard",
         name="Trip", time=datetime.datetime(2016, 5, 25, 22, 31, 7)))
db.session.add(Post(uid=135, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=51, c2_number=27,
                    league="Standard", name="Easy Sweep", time=datetime.datetime(2016, 3, 4, 15, 44, 32)))
db.session.add(Post(uid=136, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=185, c2_number=197,
                    league="Standard", name="Natural Mess", time=datetime.datetime(2016, 2, 4, 21, 37, 18)))
db.session.add(Post(uid=137, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=157, c2_number=171,
                    league="Standard", name="Troubadour", time=datetime.datetime(2016, 10, 6, 5, 22, 4)))
db.session.add(Post(uid=138, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=115, c2_number=92,
                    league="Standard", name="Electric Player", time=datetime.datetime(2016, 2, 24, 19, 1, 8)))
db.session.add(Post(uid=139, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=223, c2_number=225,
                    league="Standard", name="Necromancer", time=datetime.datetime(2016, 7, 16, 2, 52, 1)))
db.session.add(Post(uid=140, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=270, c2_number=314,
                    league="Standard", name="Turnip King", time=datetime.datetime(2016, 2, 26, 15, 33, 33)))
db.session.add(Post(uid=141, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=46, c2_number=57,
                    league="Standard", name="Esquire", time=datetime.datetime(2016, 11, 1, 14, 21, 51)))
db.session.add(Post(uid=142, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=240, c2_number=252,
                    league="Standard", name="Neophyte Believer", time=datetime.datetime(2016, 12, 8, 1, 25, 34)))
db.session.add(Post(uid=143, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=148, c2_number=25,
                    league="Standard", name="Twitch", time=datetime.datetime(2016, 10, 12, 11, 9, 12)))
db.session.add(Post(uid=144, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=139, c2_number=188,
                    league="Standard", name="Fast Draw", time=datetime.datetime(2016, 12, 13, 11, 42, 52)))
db.session.add(Post(uid=145, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=144, c2_number=185,
                    league="Standard", name="Nessie", time=datetime.datetime(2016, 11, 13, 20, 31, 9)))
db.session.add(
    Post(uid=146, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=166, c2_number=144, league="Standard",
         name="Vagabond Warrior", time=datetime.datetime(2016, 9, 12, 15, 33, 44)))
db.session.add(
    Post(uid=147, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=282, c2_number=173, league="Standard",
         name="Flakes", time=datetime.datetime(2016, 10, 24, 10, 20, 10)))
db.session.add(Post(uid=148, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=158, c2_number=167,
                    league="Standard", name="New Cycle", time=datetime.datetime(2016, 7, 4, 17, 29, 14)))
db.session.add(Post(uid=149, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=218, c2_number=60,
                    league="Standard", name="Voluntary", time=datetime.datetime(2016, 4, 4, 21, 35, 10)))
db.session.add(
    Post(uid=150, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=169, c2_number=236, league="Standard",
         name="Flint", time=datetime.datetime(2016, 1, 4, 9, 37, 20)))
db.session.add(
    Post(uid=151, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=61, c2_number=133, league="Standard",
         name="Nickname Master", time=datetime.datetime(2016, 8, 17, 1, 15, 19)))
db.session.add(Post(uid=152, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=41, c2_number=273, league="Standard",
                    name="Vortex", time=datetime.datetime(2016, 6, 13, 3, 49, 37)))
db.session.add(
    Post(uid=153, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=260, c2_number=264, league="Standard",
         name="Freak", time=datetime.datetime(2016, 5, 16, 16, 40, 39)))
db.session.add(Post(uid=154, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=52, c2_number=63, league="Standard",
                    name="Nightmare King", time=datetime.datetime(2016, 4, 1, 8, 31, 11)))
db.session.add(Post(uid=155, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=139, c2_number=88, league="Standard",
                    name="Washer", time=datetime.datetime(2016, 12, 3, 15, 49, 18)))
db.session.add(
    Post(uid=156, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=143, c2_number=37, league="Standard",
         name="Gas Man", time=datetime.datetime(2016, 1, 19, 21, 20, 55)))
db.session.add(
    Post(uid=157, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=307, c2_number=290, league="Standard",
         name="Night Train", time=datetime.datetime(2016, 12, 18, 9, 37, 57)))
db.session.add(
    Post(uid=158, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=39, c2_number=175, league="Standard",
         name="Waylay Dave", time=datetime.datetime(2016, 6, 9, 14, 48, 30)))
db.session.add(
    Post(uid=159, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=199, c2_number=78, league="Standard",
         name="Glyph", time=datetime.datetime(2016, 11, 16, 20, 49, 29)))
db.session.add(
    Post(uid=160, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=278, c2_number=211, league="Standard",
         name="Old Man Winter", time=datetime.datetime(2016, 12, 13, 6, 11, 10)))
db.session.add(
    Post(uid=161, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=105, c2_number=268, league="Standard",
         name="Wheels", time=datetime.datetime(2016, 8, 28, 6, 49, 35)))
db.session.add(
    Post(uid=162, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=27, c2_number=132, league="Standard",
         name="Grave Digger", time=datetime.datetime(2016, 1, 25, 16, 10, 50)))
db.session.add(
    Post(uid=163, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=194, c2_number=170, league="Standard",
         name="Old Orange Eyes", time=datetime.datetime(2016, 10, 26, 9, 26, 17)))
db.session.add(Post(uid=164, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=248, c2_number=96, league="Standard",
                    name="Wooden Man", time=datetime.datetime(2016, 11, 13, 16, 6, 56)))
db.session.add(Post(uid=165, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=226, c2_number=23, league="Standard",
                    name="Guillotine", time=datetime.datetime(2016, 8, 28, 17, 41, 53)))
db.session.add(
    Post(uid=166, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=114, c2_number=253, league="Standard",
         name="Old Regret", time=datetime.datetime(2016, 4, 19, 19, 16, 48)))
db.session.add(
    Post(uid=167, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=277, c2_number=232, league="Standard",
         name="Woo Woo", time=datetime.datetime(2016, 4, 13, 11, 23, 45)))
db.session.add(
    Post(uid=168, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=274, c2_number=270, league="Standard",
         name="Gunhawk", time=datetime.datetime(2016, 12, 22, 4, 24, 48)))
db.session.add(Post(uid=169, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=116, c2_number=49,
                    league="Standard", name="Onion King", time=datetime.datetime(2016, 5, 20, 1, 26, 45)))
db.session.add(
    Post(uid=170, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=274, c2_number=220, league="Standard",
         name="Yellow Menace", time=datetime.datetime(2016, 11, 17, 7, 2, 23)))
db.session.add(
    Post(uid=171, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=230, c2_number=58, league="Standard",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 2, 8, 20, 13, 46)))
db.session.add(
    Post(uid=172, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=75, c2_number=143, league="Standard",
         name="Osprey", time=datetime.datetime(2016, 10, 22, 9, 51, 1)))
db.session.add(
    Post(uid=173, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=177, c2_number=243, league="Standard",
         name="Zero Charisma", time=datetime.datetime(2016, 8, 26, 3, 33, 46)))
db.session.add(
    Post(uid=174, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=275, c2_number=281, league="Standard",
         name="Highlander Monk", time=datetime.datetime(2016, 9, 19, 9, 55, 10)))
db.session.add(
    Post(uid=175, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=144, c2_number=209, league="Standard",
         name="Overrun", time=datetime.datetime(2016, 12, 4, 3, 31, 33)))
db.session.add(
    Post(uid=176, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=294, c2_number=48, league="Standard",
         name="Zesty Dragon", time=datetime.datetime(2016, 5, 23, 19, 7, 12)))
db.session.add(
    Post(uid=177, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=144, c2_number=214, league="Standard",
         name="Zod", time=datetime.datetime(2016, 6, 11, 2, 57, 32)))
db.session.add(
    Post(uid=0, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=204, c2_number=53, league="Standard",
         name="101", time=datetime.datetime(2016, 7, 2, 19, 39, 3)))
db.session.add(
    Post(uid=1, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=284, c2_number=253, league="Standard",
         name="Houston", time=datetime.datetime(2016, 8, 15, 13, 32, 41)))
db.session.add(
    Post(uid=2, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=139, c2_number=169, league="Standard",
         name="Pinball Wizard", time=datetime.datetime(2016, 5, 27, 8, 5, 34)))
db.session.add(
    Post(uid=3, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=308, c2_number=289, league="Standard",
         name="Accidental Genius", time=datetime.datetime(2016, 5, 24, 18, 4, 49)))
db.session.add(
    Post(uid=4, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=188, c2_number=186, league="Standard",
         name="Hyper", time=datetime.datetime(2016, 5, 20, 20, 13, 28)))
db.session.add(Post(uid=5, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=215, c2_number=122, league="Standard",
                    name="Pluto", time=datetime.datetime(2016, 9, 11, 1, 19, 35)))
db.session.add(
    Post(uid=6, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=102, c2_number=149, league="Standard",
         name="Alpha", time=datetime.datetime(2016, 3, 11, 13, 54, 55)))
db.session.add(
    Post(uid=7, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=290, c2_number=224, league="Standard",
         name="Jester", time=datetime.datetime(2016, 8, 22, 17, 24, 10)))
db.session.add(Post(uid=8, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=65, c2_number=146, league="Standard",
                    name="Pogue", time=datetime.datetime(2016, 7, 28, 4, 1, 45)))
db.session.add(
    Post(uid=9, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=34, c2_number=160, league="Standard",
         name="Airport Hobo", time=datetime.datetime(2016, 7, 4, 10, 38, 26)))
db.session.add(Post(uid=10, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=220, c2_number=257, league="Standard",
                    name="Jigsaw", time=datetime.datetime(2016, 7, 23, 10, 57, 28)))
db.session.add(
    Post(uid=11, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=128, c2_number=64, league="Standard",
         name="Prometheus", time=datetime.datetime(2016, 1, 17, 14, 43, 11)))
db.session.add(Post(uid=12, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=147, c2_number=131, league="Standard",
                    name="Bearded Angler", time=datetime.datetime(2016, 5, 3, 2, 29, 13)))
db.session.add(
    Post(uid=13, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=254, c2_number=100, league="Standard",
         name="Joker's Grin", time=datetime.datetime(2016, 6, 14, 2, 29, 22)))
db.session.add(
    Post(uid=14, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=58, c2_number=259, league="Standard",
         name="Psycho Thinker", time=datetime.datetime(2016, 10, 14, 5, 21, 1)))
db.session.add(
    Post(uid=15, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=193, c2_number=245, league="Standard",
         name="Beetle King", time=datetime.datetime(2016, 2, 23, 10, 35, 53)))
db.session.add(
    Post(uid=16, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=261, c2_number=141, league="Standard",
         name="Judge", time=datetime.datetime(2016, 12, 13, 8, 31, 1)))
db.session.add(
    Post(uid=17, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=272, c2_number=100, league="Standard",
         name="Pusher", time=datetime.datetime(2016, 5, 24, 21, 33, 46)))
db.session.add(
    Post(uid=18, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=46, c2_number=272, league="Standard",
         name="Bitmap", time=datetime.datetime(2016, 4, 24, 0, 33, 29)))
db.session.add(
    Post(uid=19, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=179, c2_number=152, league="Standard",
         name="Junkyard Dog", time=datetime.datetime(2016, 3, 5, 5, 50, 43)))
db.session.add(
    Post(uid=20, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=150, c2_number=305, league="Standard",
         name="Riff Raff", time=datetime.datetime(2016, 9, 11, 1, 10, 27)))
db.session.add(
    Post(uid=21, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=96, c2_number=47, league="Standard",
         name="Blister", time=datetime.datetime(2016, 10, 27, 1, 21, 16)))
db.session.add(
    Post(uid=22, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=121, c2_number=151, league="Standard", name="K-9",
         time=datetime.datetime(2016, 8, 27, 19, 20, 25)))
db.session.add(Post(uid=23, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=228, c2_number=52, league="Standard",
                    name="Roadblock", time=datetime.datetime(2016, 9, 18, 18, 22, 13)))
db.session.add(
    Post(uid=24, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=189, c2_number=312, league="Standard",
         name="Bowie", time=datetime.datetime(2016, 4, 11, 13, 53, 49)))
db.session.add(
    Post(uid=25, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=198, c2_number=297, league="Standard",
         name="Keystone", time=datetime.datetime(2016, 7, 26, 6, 11, 55)))
db.session.add(
    Post(uid=26, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=234, c2_number=228, league="Standard",
         name="Rooster", time=datetime.datetime(2016, 1, 13, 11, 14, 36)))
db.session.add(
    Post(uid=27, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=199, c2_number=95, league="Standard",
         name="Bowler", time=datetime.datetime(2016, 4, 4, 8, 57, 0)))
db.session.add(Post(uid=28, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=230, c2_number=218, league="Standard",
                    name="Kickstart", time=datetime.datetime(2016, 3, 17, 21, 58, 12)))
db.session.add(
    Post(uid=29, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=285, c2_number=182, league="Standard",
         name="Sandbox", time=datetime.datetime(2016, 1, 24, 19, 35, 50)))
db.session.add(Post(uid=30, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=117, c2_number=22, league="Standard",
                    name="Breadmaker", time=datetime.datetime(2016, 2, 22, 7, 50, 58)))
db.session.add(Post(uid=31, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=63, c2_number=50, league="Standard",
                    name="Kill Switch", time=datetime.datetime(2016, 2, 24, 20, 51, 3)))
db.session.add(
    Post(uid=32, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=242, c2_number=133, league="Standard",
         name="Scrapper", time=datetime.datetime(2016, 12, 21, 20, 18, 22)))
db.session.add(
    Post(uid=33, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=237, c2_number=138, league="Standard",
         name="Broomspun", time=datetime.datetime(2016, 11, 16, 9, 9, 18)))
db.session.add(
    Post(uid=34, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=257, c2_number=157, league="Standard",
         name="Kingfisher", time=datetime.datetime(2016, 8, 23, 15, 30, 14)))
db.session.add(
    Post(uid=35, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=32, c2_number=225, league="Standard",
         name="Screwtape", time=datetime.datetime(2016, 1, 1, 7, 8, 37)))
db.session.add(
    Post(uid=36, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=50, c2_number=120, league="Standard",
         name="Buckshot", time=datetime.datetime(2016, 5, 18, 16, 38, 7)))
db.session.add(
    Post(uid=37, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=77, c2_number=303, league="Standard",
         name="Kitchen", time=datetime.datetime(2016, 1, 12, 10, 39, 4)))
db.session.add(
    Post(uid=38, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=176, c2_number=221, league="Standard",
         name="Sexual Chocolate", time=datetime.datetime(2016, 6, 14, 5, 17, 44)))
db.session.add(
    Post(uid=39, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=296, c2_number=261, league="Standard",
         name="Bugger", time=datetime.datetime(2016, 1, 25, 13, 17, 19)))
db.session.add(Post(uid=40, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=233, c2_number=128, league="Standard",
                    name="Knuckles", time=datetime.datetime(2016, 5, 24, 12, 18, 49)))
db.session.add(Post(uid=41, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=82, c2_number=160, league="Standard",
                    name="Shadow Chaser", time=datetime.datetime(2016, 8, 6, 22, 44, 23)))
db.session.add(
    Post(uid=42, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=207, c2_number=191, league="Standard",
         name="Cabbie", time=datetime.datetime(2016, 11, 2, 3, 34, 26)))
db.session.add(
    Post(uid=43, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=55, c2_number=238, league="Standard",
         name="Lady Killer", time=datetime.datetime(2016, 2, 8, 14, 44, 32)))
db.session.add(
    Post(uid=44, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=26, c2_number=295, league="Standard",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 4, 4, 3, 54, 11)))
db.session.add(Post(uid=45, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=230, c2_number=263,
                    league="Standard", name="Candy Butcher", time=datetime.datetime(2016, 5, 11, 20, 56, 54)))
db.session.add(
    Post(uid=46, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=48, c2_number=231, league="Standard",
         name="Liquid Science", time=datetime.datetime(2016, 10, 28, 7, 31, 17)))
db.session.add(
    Post(uid=47, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=56, c2_number=101, league="Standard",
         name="Shooter", time=datetime.datetime(2016, 11, 18, 11, 20, 29)))
db.session.add(
    Post(uid=48, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=140, c2_number=137, league="Standard",
         name="Capital F", time=datetime.datetime(2016, 2, 9, 21, 49, 49)))
db.session.add(
    Post(uid=49, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=309, c2_number=313, league="Standard",
         name="Little Cobra", time=datetime.datetime(2016, 5, 12, 21, 9, 10)))
db.session.add(Post(uid=50, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=278, c2_number=147,
                    league="Standard", name="Sidewalk Enforcer", time=datetime.datetime(2016, 2, 5, 8, 57, 4)))
db.session.add(
    Post(uid=51, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=55, c2_number=70, league="Standard",
         name="Captain Peroxide", time=datetime.datetime(2016, 6, 20, 22, 39, 9)))
db.session.add(
    Post(uid=52, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=44, c2_number=120, league="Standard",
         name="Little General", time=datetime.datetime(2016, 10, 22, 21, 5, 53)))
db.session.add(Post(uid=53, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=82, c2_number=52,
                    league="Standard", name="Skull Crusher", time=datetime.datetime(2016, 6, 8, 12, 32, 3)))
db.session.add(
    Post(uid=54, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=261, c2_number=125, league="Standard",
         name="Celtic Charger", time=datetime.datetime(2016, 3, 12, 1, 32, 36)))
db.session.add(
    Post(uid=55, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=43, c2_number=36, league="Standard",
         name="Lord Nikon", time=datetime.datetime(2016, 7, 7, 21, 49, 13)))
db.session.add(
    Post(uid=56, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=168, c2_number=88, league="Standard",
         name="Sky Bully", time=datetime.datetime(2016, 6, 5, 6, 6, 29)))
db.session.add(Post(uid=57, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=111, c2_number=115,
                    league="Standard", name="Cereal Killer", time=datetime.datetime(2016, 10, 9, 0, 38, 19)))
db.session.add(
    Post(uid=58, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=84, c2_number=74, league="Standard",
         name="Lord Pistachio", time=datetime.datetime(2016, 8, 11, 12, 0, 29)))
db.session.add(
    Post(uid=59, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=36, c2_number=300, league="Standard",
         name="Slow Trot", time=datetime.datetime(2016, 4, 5, 11, 55, 44)))
db.session.add(
    Post(uid=60, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=291, c2_number=285, league="Standard",
         name="Chicago Blackout", time=datetime.datetime(2016, 10, 7, 13, 20, 47)))
db.session.add(
    Post(uid=61, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=93, c2_number=308, league="Standard",
         name="Mad Irishman", time=datetime.datetime(2016, 4, 2, 4, 44, 40)))
db.session.add(
    Post(uid=62, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=65, c2_number=286, league="Standard",
         name="Snake Eyes", time=datetime.datetime(2016, 8, 2, 9, 21, 50)))
db.session.add(Post(uid=63, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=145, c2_number=294,
                    league="Standard", name="Chocolate Thunder", time=datetime.datetime(2016, 12, 23, 1, 8, 39)))
db.session.add(
    Post(uid=64, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=201, c2_number=130, league="Standard",
         name="Mad Jack", time=datetime.datetime(2016, 9, 10, 6, 3, 39)))
db.session.add(
    Post(uid=65, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=255, c2_number=68, league="Standard",
         name="Snow Hound", time=datetime.datetime(2016, 9, 20, 4, 24, 12)))
db.session.add(
    Post(uid=66, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=291, c2_number=302, league="Standard",
         name="Chuckles", time=datetime.datetime(2016, 9, 3, 3, 16, 51)))
db.session.add(
    Post(uid=67, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=278, c2_number=309, league="Standard",
         name="Mad Rascal", time=datetime.datetime(2016, 7, 6, 9, 29, 17)))
db.session.add(
    Post(uid=68, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=98, c2_number=307, league="Standard",
         name="Sofa King", time=datetime.datetime(2016, 12, 17, 15, 8, 35)))
db.session.add(
    Post(uid=69, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=88, c2_number=24, league="Standard",
         name="Commando", time=datetime.datetime(2016, 4, 7, 7, 46, 2)))
db.session.add(
    Post(uid=70, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=95, c2_number=82, league="Standard",
         name="Manimal", time=datetime.datetime(2016, 10, 17, 8, 25, 31)))
db.session.add(
    Post(uid=71, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=51, c2_number=275, league="Standard",
         name="Speedwell", time=datetime.datetime(2016, 11, 26, 13, 54, 28)))
db.session.add(
    Post(uid=72, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=264, c2_number=87, league="Standard",
         name="Cool Whip", time=datetime.datetime(2016, 4, 25, 21, 55, 13)))
db.session.add(
    Post(uid=73, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=54, c2_number=234, league="Standard",
         name="Marbles", time=datetime.datetime(2016, 3, 9, 18, 20, 1)))
db.session.add(
    Post(uid=74, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=125, c2_number=193, league="Standard",
         name="Spider Fuji", time=datetime.datetime(2016, 12, 26, 1, 7, 44)))
db.session.add(
    Post(uid=75, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=54, c2_number=245, league="Standard",
         name="Cosmo", time=datetime.datetime(2016, 5, 18, 4, 20, 12)))
db.session.add(
    Post(uid=76, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=82, c2_number=302, league="Standard",
         name="Married Man", time=datetime.datetime(2016, 12, 6, 18, 55, 24)))
db.session.add(
    Post(uid=77, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=47, c2_number=213, league="Standard",
         name="Springheel Jack", time=datetime.datetime(2016, 2, 22, 15, 47, 47)))
db.session.add(
    Post(uid=78, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=31, c2_number=130, league="Standard",
         name="Crash Override", time=datetime.datetime(2016, 6, 24, 17, 56, 26)))
db.session.add(
    Post(uid=79, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=256, c2_number=278, league="Standard",
         name="Marshmallow", time=datetime.datetime(2016, 12, 16, 12, 42, 39)))
db.session.add(
    Post(uid=80, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=125, c2_number=39, league="Standard",
         name="Squatch", time=datetime.datetime(2016, 9, 23, 17, 56, 18)))
db.session.add(Post(uid=81, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=308, c2_number=278,
                    league="Standard", name="Crash Test", time=datetime.datetime(2016, 1, 19, 7, 1, 8)))
db.session.add(
    Post(uid=82, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=283, c2_number=302, league="Standard",
         name="Mental", time=datetime.datetime(2016, 1, 28, 18, 47, 57)))
db.session.add(
    Post(uid=83, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=283, c2_number=86, league="Standard",
         name="Stacker of Wheat", time=datetime.datetime(2016, 6, 19, 22, 22, 41)))
db.session.add(
    Post(uid=84, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=36, c2_number=175, league="Standard",
         name="Crazy Eights", time=datetime.datetime(2016, 2, 13, 16, 57, 22)))
db.session.add(
    Post(uid=85, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=112, c2_number=234, league="Standard",
         name="Mercury Reborn", time=datetime.datetime(2016, 8, 9, 20, 21, 33)))
db.session.add(
    Post(uid=86, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=236, c2_number=276, league="Standard",
         name="Sugar Man", time=datetime.datetime(2016, 10, 23, 4, 35, 14)))
db.session.add(
    Post(uid=87, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=317, c2_number=48, league="Standard",
         name="Criss Cross", time=datetime.datetime(2016, 7, 1, 18, 45, 22)))
db.session.add(
    Post(uid=88, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=123, c2_number=30, league="Standard",
         name="Midas", time=datetime.datetime(2016, 8, 7, 4, 19, 55)))
db.session.add(
    Post(uid=89, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=261, c2_number=308, league="Standard",
         name="Suicide Jockey", time=datetime.datetime(2016, 1, 24, 11, 20, 1)))
db.session.add(
    Post(uid=90, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=163, c2_number=81, league="Standard",
         name="Cross Thread", time=datetime.datetime(2016, 8, 17, 10, 1, 18)))
db.session.add(
    Post(uid=91, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=84, c2_number=215, league="Standard",
         name="Midnight Rambler", time=datetime.datetime(2016, 8, 17, 17, 41, 48)))
db.session.add(
    Post(uid=92, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=79, c2_number=254, league="Standard",
         name="Swampmasher", time=datetime.datetime(2016, 6, 25, 3, 30, 2)))
db.session.add(
    Post(uid=93, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=213, c2_number=226, league="Standard",
         name="Cujo", time=datetime.datetime(2016, 3, 7, 7, 33, 1)))
db.session.add(
    Post(uid=94, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=224, c2_number=198, league="Standard",
         name="Midnight Rider", time=datetime.datetime(2016, 5, 10, 14, 28, 14)))
db.session.add(
    Post(uid=95, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=312, c2_number=105, league="Standard",
         name="Swerve", time=datetime.datetime(2016, 8, 11, 0, 58, 31)))
db.session.add(
    Post(uid=96, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=285, c2_number=259, league="Standard",
         name="Dancing Madman", time=datetime.datetime(2016, 10, 26, 21, 54, 20)))
db.session.add(
    Post(uid=97, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=74, c2_number=105, league="Standard",
         name="Mindless Bobcat", time=datetime.datetime(2016, 9, 16, 17, 55, 29)))
db.session.add(
    Post(uid=98, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=289, c2_number=190, league="Standard",
         name="Tacklebox", time=datetime.datetime(2016, 5, 4, 17, 45, 24)))
db.session.add(Post(uid=99, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=138, c2_number=215,
                    league="Standard", name="Dangle", time=datetime.datetime(2016, 4, 9, 9, 8, 21)))
db.session.add(
    Post(uid=100, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=98, c2_number=283, league="Standard",
         name="Mr. 44", time=datetime.datetime(2016, 2, 8, 16, 8, 13)))
db.session.add(
    Post(uid=101, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=43, c2_number=68, league="Standard",
         name="Take Away", time=datetime.datetime(2016, 10, 8, 9, 23, 38)))
db.session.add(
    Post(uid=102, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=62, c2_number=293, league="Standard",
         name="Dark Horse", time=datetime.datetime(2016, 3, 20, 3, 43, 17)))
db.session.add(
    Post(uid=103, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=116, c2_number=207, league="Standard",
         name="Mr. Fabulous", time=datetime.datetime(2016, 1, 20, 10, 51, 6)))
db.session.add(Post(uid=104, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=268, c2_number=213,
                    league="Standard", name="Tan Stallion", time=datetime.datetime(2016, 5, 4, 1, 20, 3)))
db.session.add(
    Post(uid=105, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=310, c2_number=94, league="Standard",
         name="Day Hawk", time=datetime.datetime(2016, 9, 8, 9, 9, 15)))
db.session.add(Post(uid=106, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=196, c2_number=209,
                    league="Standard", name="Mr. Gadget", time=datetime.datetime(2016, 9, 24, 2, 47, 0)))
db.session.add(Post(uid=107, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=300, c2_number=176,
                    league="Standard", name="The China Wall", time=datetime.datetime(2016, 11, 16, 15, 22, 18)))
db.session.add(
    Post(uid=108, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=27, c2_number=47, league="Standard",
         name="Desert Haze", time=datetime.datetime(2016, 7, 9, 11, 51, 10)))
db.session.add(
    Post(uid=109, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=214, c2_number=75, league="Standard",
         name="Mr. Lucky", time=datetime.datetime(2016, 10, 26, 2, 46, 58)))
db.session.add(
    Post(uid=110, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=112, c2_number=310, league="Standard",
         name="The Dude", time=datetime.datetime(2016, 8, 18, 13, 52, 22)))
db.session.add(Post(uid=111, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=181, c2_number=164,
                    league="Standard", name="Digger", time=datetime.datetime(2016, 12, 24, 8, 4, 6)))
db.session.add(
    Post(uid=112, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=49, c2_number=45, league="Standard",
         name="Mr. Peppermint", time=datetime.datetime(2016, 7, 21, 2, 22, 26)))
db.session.add(
    Post(uid=113, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=187, c2_number=307, league="Standard",
         name="The Flying Mouse", time=datetime.datetime(2016, 8, 24, 6, 9, 44)))
db.session.add(
    Post(uid=114, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=102, c2_number=36, league="Standard",
         name="Disco Thunder", time=datetime.datetime(2016, 1, 15, 22, 19, 6)))
db.session.add(
    Post(uid=115, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=296, c2_number=170, league="Standard",
         name="Mr. Spy", time=datetime.datetime(2016, 11, 6, 16, 43, 7)))
db.session.add(
    Post(uid=116, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=36, c2_number=178, league="Standard",
         name="The Happy Jock", time=datetime.datetime(2016, 10, 4, 12, 11, 12)))
db.session.add(Post(uid=117, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=88, c2_number=305,
                    league="Standard", name="Disco Potato", time=datetime.datetime(2016, 6, 6, 11, 33, 40)))
db.session.add(
    Post(uid=118, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=290, c2_number=137, league="Standard",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 9, 11, 16, 33, 29)))
db.session.add(
    Post(uid=119, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=99, c2_number=202, league="Standard",
         name="The Howling Swede", time=datetime.datetime(2016, 3, 15, 11, 27, 35)))
db.session.add(
    Post(uid=120, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=143, c2_number=99, league="Standard",
         name="Dr. Cocktail", time=datetime.datetime(2016, 8, 2, 1, 54, 19)))
db.session.add(
    Post(uid=121, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=30, c2_number=249, league="Standard",
         name="Mr. Wholesome", time=datetime.datetime(2016, 7, 21, 6, 37, 5)))
db.session.add(
    Post(uid=122, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=80, c2_number=149, league="Standard",
         name="Thrasher", time=datetime.datetime(2016, 7, 10, 20, 20, 0)))
db.session.add(
    Post(uid=123, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=107, c2_number=218, league="Standard",
         name="Dredd", time=datetime.datetime(2016, 10, 22, 17, 36, 28)))
db.session.add(
    Post(uid=124, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=54, c2_number=283, league="Standard",
         name="Mud Pie Man", time=datetime.datetime(2016, 1, 9, 22, 15, 17)))
db.session.add(
    Post(uid=125, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=161, c2_number=231, league="Standard",
         name="Toe", time=datetime.datetime(2016, 12, 24, 8, 26, 6)))
db.session.add(
    Post(uid=126, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=72, c2_number=64, league="Standard",
         name="Dropkick", time=datetime.datetime(2016, 4, 23, 7, 37, 5)))
db.session.add(
    Post(uid=127, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=281, c2_number=242, league="Standard",
         name="Mule Skinner", time=datetime.datetime(2016, 8, 9, 12, 21, 34)))
db.session.add(
    Post(uid=128, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=223, c2_number=244, league="Standard",
         name="Toolmaker", time=datetime.datetime(2016, 7, 8, 10, 49, 50)))
db.session.add(
    Post(uid=129, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=250, c2_number=255, league="Standard",
         name="Drop Stone", time=datetime.datetime(2016, 8, 24, 10, 2, 15)))
db.session.add(
    Post(uid=130, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=106, c2_number=153, league="Standard",
         name="Murmur", time=datetime.datetime(2016, 3, 22, 12, 58, 21)))
db.session.add(
    Post(uid=131, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=21, c2_number=171, league="Standard",
         name="Tough Nut", time=datetime.datetime(2016, 7, 1, 7, 18, 11)))
db.session.add(
    Post(uid=132, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=212, c2_number=301, league="Standard",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 5, 15, 3, 51, 5)))
db.session.add(
    Post(uid=133, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=152, c2_number=300, league="Standard",
         name="Nacho", time=datetime.datetime(2016, 9, 9, 16, 28, 0)))
db.session.add(
    Post(uid=134, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=276, c2_number=267, league="Standard",
         name="Trip", time=datetime.datetime(2016, 2, 19, 19, 45, 39)))
db.session.add(Post(uid=135, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=171, c2_number=251,
                    league="Standard", name="Easy Sweep", time=datetime.datetime(2016, 8, 1, 9, 56, 20)))
db.session.add(
    Post(uid=136, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=173, c2_number=162, league="Standard",
         name="Natural Mess", time=datetime.datetime(2016, 2, 5, 20, 30, 47)))
db.session.add(
    Post(uid=137, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=319, c2_number=202, league="Standard",
         name="Troubadour", time=datetime.datetime(2016, 11, 11, 9, 14, 5)))
db.session.add(
    Post(uid=138, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=255, c2_number=221, league="Standard",
         name="Electric Player", time=datetime.datetime(2016, 3, 25, 7, 54, 16)))
db.session.add(
    Post(uid=139, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=115, c2_number=180, league="Standard",
         name="Necromancer", time=datetime.datetime(2016, 12, 1, 8, 22, 8)))
db.session.add(
    Post(uid=140, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=312, c2_number=253, league="Standard",
         name="Turnip King", time=datetime.datetime(2016, 3, 2, 0, 4, 29)))
db.session.add(
    Post(uid=141, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=208, c2_number=82, league="Standard",
         name="Esquire", time=datetime.datetime(2016, 5, 17, 19, 36, 44)))
db.session.add(
    Post(uid=142, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=222, c2_number=289, league="Standard",
         name="Neophyte Believer", time=datetime.datetime(2016, 4, 14, 4, 43, 54)))
db.session.add(
    Post(uid=143, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=294, c2_number=268, league="Standard",
         name="Twitch", time=datetime.datetime(2016, 8, 14, 6, 13, 39)))
db.session.add(
    Post(uid=144, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=191, c2_number=308, league="Standard",
         name="Fast Draw", time=datetime.datetime(2016, 1, 8, 9, 57, 49)))
db.session.add(
    Post(uid=145, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=112, c2_number=219, league="Standard",
         name="Nessie", time=datetime.datetime(2016, 5, 18, 19, 19, 35)))
db.session.add(
    Post(uid=146, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=63, c2_number=238, league="Standard",
         name="Vagabond Warrior", time=datetime.datetime(2016, 8, 13, 3, 15, 26)))
db.session.add(
    Post(uid=147, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=179, c2_number=109, league="Standard",
         name="Flakes", time=datetime.datetime(2016, 1, 15, 13, 57, 41)))
db.session.add(
    Post(uid=148, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=42, c2_number=255, league="Standard",
         name="New Cycle", time=datetime.datetime(2016, 10, 2, 21, 14, 45)))
db.session.add(
    Post(uid=149, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=136, c2_number=94, league="Standard",
         name="Voluntary", time=datetime.datetime(2016, 1, 25, 21, 41, 45)))
db.session.add(
    Post(uid=150, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=131, c2_number=218, league="Standard",
         name="Flint", time=datetime.datetime(2016, 7, 20, 20, 17, 5)))
db.session.add(
    Post(uid=151, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=199, c2_number=319, league="Standard",
         name="Nickname Master", time=datetime.datetime(2016, 11, 16, 7, 49, 57)))
db.session.add(
    Post(uid=152, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=237, c2_number=31, league="Standard",
         name="Vortex", time=datetime.datetime(2016, 12, 5, 13, 39, 33)))
db.session.add(Post(uid=153, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=46, c2_number=307,
                    league="Standard", name="Freak", time=datetime.datetime(2016, 4, 22, 6, 37, 44)))
db.session.add(
    Post(uid=154, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=70, c2_number=177, league="Standard",
         name="Nightmare King", time=datetime.datetime(2016, 4, 28, 19, 57, 49)))
db.session.add(
    Post(uid=155, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=313, c2_number=241, league="Standard",
         name="Washer", time=datetime.datetime(2016, 2, 21, 12, 46, 52)))
db.session.add(
    Post(uid=156, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=290, c2_number=20, league="Standard",
         name="Gas Man", time=datetime.datetime(2016, 7, 6, 20, 15, 38)))
db.session.add(
    Post(uid=157, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=36, c2_number=41, league="Standard",
         name="Night Train", time=datetime.datetime(2016, 12, 1, 11, 25, 32)))
db.session.add(
    Post(uid=158, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=107, c2_number=286, league="Standard",
         name="Waylay Dave", time=datetime.datetime(2016, 8, 8, 9, 9, 25)))
db.session.add(
    Post(uid=159, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=39, c2_number=180, league="Standard",
         name="Glyph", time=datetime.datetime(2016, 10, 24, 8, 55, 19)))
db.session.add(
    Post(uid=160, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=81, c2_number=232, league="Standard",
         name="Old Man Winter", time=datetime.datetime(2016, 1, 3, 21, 28, 28)))
db.session.add(
    Post(uid=161, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=137, c2_number=57, league="Standard",
         name="Wheels", time=datetime.datetime(2016, 5, 13, 14, 20, 39)))
db.session.add(
    Post(uid=162, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=229, c2_number=271, league="Standard",
         name="Grave Digger", time=datetime.datetime(2016, 8, 9, 3, 25, 20)))
db.session.add(
    Post(uid=163, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=49, c2_number=261, league="Standard",
         name="Old Orange Eyes", time=datetime.datetime(2016, 9, 13, 2, 33, 18)))
db.session.add(
    Post(uid=164, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=242, c2_number=152, league="Standard",
         name="Wooden Man", time=datetime.datetime(2016, 2, 3, 21, 7, 6)))
db.session.add(
    Post(uid=165, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=73, c2_number=101, league="Standard",
         name="Guillotine", time=datetime.datetime(2016, 9, 22, 12, 41, 19)))
db.session.add(
    Post(uid=166, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=36, c2_number=137, league="Standard",
         name="Old Regret", time=datetime.datetime(2016, 10, 9, 9, 34, 17)))
db.session.add(
    Post(uid=167, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=112, c2_number=239, league="Standard",
         name="Woo Woo", time=datetime.datetime(2016, 9, 25, 8, 34, 53)))
db.session.add(
    Post(uid=168, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=99, c2_number=292, league="Standard",
         name="Gunhawk", time=datetime.datetime(2016, 3, 9, 19, 43, 40)))
db.session.add(
    Post(uid=169, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=250, c2_number=36, league="Standard",
         name="Onion King", time=datetime.datetime(2016, 3, 7, 3, 17, 51)))
db.session.add(
    Post(uid=170, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=140, c2_number=178, league="Standard",
         name="Yellow Menace", time=datetime.datetime(2016, 9, 19, 18, 42, 14)))
db.session.add(Post(uid=171, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=281, c2_number=226,
                    league="Standard", name="High Kingdom Warrior", time=datetime.datetime(2016, 11, 26, 16, 12, 34)))
db.session.add(
    Post(uid=172, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=50, c2_number=111, league="Standard",
         name="Osprey", time=datetime.datetime(2016, 3, 10, 7, 49, 42)))
db.session.add(
    Post(uid=173, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=220, c2_number=268, league="Standard",
         name="Zero Charisma", time=datetime.datetime(2016, 3, 6, 15, 55, 56)))
db.session.add(
    Post(uid=174, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=283, c2_number=33, league="Standard",
         name="Highlander Monk", time=datetime.datetime(2016, 7, 1, 8, 39, 51)))
db.session.add(
    Post(uid=175, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=249, c2_number=276, league="Standard",
         name="Overrun", time=datetime.datetime(2016, 8, 4, 15, 25, 15)))
db.session.add(
    Post(uid=176, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=25, c2_number=89, league="Standard",
         name="Zesty Dragon", time=datetime.datetime(2016, 1, 1, 6, 45, 38)))
db.session.add(
    Post(uid=177, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=311, c2_number=170, league="Standard",
         name="Zod", time=datetime.datetime(2016, 4, 10, 10, 45, 6)))
db.session.add(
    Post(uid=0, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=132, c2_number=28, league="Standard",
         name="101", time=datetime.datetime(2016, 8, 28, 8, 51, 40)))
db.session.add(
    Post(uid=1, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=305, c2_number=51, league="Standard",
         name="Houston", time=datetime.datetime(2016, 10, 24, 2, 4, 39)))
db.session.add(
    Post(uid=2, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=318, c2_number=113, league="Standard",
         name="Pinball Wizard", time=datetime.datetime(2016, 11, 19, 2, 40, 37)))
db.session.add(
    Post(uid=3, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=274, c2_number=311, league="Standard",
         name="Accidental Genius", time=datetime.datetime(2016, 6, 18, 7, 28, 0)))
db.session.add(
    Post(uid=4, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=169, c2_number=309, league="Standard",
         name="Hyper", time=datetime.datetime(2016, 12, 23, 1, 2, 40)))
db.session.add(
    Post(uid=5, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=122, c2_number=254, league="Standard",
         name="Pluto", time=datetime.datetime(2016, 10, 17, 5, 57, 37)))
db.session.add(
    Post(uid=6, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=153, c2_number=305, league="Standard",
         name="Alpha", time=datetime.datetime(2016, 8, 11, 0, 38, 50)))
db.session.add(
    Post(uid=7, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=214, c2_number=153, league="Standard",
         name="Jester", time=datetime.datetime(2016, 7, 11, 9, 27, 50)))
db.session.add(
    Post(uid=8, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=211, c2_number=313, league="Standard",
         name="Pogue", time=datetime.datetime(2016, 3, 28, 11, 58, 31)))
db.session.add(
    Post(uid=9, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=102, c2_number=177, league="Standard",
         name="Airport Hobo", time=datetime.datetime(2016, 5, 10, 4, 49, 33)))
db.session.add(Post(uid=10, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=235, c2_number=180, league="Standard",
                    name="Jigsaw", time=datetime.datetime(2016, 4, 26, 8, 10, 40)))
db.session.add(
    Post(uid=11, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=209, c2_number=24, league="Standard",
         name="Prometheus", time=datetime.datetime(2016, 5, 2, 3, 14, 51)))
db.session.add(Post(uid=12, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=262, c2_number=283, league="Standard",
                    name="Bearded Angler", time=datetime.datetime(2016, 1, 1, 19, 55, 31)))
db.session.add(
    Post(uid=13, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=107, c2_number=96, league="Standard",
         name="Joker's Grin", time=datetime.datetime(2016, 8, 17, 12, 8, 52)))
db.session.add(Post(uid=14, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=249, c2_number=281, league="Standard",
                    name="Psycho Thinker", time=datetime.datetime(2016, 7, 9, 15, 18, 18)))
db.session.add(Post(uid=15, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=135, c2_number=60, league="Standard",
                    name="Beetle King", time=datetime.datetime(2016, 6, 3, 9, 41, 29)))
db.session.add(
    Post(uid=16, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=263, c2_number=59, league="Standard",
         name="Judge", time=datetime.datetime(2016, 4, 19, 3, 12, 52)))
db.session.add(
    Post(uid=17, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=319, c2_number=98, league="Standard",
         name="Pusher", time=datetime.datetime(2016, 9, 17, 10, 10, 4)))
db.session.add(
    Post(uid=18, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=155, c2_number=163, league="Standard",
         name="Bitmap", time=datetime.datetime(2016, 1, 10, 14, 15, 24)))
db.session.add(
    Post(uid=19, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=121, c2_number=71, league="Standard",
         name="Junkyard Dog", time=datetime.datetime(2016, 7, 23, 17, 3, 25)))
db.session.add(
    Post(uid=20, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=219, c2_number=295, league="Standard",
         name="Riff Raff", time=datetime.datetime(2016, 12, 13, 3, 31, 20)))
db.session.add(
    Post(uid=21, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=32, c2_number=296, league="Standard",
         name="Blister", time=datetime.datetime(2016, 3, 27, 21, 25, 10)))
db.session.add(
    Post(uid=22, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=221, c2_number=267, league="Standard",
         name="K-9", time=datetime.datetime(2016, 8, 23, 6, 42, 17)))
db.session.add(
    Post(uid=23, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=244, c2_number=28, league="Standard",
         name="Roadblock", time=datetime.datetime(2016, 4, 22, 10, 0, 45)))
db.session.add(Post(uid=24, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=148, c2_number=293, league="Standard",
                    name="Bowie", time=datetime.datetime(2016, 10, 19, 16, 42, 33)))
db.session.add(Post(uid=25, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=21, c2_number=248, league="Standard",
                    name="Keystone", time=datetime.datetime(2016, 10, 15, 3, 2, 42)))
db.session.add(
    Post(uid=26, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=103, c2_number=98, league="Standard",
         name="Rooster", time=datetime.datetime(2016, 12, 7, 21, 27, 27)))
db.session.add(Post(uid=27, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=292, c2_number=240, league="Standard",
                    name="Bowler", time=datetime.datetime(2016, 2, 6, 16, 25, 38)))
db.session.add(Post(uid=28, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=157, c2_number=116, league="Standard",
                    name="Kickstart", time=datetime.datetime(2016, 7, 19, 19, 14, 2)))
db.session.add(
    Post(uid=29, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=88, c2_number=176, league="Standard",
         name="Sandbox", time=datetime.datetime(2016, 4, 6, 19, 37, 4)))
db.session.add(Post(uid=30, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=48, c2_number=285, league="Standard",
                    name="Breadmaker", time=datetime.datetime(2016, 12, 13, 9, 7, 45)))
db.session.add(Post(uid=31, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=62, c2_number=58, league="Standard",
                    name="Kill Switch", time=datetime.datetime(2016, 1, 18, 16, 12, 1)))
db.session.add(Post(uid=32, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=244, c2_number=78, league="Standard",
                    name="Scrapper", time=datetime.datetime(2016, 2, 3, 7, 13, 14)))
db.session.add(Post(uid=33, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=133, c2_number=210, league="Standard",
                    name="Broomspun", time=datetime.datetime(2016, 7, 4, 20, 17, 55)))
db.session.add(
    Post(uid=34, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=157, c2_number=70, league="Standard",
         name="Kingfisher", time=datetime.datetime(2016, 8, 14, 4, 17, 3)))
db.session.add(
    Post(uid=35, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=162, c2_number=88, league="Standard",
         name="Screwtape", time=datetime.datetime(2016, 2, 2, 11, 38, 3)))
db.session.add(
    Post(uid=36, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=132, c2_number=259, league="Standard",
         name="Buckshot", time=datetime.datetime(2016, 12, 12, 14, 12, 40)))
db.session.add(
    Post(uid=37, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=182, c2_number=287, league="Standard",
         name="Kitchen", time=datetime.datetime(2016, 12, 16, 10, 50, 3)))
db.session.add(
    Post(uid=38, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=172, c2_number=193, league="Standard",
         name="Sexual Chocolate", time=datetime.datetime(2016, 5, 12, 10, 30, 21)))
db.session.add(
    Post(uid=39, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=221, c2_number=133, league="Standard",
         name="Bugger", time=datetime.datetime(2016, 10, 18, 14, 46, 21)))
db.session.add(Post(uid=40, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=30, c2_number=100, league="Standard",
                    name="Knuckles", time=datetime.datetime(2016, 10, 13, 10, 53, 48)))
db.session.add(
    Post(uid=41, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=189, c2_number=58, league="Standard",
         name="Shadow Chaser", time=datetime.datetime(2016, 3, 27, 14, 2, 8)))
db.session.add(
    Post(uid=42, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=34, c2_number=301, league="Standard", name="Cabbie",
         time=datetime.datetime(2016, 7, 12, 21, 49, 31)))
db.session.add(Post(uid=43, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=190, c2_number=114, league="Standard",
                    name="Lady Killer", time=datetime.datetime(2016, 1, 18, 9, 40, 4)))
db.session.add(
    Post(uid=44, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=182, c2_number=191, league="Standard",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 9, 13, 12, 15, 10)))
db.session.add(Post(uid=45, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=65, c2_number=238, league="Standard",
                    name="Candy Butcher", time=datetime.datetime(2016, 7, 22, 11, 29, 21)))
db.session.add(
    Post(uid=46, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=304, c2_number=224, league="Standard",
         name="Liquid Science", time=datetime.datetime(2016, 3, 13, 16, 42, 35)))
db.session.add(Post(uid=47, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=116, c2_number=58,
                    league="Standard", name="Shooter", time=datetime.datetime(2016, 11, 24, 16, 15, 45)))
db.session.add(
    Post(uid=48, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=202, c2_number=319, league="Standard",
         name="Capital F", time=datetime.datetime(2016, 10, 22, 14, 29, 30)))
db.session.add(
    Post(uid=49, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=49, c2_number=69, league="Standard",
         name="Little Cobra", time=datetime.datetime(2016, 7, 19, 7, 47, 25)))
db.session.add(
    Post(uid=50, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=81, c2_number=174, league="Standard",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 7, 10, 7, 33, 48)))
db.session.add(
    Post(uid=51, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=155, c2_number=204, league="Standard",
         name="Captain Peroxide", time=datetime.datetime(2016, 2, 1, 7, 47, 29)))
db.session.add(
    Post(uid=52, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=129, c2_number=110, league="Standard",
         name="Little General", time=datetime.datetime(2016, 8, 12, 14, 7, 23)))
db.session.add(
    Post(uid=53, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=267, c2_number=76, league="Standard",
         name="Skull Crusher", time=datetime.datetime(2016, 12, 16, 20, 20, 35)))
db.session.add(
    Post(uid=54, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=94, c2_number=144, league="Standard",
         name="Celtic Charger", time=datetime.datetime(2016, 3, 17, 2, 52, 21)))
db.session.add(
    Post(uid=55, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=56, c2_number=277, league="Standard",
         name="Lord Nikon", time=datetime.datetime(2016, 2, 18, 14, 45, 36)))
db.session.add(
    Post(uid=56, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=76, c2_number=215, league="Standard",
         name="Sky Bully", time=datetime.datetime(2016, 8, 19, 8, 5, 30)))
db.session.add(
    Post(uid=57, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=64, c2_number=65, league="Standard",
         name="Cereal Killer", time=datetime.datetime(2016, 11, 3, 20, 30, 44)))
db.session.add(
    Post(uid=58, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=252, c2_number=70, league="Standard",
         name="Lord Pistachio", time=datetime.datetime(2016, 12, 28, 9, 40, 38)))
db.session.add(
    Post(uid=59, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=115, c2_number=228, league="Standard",
         name="Slow Trot", time=datetime.datetime(2016, 12, 15, 4, 21, 47)))
db.session.add(
    Post(uid=60, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=262, c2_number=151, league="Standard",
         name="Chicago Blackout", time=datetime.datetime(2016, 3, 5, 10, 29, 43)))
db.session.add(
    Post(uid=61, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=311, c2_number=257, league="Standard",
         name="Mad Irishman", time=datetime.datetime(2016, 4, 4, 17, 51, 57)))
db.session.add(
    Post(uid=62, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=78, c2_number=26, league="Standard",
         name="Snake Eyes", time=datetime.datetime(2016, 2, 17, 2, 10, 12)))
db.session.add(
    Post(uid=63, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=55, c2_number=208, league="Standard",
         name="Chocolate Thunder", time=datetime.datetime(2016, 1, 13, 13, 4, 23)))
db.session.add(
    Post(uid=64, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=113, c2_number=303, league="Standard",
         name="Mad Jack", time=datetime.datetime(2016, 9, 5, 20, 45, 19)))
db.session.add(
    Post(uid=65, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=93, c2_number=55, league="Standard",
         name="Snow Hound", time=datetime.datetime(2016, 7, 10, 12, 51, 1)))
db.session.add(Post(uid=66, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=318, c2_number=72, league="Standard",
                    name="Chuckles", time=datetime.datetime(2016, 4, 14, 21, 29, 40)))
db.session.add(
    Post(uid=67, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=120, c2_number=296, league="Standard",
         name="Mad Rascal", time=datetime.datetime(2016, 8, 8, 13, 1, 52)))
db.session.add(
    Post(uid=68, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=158, c2_number=228, league="Standard",
         name="Sofa King", time=datetime.datetime(2016, 6, 20, 5, 25, 7)))
db.session.add(Post(uid=69, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=95, c2_number=96, league="Standard",
                    name="Commando", time=datetime.datetime(2016, 9, 18, 16, 29, 34)))
db.session.add(
    Post(uid=70, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=179, c2_number=73, league="Standard",
         name="Manimal", time=datetime.datetime(2016, 1, 9, 0, 53, 9)))
db.session.add(
    Post(uid=71, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=118, c2_number=20, league="Standard",
         name="Speedwell", time=datetime.datetime(2016, 2, 24, 22, 40, 25)))
db.session.add(
    Post(uid=72, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=270, c2_number=85, league="Standard",
         name="Cool Whip", time=datetime.datetime(2016, 7, 15, 22, 14, 12)))
db.session.add(
    Post(uid=73, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=299, c2_number=309, league="Standard",
         name="Marbles", time=datetime.datetime(2016, 2, 26, 17, 31, 26)))
db.session.add(
    Post(uid=74, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=135, c2_number=172, league="Standard",
         name="Spider Fuji", time=datetime.datetime(2016, 4, 18, 14, 43, 3)))
db.session.add(
    Post(uid=75, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=268, c2_number=293, league="Standard",
         name="Cosmo", time=datetime.datetime(2016, 2, 22, 14, 10, 37)))
db.session.add(
    Post(uid=76, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=187, c2_number=228, league="Standard",
         name="Married Man", time=datetime.datetime(2016, 1, 15, 13, 56, 4)))
db.session.add(
    Post(uid=77, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=168, c2_number=59, league="Standard",
         name="Springheel Jack", time=datetime.datetime(2016, 2, 23, 20, 17, 18)))
db.session.add(Post(uid=78, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=49, c2_number=210, league="Standard",
                    name="Crash Override", time=datetime.datetime(2016, 8, 14, 20, 40, 15)))
db.session.add(Post(uid=79, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=21, c2_number=118, league="Standard",
                    name="Marshmallow", time=datetime.datetime(2016, 9, 15, 6, 50, 44)))
db.session.add(
    Post(uid=80, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=269, c2_number=272, league="Standard",
         name="Squatch", time=datetime.datetime(2016, 4, 9, 8, 9, 3)))
db.session.add(
    Post(uid=81, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=93, c2_number=265, league="Standard",
         name="Crash Test", time=datetime.datetime(2016, 5, 4, 9, 18, 3)))
db.session.add(Post(uid=82, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=81, c2_number=83, league="Hardcore",
                    name="Mental", time=datetime.datetime(2016, 7, 6, 14, 45, 44)))
db.session.add(
    Post(uid=83, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=33, c2_number=246, league="Hardcore",
         name="Stacker of Wheat", time=datetime.datetime(2016, 11, 2, 21, 32, 4)))
db.session.add(Post(uid=84, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=126, c2_number=314, league="Hardcore",
                    name="Crazy Eights", time=datetime.datetime(2016, 6, 23, 1, 12, 30)))
db.session.add(
    Post(uid=85, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=26, c2_number=166, league="Hardcore",
         name="Mercury Reborn", time=datetime.datetime(2016, 2, 16, 15, 32, 19)))
db.session.add(Post(uid=86, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=168, c2_number=24, league="Hardcore",
                    name="Sugar Man", time=datetime.datetime(2016, 1, 1, 2, 0, 54)))
db.session.add(
    Post(uid=87, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=272, c2_number=233, league="Hardcore",
         name="Criss Cross", time=datetime.datetime(2016, 3, 20, 19, 33, 49)))
db.session.add(
    Post(uid=88, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=128, c2_number=84, league="Hardcore",
         name="Midas", time=datetime.datetime(2016, 3, 15, 20, 23, 47)))
db.session.add(
    Post(uid=89, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=78, c2_number=267, league="Hardcore",
         name="Suicide Jockey", time=datetime.datetime(2016, 10, 19, 6, 14, 11)))
db.session.add(
    Post(uid=90, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=32, c2_number=127, league="Hardcore",
         name="Cross Thread", time=datetime.datetime(2016, 9, 16, 5, 11, 56)))
db.session.add(
    Post(uid=91, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=104, c2_number=106, league="Hardcore",
         name="Midnight Rambler", time=datetime.datetime(2016, 8, 20, 21, 15, 22)))
db.session.add(
    Post(uid=92, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=176, c2_number=301, league="Hardcore",
         name="Swampmasher", time=datetime.datetime(2016, 9, 6, 5, 11, 21)))
db.session.add(
    Post(uid=93, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=219, c2_number=294, league="Hardcore",
         name="Cujo", time=datetime.datetime(2016, 5, 5, 9, 6, 12)))
db.session.add(
    Post(uid=94, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=31, c2_number=255, league="Hardcore",
         name="Midnight Rider", time=datetime.datetime(2016, 11, 28, 13, 22, 44)))
db.session.add(
    Post(uid=95, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=26, c2_number=25, league="Hardcore",
         name="Swerve", time=datetime.datetime(2016, 9, 3, 12, 58, 32)))
db.session.add(Post(uid=96, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=304, c2_number=31, league="Hardcore",
                    name="Dancing Madman", time=datetime.datetime(2016, 11, 18, 8, 1, 28)))
db.session.add(Post(uid=97, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=235, c2_number=272, league="Hardcore",
                    name="Mindless Bobcat", time=datetime.datetime(2016, 1, 19, 18, 6, 19)))
db.session.add(
    Post(uid=98, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=130, c2_number=273, league="Hardcore",
         name="Tacklebox", time=datetime.datetime(2016, 9, 8, 6, 1, 26)))
db.session.add(
    Post(uid=99, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=128, c2_number=37, league="Hardcore",
         name="Dangle", time=datetime.datetime(2016, 6, 5, 4, 37, 52)))
db.session.add(Post(uid=100, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=155, c2_number=115,
                    league="Hardcore", name="Mr. 44", time=datetime.datetime(2016, 11, 25, 22, 54, 54)))
db.session.add(
    Post(uid=101, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=39, c2_number=202,
         league="Hardcore", name="Take Away", time=datetime.datetime(2016, 10, 14, 10, 10, 8)))
db.session.add(
    Post(uid=102, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=306, c2_number=231, league="Hardcore",
         name="Dark Horse", time=datetime.datetime(2016, 9, 20, 19, 7, 34)))
db.session.add(Post(uid=103, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=76, c2_number=235,
                    league="Hardcore", name="Mr. Fabulous", time=datetime.datetime(2016, 3, 4, 0, 38, 20)))
db.session.add(Post(uid=104, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=246, c2_number=206,
                    league="Hardcore", name="Tan Stallion", time=datetime.datetime(2016, 9, 13, 16, 24, 55)))
db.session.add(Post(uid=105, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=245, c2_number=280,
                    league="Hardcore", name="Day Hawk", time=datetime.datetime(2016, 4, 19, 14, 1, 44)))
db.session.add(Post(uid=106, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=67, c2_number=139,
                    league="Hardcore", name="Mr. Gadget", time=datetime.datetime(2016, 4, 26, 4, 43, 23)))
db.session.add(Post(uid=107, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=227, c2_number=250,
                    league="Hardcore", name="The China Wall", time=datetime.datetime(2016, 10, 19, 13, 34, 34)))
db.session.add(Post(uid=108, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=201, c2_number=149,
                    league="Hardcore", name="Desert Haze", time=datetime.datetime(2016, 8, 24, 16, 47, 44)))
db.session.add(Post(uid=109, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=21, c2_number=140,
                    league="Hardcore", name="Mr. Lucky", time=datetime.datetime(2016, 1, 28, 0, 21, 39)))
db.session.add(Post(uid=110, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=27, c2_number=111,
                    league="Hardcore", name="The Dude", time=datetime.datetime(2016, 8, 27, 17, 25, 41)))
db.session.add(Post(uid=111, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=235, c2_number=168,
                    league="Hardcore", name="Digger", time=datetime.datetime(2016, 4, 15, 10, 34, 7)))
db.session.add(Post(uid=112, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=239, c2_number=162,
                    league="Hardcore", name="Mr. Peppermint", time=datetime.datetime(2016, 12, 18, 18, 39, 7)))
db.session.add(Post(uid=113, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=132, c2_number=77,
                    league="Hardcore", name="The Flying Mouse", time=datetime.datetime(2016, 4, 13, 7, 57, 41)))
db.session.add(
    Post(uid=114, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=301, c2_number=166, league="Hardcore",
         name="Disco Thunder", time=datetime.datetime(2016, 10, 17, 10, 49, 12)))
db.session.add(
    Post(uid=115, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=148, c2_number=121, league="Hardcore",
         name="Mr. Spy", time=datetime.datetime(2016, 3, 26, 3, 42, 13)))
db.session.add(Post(uid=116, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=126, c2_number=73,
                    league="Hardcore", name="The Happy Jock", time=datetime.datetime(2016, 7, 12, 13, 28, 33)))
db.session.add(Post(uid=117, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=290, c2_number=277,
                    league="Hardcore", name="Disco Potato", time=datetime.datetime(2016, 12, 22, 10, 1, 4)))
db.session.add(Post(uid=118, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=62, c2_number=91, league="Hardcore",
                    name="Mr. Thanksgiving", time=datetime.datetime(2016, 7, 26, 20, 57, 37)))
db.session.add(
    Post(uid=119, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=304, c2_number=268, league="Hardcore",
         name="The Howling Swede", time=datetime.datetime(2016, 5, 25, 11, 13, 45)))
db.session.add(Post(uid=120, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=106, c2_number=152, league="Hardcore",
                    name="Dr. Cocktail", time=datetime.datetime(2016, 11, 2, 21, 36, 44)))
db.session.add(
    Post(uid=121, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=81, c2_number=191, league="Hardcore",
         name="Mr. Wholesome", time=datetime.datetime(2016, 6, 3, 22, 25, 13)))
db.session.add(Post(uid=122, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=255, c2_number=55, league="Hardcore",
                    name="Thrasher", time=datetime.datetime(2016, 10, 3, 13, 32, 25)))
db.session.add(
    Post(uid=123, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=158, c2_number=289, league="Hardcore",
         name="Dredd", time=datetime.datetime(2016, 12, 20, 18, 54, 39)))
db.session.add(
    Post(uid=124, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=300, c2_number=163, league="Hardcore",
         name="Mud Pie Man", time=datetime.datetime(2016, 7, 21, 7, 15, 16)))
db.session.add(
    Post(uid=125, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=238, c2_number=291, league="Hardcore",
         name="Toe", time=datetime.datetime(2016, 12, 5, 2, 6, 21)))
db.session.add(
    Post(uid=126, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=172, c2_number=177, league="Hardcore",
         name="Dropkick", time=datetime.datetime(2016, 1, 20, 20, 28, 52)))
db.session.add(
    Post(uid=127, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=74, c2_number=28, league="Hardcore",
         name="Mule Skinner", time=datetime.datetime(2016, 4, 17, 12, 31, 22)))
db.session.add(
    Post(uid=128, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=95, c2_number=44, league="Hardcore",
         name="Toolmaker", time=datetime.datetime(2016, 12, 6, 17, 41, 10)))
db.session.add(
    Post(uid=129, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=165, c2_number=301, league="Hardcore",
         name="Drop Stone", time=datetime.datetime(2016, 8, 11, 4, 32, 36)))
db.session.add(
    Post(uid=130, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=82, c2_number=201, league="Hardcore",
         name="Murmur", time=datetime.datetime(2016, 10, 1, 21, 49, 47)))
db.session.add(
    Post(uid=131, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=95, c2_number=109, league="Hardcore",
         name="Tough Nut", time=datetime.datetime(2016, 12, 9, 3, 22, 12)))
db.session.add(Post(uid=132, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=143, c2_number=259, league="Hardcore",
                    name="Drugstore Cowboy", time=datetime.datetime(2016, 3, 16, 0, 57, 17)))
db.session.add(Post(uid=133, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=294, c2_number=192, league="Hardcore",
                    name="Nacho", time=datetime.datetime(2016, 8, 20, 3, 58, 13)))
db.session.add(
    Post(uid=134, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=151, c2_number=27, league="Hardcore",
         name="Trip", time=datetime.datetime(2016, 5, 23, 7, 11, 32)))
db.session.add(
    Post(uid=135, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=216, c2_number=156, league="Hardcore",
         name="Easy Sweep", time=datetime.datetime(2016, 6, 15, 13, 53, 6)))
db.session.add(
    Post(uid=136, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=62, c2_number=54, league="Hardcore",
         name="Natural Mess", time=datetime.datetime(2016, 10, 17, 13, 42, 11)))
db.session.add(Post(uid=137, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=174, c2_number=153,
                    league="Hardcore", name="Troubadour", time=datetime.datetime(2016, 3, 23, 21, 28, 18)))
db.session.add(
    Post(uid=138, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=296, c2_number=283, league="Hardcore",
         name="Electric Player", time=datetime.datetime(2016, 4, 21, 22, 6, 43)))
db.session.add(
    Post(uid=139, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=235, c2_number=318, league="Hardcore",
         name="Necromancer", time=datetime.datetime(2016, 10, 27, 9, 22, 3)))
db.session.add(
    Post(uid=140, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=264, c2_number=258, league="Hardcore",
         name="Turnip King", time=datetime.datetime(2016, 10, 17, 16, 5, 30)))
db.session.add(
    Post(uid=141, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=41, c2_number=268, league="Hardcore",
         name="Esquire", time=datetime.datetime(2016, 4, 12, 12, 13, 39)))
db.session.add(
    Post(uid=142, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=306, c2_number=222, league="Hardcore",
         name="Neophyte Believer", time=datetime.datetime(2016, 12, 4, 9, 29, 48)))
db.session.add(
    Post(uid=143, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=241, c2_number=270, league="Hardcore",
         name="Twitch", time=datetime.datetime(2016, 12, 17, 12, 45, 29)))
db.session.add(
    Post(uid=144, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=25, c2_number=41, league="Hardcore",
         name="Fast Draw", time=datetime.datetime(2016, 9, 23, 12, 16, 2)))
db.session.add(
    Post(uid=145, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=144, c2_number=270, league="Hardcore",
         name="Nessie", time=datetime.datetime(2016, 11, 19, 2, 44, 45)))
db.session.add(
    Post(uid=146, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=288, c2_number=284, league="Hardcore",
         name="Vagabond Warrior", time=datetime.datetime(2016, 3, 15, 9, 1, 10)))
db.session.add(
    Post(uid=147, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=237, c2_number=136, league="Hardcore",
         name="Flakes", time=datetime.datetime(2016, 4, 22, 12, 6, 5)))
db.session.add(
    Post(uid=148, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=282, c2_number=121, league="Hardcore",
         name="New Cycle", time=datetime.datetime(2016, 10, 9, 4, 4, 48)))
db.session.add(
    Post(uid=149, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=192, c2_number=194, league="Hardcore",
         name="Voluntary", time=datetime.datetime(2016, 9, 15, 3, 10, 11)))
db.session.add(
    Post(uid=150, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=225, c2_number=118, league="Hardcore",
         name="Flint", time=datetime.datetime(2016, 5, 2, 8, 51, 25)))
db.session.add(
    Post(uid=151, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=58, c2_number=305, league="Hardcore",
         name="Nickname Master", time=datetime.datetime(2016, 1, 7, 3, 46, 9)))
db.session.add(
    Post(uid=152, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=169, c2_number=184, league="Hardcore",
         name="Vortex", time=datetime.datetime(2016, 10, 12, 17, 17, 34)))
db.session.add(
    Post(uid=153, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=129, c2_number=156, league="Hardcore",
         name="Freak", time=datetime.datetime(2016, 11, 12, 17, 50, 21)))
db.session.add(Post(uid=154, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=95, c2_number=44, league="Hardcore",
                    name="Nightmare King", time=datetime.datetime(2016, 3, 26, 20, 14, 23)))
db.session.add(Post(uid=155, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=282, c2_number=306,
                    league="Hardcore", name="Washer", time=datetime.datetime(2016, 2, 11, 14, 31, 44)))
db.session.add(Post(uid=156, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=308, c2_number=129, league="Hardcore",
                    name="Gas Man", time=datetime.datetime(2016, 8, 25, 6, 33, 3)))
db.session.add(
    Post(uid=157, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=110, c2_number=114, league="Hardcore",
         name="Night Train", time=datetime.datetime(2016, 4, 18, 8, 42, 28)))
db.session.add(Post(uid=158, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=238, c2_number=85, league="Hardcore",
                    name="Waylay Dave", time=datetime.datetime(2016, 6, 24, 22, 38, 57)))
db.session.add(
    Post(uid=159, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=246, c2_number=56, league="Hardcore",
         name="Glyph", time=datetime.datetime(2016, 5, 9, 9, 13, 5)))
db.session.add(
    Post(uid=160, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=205, c2_number=202, league="Hardcore",
         name="Old Man Winter", time=datetime.datetime(2016, 7, 1, 6, 54, 45)))
db.session.add(
    Post(uid=161, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=242, c2_number=143, league="Hardcore",
         name="Wheels", time=datetime.datetime(2016, 9, 18, 15, 32, 36)))
db.session.add(
    Post(uid=162, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=281, c2_number=89, league="Hardcore",
         name="Grave Digger", time=datetime.datetime(2016, 8, 6, 0, 17, 6)))
db.session.add(
    Post(uid=163, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=208, c2_number=248, league="Hardcore",
         name="Old Orange Eyes", time=datetime.datetime(2016, 3, 18, 3, 45, 23)))
db.session.add(
    Post(uid=164, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=68, c2_number=120, league="Hardcore",
         name="Wooden Man", time=datetime.datetime(2016, 7, 22, 13, 50, 31)))
db.session.add(
    Post(uid=165, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=55, c2_number=309, league="Hardcore",
         name="Guillotine", time=datetime.datetime(2016, 11, 13, 8, 36, 11)))
db.session.add(
    Post(uid=166, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=171, c2_number=138, league="Hardcore",
         name="Old Regret", time=datetime.datetime(2016, 5, 2, 0, 52, 23)))
db.session.add(
    Post(uid=167, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=214, c2_number=83, league="Hardcore",
         name="Woo Woo", time=datetime.datetime(2016, 6, 1, 9, 57, 55)))
db.session.add(Post(uid=168, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=214, c2_number=110, league="Hardcore",
                    name="Gunhawk", time=datetime.datetime(2016, 2, 19, 20, 45, 40)))
db.session.add(Post(uid=169, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=287, c2_number=217, league="Hardcore",
                    name="Onion King", time=datetime.datetime(2016, 9, 23, 2, 18, 8)))
db.session.add(
    Post(uid=170, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=248, c2_number=277, league="Hardcore",
         name="Yellow Menace", time=datetime.datetime(2016, 8, 22, 12, 43, 16)))
db.session.add(
    Post(uid=171, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=310, c2_number=85, league="Hardcore",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 7, 4, 4, 52, 48)))
db.session.add(
    Post(uid=172, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=214, c2_number=115, league="Hardcore",
         name="Osprey", time=datetime.datetime(2016, 8, 3, 18, 31, 43)))
db.session.add(Post(uid=173, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=290, c2_number=312,
                    league="Hardcore", name="Zero Charisma", time=datetime.datetime(2016, 10, 10, 22, 24, 19)))
db.session.add(
    Post(uid=174, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=243, c2_number=212, league="Hardcore",
         name="Highlander Monk", time=datetime.datetime(2016, 5, 17, 17, 57, 15)))
db.session.add(
    Post(uid=175, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=41, c2_number=60, league="Hardcore",
         name="Overrun", time=datetime.datetime(2016, 5, 16, 1, 56, 2)))
db.session.add(
    Post(uid=176, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=51, c2_number=123, league="Hardcore",
         name="Zesty Dragon", time=datetime.datetime(2016, 7, 6, 3, 21, 46)))
db.session.add(
    Post(uid=177, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=143, c2_number=30, league="Hardcore",
         name="Zod", time=datetime.datetime(2016, 12, 13, 7, 2, 7)))
db.session.add(
    Post(uid=0, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=191, c2_number=48, league="Hardcore",
         name="101", time=datetime.datetime(2016, 4, 16, 22, 10, 8)))
db.session.add(
    Post(uid=1, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=66, c2_number=59, league="Hardcore",
         name="Houston", time=datetime.datetime(2016, 11, 5, 7, 53, 36)))
db.session.add(
    Post(uid=2, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=232, c2_number=282, league="Hardcore",
         name="Pinball Wizard", time=datetime.datetime(2016, 4, 14, 12, 33, 46)))
db.session.add(
    Post(uid=3, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=63, c2_number=215, league="Hardcore",
         name="Accidental Genius", time=datetime.datetime(2016, 6, 9, 21, 42, 9)))
db.session.add(
    Post(uid=4, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=67, c2_number=246, league="Hardcore",
         name="Hyper", time=datetime.datetime(2016, 1, 20, 17, 23, 16)))
db.session.add(
    Post(uid=5, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=179, c2_number=37, league="Hardcore",
         name="Pluto", time=datetime.datetime(2016, 2, 10, 11, 10, 54)))
db.session.add(
    Post(uid=6, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=170, c2_number=132, league="Hardcore",
         name="Alpha", time=datetime.datetime(2016, 2, 13, 5, 0, 6)))
db.session.add(
    Post(uid=7, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=72, c2_number=187, league="Hardcore",
         name="Jester", time=datetime.datetime(2016, 5, 15, 12, 5, 22)))
db.session.add(Post(uid=8, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=259, c2_number=280, league="Hardcore",
                    name="Pogue", time=datetime.datetime(2016, 3, 17, 4, 9, 29)))
db.session.add(Post(uid=9, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=92, c2_number=146, league="Hardcore",
                    name="Airport Hobo", time=datetime.datetime(2016, 4, 5, 3, 11, 21)))
db.session.add(
    Post(uid=10, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=65, c2_number=114, league="Hardcore",
         name="Jigsaw", time=datetime.datetime(2016, 9, 21, 12, 55, 44)))
db.session.add(
    Post(uid=11, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=164, c2_number=92, league="Hardcore",
         name="Prometheus", time=datetime.datetime(2016, 4, 5, 17, 17, 35)))
db.session.add(
    Post(uid=12, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=143, c2_number=65, league="Hardcore",
         name="Bearded Angler", time=datetime.datetime(2016, 2, 4, 22, 47, 37)))
db.session.add(Post(uid=13, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=196, c2_number=250,
                    league="Hardcore", name="Joker's Grin", time=datetime.datetime(2016, 5, 28, 6, 45, 47)))
db.session.add(
    Post(uid=14, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=197, c2_number=130, league="Hardcore",
         name="Psycho Thinker", time=datetime.datetime(2016, 6, 9, 6, 46, 40)))
db.session.add(
    Post(uid=15, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=165, c2_number=152, league="Hardcore",
         name="Beetle King", time=datetime.datetime(2016, 1, 15, 13, 58, 8)))
db.session.add(
    Post(uid=16, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=186, c2_number=189, league="Hardcore",
         name="Judge", time=datetime.datetime(2016, 6, 25, 8, 36, 24)))
db.session.add(
    Post(uid=17, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=150, c2_number=41, league="Hardcore",
         name="Pusher", time=datetime.datetime(2016, 3, 20, 5, 52, 15)))
db.session.add(Post(uid=18, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=294, c2_number=31,
                    league="Hardcore", name="Bitmap", time=datetime.datetime(2016, 12, 23, 20, 44, 52)))
db.session.add(
    Post(uid=19, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=222, c2_number=131, league="Hardcore",
         name="Junkyard Dog", time=datetime.datetime(2016, 3, 14, 14, 22, 42)))
db.session.add(
    Post(uid=20, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=155, c2_number=85, league="Hardcore",
         name="Riff Raff", time=datetime.datetime(2016, 11, 20, 4, 21, 49)))
db.session.add(Post(uid=21, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=187, c2_number=298,
                    league="Hardcore", name="Blister", time=datetime.datetime(2016, 8, 28, 15, 27, 10)))
db.session.add(
    Post(uid=22, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=64, c2_number=60, league="Hardcore",
         name="K-9", time=datetime.datetime(2016, 3, 17, 15, 7, 16)))
db.session.add(
    Post(uid=23, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=44, c2_number=227, league="Hardcore",
         name="Roadblock", time=datetime.datetime(2016, 7, 12, 21, 35, 3)))
db.session.add(
    Post(uid=24, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=20, c2_number=211, league="Hardcore",
         name="Bowie", time=datetime.datetime(2016, 1, 3, 3, 32, 30)))
db.session.add(
    Post(uid=25, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=161, c2_number=73, league="Hardcore",
         name="Keystone", time=datetime.datetime(2016, 3, 13, 13, 54, 19)))
db.session.add(
    Post(uid=26, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=44, c2_number=298, league="Hardcore",
         name="Rooster", time=datetime.datetime(2016, 10, 9, 4, 23, 22)))
db.session.add(
    Post(uid=27, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=277, c2_number=255, league="Hardcore",
         name="Bowler", time=datetime.datetime(2016, 10, 20, 4, 5, 51)))
db.session.add(
    Post(uid=28, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=125, c2_number=274, league="Hardcore",
         name="Kickstart", time=datetime.datetime(2016, 6, 1, 17, 2, 3)))
db.session.add(
    Post(uid=29, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=154, c2_number=74, league="Hardcore",
         name="Sandbox", time=datetime.datetime(2016, 4, 8, 17, 19, 25)))
db.session.add(
    Post(uid=30, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=191, c2_number=313, league="Hardcore",
         name="Breadmaker", time=datetime.datetime(2016, 7, 2, 0, 10, 18)))
db.session.add(Post(uid=31, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=298, c2_number=93,
                    league="Hardcore", name="Kill Switch", time=datetime.datetime(2016, 2, 16, 21, 29, 15)))
db.session.add(
    Post(uid=32, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=234, c2_number=270, league="Hardcore",
         name="Scrapper", time=datetime.datetime(2016, 12, 26, 15, 14, 53)))
db.session.add(
    Post(uid=33, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=187, c2_number=72, league="Hardcore",
         name="Broomspun", time=datetime.datetime(2016, 11, 3, 20, 43, 28)))
db.session.add(
    Post(uid=34, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=229, c2_number=52, league="Hardcore",
         name="Kingfisher", time=datetime.datetime(2016, 4, 12, 5, 9, 18)))
db.session.add(
    Post(uid=35, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=62, c2_number=156, league="Hardcore",
         name="Screwtape", time=datetime.datetime(2016, 1, 1, 14, 54, 4)))
db.session.add(
    Post(uid=36, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=67, c2_number=44, league="Hardcore",
         name="Buckshot", time=datetime.datetime(2016, 7, 12, 8, 17, 23)))
db.session.add(
    Post(uid=37, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=266, c2_number=115, league="Hardcore",
         name="Kitchen", time=datetime.datetime(2016, 2, 21, 14, 10, 10)))
db.session.add(
    Post(uid=38, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=267, c2_number=285, league="Hardcore",
         name="Sexual Chocolate", time=datetime.datetime(2016, 6, 16, 16, 9, 33)))
db.session.add(
    Post(uid=39, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=294, c2_number=302, league="Hardcore",
         name="Bugger", time=datetime.datetime(2016, 11, 25, 6, 53, 27)))
db.session.add(
    Post(uid=40, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=225, c2_number=311, league="Hardcore",
         name="Knuckles", time=datetime.datetime(2016, 4, 9, 20, 2, 13)))
db.session.add(
    Post(uid=41, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=192, c2_number=183, league="Hardcore",
         name="Shadow Chaser", time=datetime.datetime(2016, 4, 21, 12, 38, 54)))
db.session.add(
    Post(uid=42, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=27, c2_number=174, league="Hardcore",
         name="Cabbie", time=datetime.datetime(2016, 2, 26, 8, 24, 39)))
db.session.add(
    Post(uid=43, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=265, c2_number=191, league="Hardcore",
         name="Lady Killer", time=datetime.datetime(2016, 7, 2, 0, 31, 20)))
db.session.add(
    Post(uid=44, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=148, c2_number=267, league="Hardcore",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 5, 26, 18, 17, 27)))
db.session.add(
    Post(uid=45, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=130, c2_number=311, league="Hardcore",
         name="Candy Butcher", time=datetime.datetime(2016, 10, 18, 17, 31, 49)))
db.session.add(
    Post(uid=46, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=161, c2_number=290, league="Hardcore",
         name="Liquid Science", time=datetime.datetime(2016, 6, 3, 4, 7, 50)))
db.session.add(
    Post(uid=47, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=319, c2_number=293, league="Hardcore",
         name="Shooter", time=datetime.datetime(2016, 1, 20, 22, 17, 11)))
db.session.add(
    Post(uid=48, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=221, c2_number=155, league="Hardcore",
         name="Capital F", time=datetime.datetime(2016, 6, 6, 18, 28, 21)))
db.session.add(Post(uid=49, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=201, c2_number=221,
                    league="Hardcore", name="Little Cobra", time=datetime.datetime(2016, 2, 5, 18, 44, 55)))
db.session.add(
    Post(uid=50, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=63, c2_number=23, league="Hardcore",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 10, 25, 12, 10, 48)))
db.session.add(
    Post(uid=51, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=263, c2_number=311, league="Hardcore",
         name="Captain Peroxide", time=datetime.datetime(2016, 5, 4, 14, 33, 36)))
db.session.add(
    Post(uid=52, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=166, c2_number=21, league="Hardcore",
         name="Little General", time=datetime.datetime(2016, 6, 26, 4, 44, 7)))
db.session.add(
    Post(uid=53, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=142, c2_number=185, league="Hardcore",
         name="Skull Crusher", time=datetime.datetime(2016, 4, 4, 2, 5, 30)))
db.session.add(
    Post(uid=54, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=288, c2_number=180, league="Hardcore",
         name="Celtic Charger", time=datetime.datetime(2016, 5, 6, 8, 57, 5)))
db.session.add(
    Post(uid=55, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=132, c2_number=36, league="Hardcore",
         name="Lord Nikon", time=datetime.datetime(2016, 8, 22, 6, 40, 55)))
db.session.add(
    Post(uid=56, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=51, c2_number=300, league="Hardcore",
         name="Sky Bully", time=datetime.datetime(2016, 6, 18, 14, 22, 46)))
db.session.add(
    Post(uid=57, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=302, c2_number=205, league="Hardcore",
         name="Cereal Killer", time=datetime.datetime(2016, 2, 20, 18, 35, 47)))
db.session.add(
    Post(uid=58, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=39, c2_number=56, league="Hardcore",
         name="Lord Pistachio", time=datetime.datetime(2016, 12, 24, 2, 48, 44)))
db.session.add(
    Post(uid=59, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=48, c2_number=311, league="Hardcore",
         name="Slow Trot", time=datetime.datetime(2016, 11, 18, 8, 53, 32)))
db.session.add(
    Post(uid=60, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=178, c2_number=231, league="Hardcore",
         name="Chicago Blackout", time=datetime.datetime(2016, 1, 4, 8, 42, 18)))
db.session.add(
    Post(uid=61, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=197, c2_number=135, league="Hardcore",
         name="Mad Irishman", time=datetime.datetime(2016, 4, 23, 5, 21, 7)))
db.session.add(
    Post(uid=62, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=290, c2_number=116, league="Hardcore",
         name="Snake Eyes", time=datetime.datetime(2016, 10, 12, 12, 38, 11)))
db.session.add(
    Post(uid=63, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=221, c2_number=238, league="Hardcore",
         name="Chocolate Thunder", time=datetime.datetime(2016, 5, 3, 20, 8, 35)))
db.session.add(
    Post(uid=64, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=260, c2_number=286, league="Hardcore",
         name="Mad Jack", time=datetime.datetime(2016, 1, 6, 11, 9, 42)))
db.session.add(
    Post(uid=65, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=74, c2_number=300, league="Hardcore",
         name="Snow Hound", time=datetime.datetime(2016, 8, 20, 22, 3, 22)))
db.session.add(
    Post(uid=66, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=241, c2_number=175, league="Hardcore",
         name="Chuckles", time=datetime.datetime(2016, 2, 4, 8, 4, 49)))
db.session.add(Post(uid=67, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=75, c2_number=236,
                    league="Hardcore", name="Mad Rascal", time=datetime.datetime(2016, 4, 6, 0, 53, 37)))
db.session.add(
    Post(uid=68, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=49, c2_number=44, league="Hardcore",
         name="Sofa King", time=datetime.datetime(2016, 1, 4, 18, 17, 29)))
db.session.add(
    Post(uid=69, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=169, c2_number=107, league="Hardcore",
         name="Commando", time=datetime.datetime(2016, 2, 21, 13, 34, 28)))
db.session.add(
    Post(uid=70, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=108, c2_number=296, league="Hardcore",
         name="Manimal", time=datetime.datetime(2016, 10, 15, 11, 50, 41)))
db.session.add(
    Post(uid=71, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=121, c2_number=287, league="Hardcore",
         name="Speedwell", time=datetime.datetime(2016, 1, 19, 15, 56, 33)))
db.session.add(Post(uid=72, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=60, c2_number=289,
                    league="Hardcore", name="Cool Whip", time=datetime.datetime(2016, 1, 14, 20, 27, 25)))
db.session.add(
    Post(uid=73, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=30, c2_number=271, league="Hardcore",
         name="Marbles", time=datetime.datetime(2016, 9, 10, 11, 9, 48)))
db.session.add(
    Post(uid=74, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=208, c2_number=280, league="Hardcore",
         name="Spider Fuji", time=datetime.datetime(2016, 7, 22, 17, 41, 9)))
db.session.add(Post(uid=75, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=27, c2_number=170,
                    league="Hardcore", name="Cosmo", time=datetime.datetime(2016, 6, 6, 17, 18, 55)))
db.session.add(
    Post(uid=76, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=215, c2_number=60, league="Hardcore",
         name="Married Man", time=datetime.datetime(2016, 2, 8, 17, 48, 52)))
db.session.add(
    Post(uid=77, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=311, c2_number=30, league="Hardcore",
         name="Springheel Jack", time=datetime.datetime(2016, 6, 3, 13, 15, 53)))
db.session.add(
    Post(uid=78, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=68, c2_number=124, league="Hardcore",
         name="Crash Override", time=datetime.datetime(2016, 6, 7, 0, 32, 21)))
db.session.add(
    Post(uid=79, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=213, c2_number=81, league="Hardcore",
         name="Marshmallow", time=datetime.datetime(2016, 12, 21, 21, 43, 29)))
db.session.add(
    Post(uid=80, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=155, c2_number=305, league="Hardcore",
         name="Squatch", time=datetime.datetime(2016, 4, 27, 13, 0, 19)))
db.session.add(
    Post(uid=81, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=306, c2_number=133, league="Hardcore",
         name="Crash Test", time=datetime.datetime(2016, 12, 10, 12, 44, 18)))
db.session.add(
    Post(uid=82, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=237, c2_number=232, league="Hardcore",
         name="Mental", time=datetime.datetime(2016, 4, 7, 5, 31, 29)))
db.session.add(
    Post(uid=83, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=254, c2_number=197, league="Hardcore",
         name="Stacker of Wheat", time=datetime.datetime(2016, 4, 26, 19, 50, 42)))
db.session.add(
    Post(uid=84, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=58, c2_number=205, league="Hardcore",
         name="Crazy Eights", time=datetime.datetime(2016, 4, 22, 15, 7, 34)))
db.session.add(Post(uid=85, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=112, c2_number=131,
                    league="Hardcore", name="Mercury Reborn", time=datetime.datetime(2016, 7, 2, 15, 5, 18)))
db.session.add(
    Post(uid=86, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=299, c2_number=96, league="Hardcore",
         name="Sugar Man", time=datetime.datetime(2016, 6, 10, 15, 23, 37)))
db.session.add(
    Post(uid=87, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=312, c2_number=293, league="Hardcore",
         name="Criss Cross", time=datetime.datetime(2016, 3, 20, 6, 4, 17)))
db.session.add(
    Post(uid=88, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=281, c2_number=63, league="Hardcore",
         name="Midas", time=datetime.datetime(2016, 10, 2, 16, 47, 55)))
db.session.add(
    Post(uid=89, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=243, c2_number=136, league="Hardcore",
         name="Suicide Jockey", time=datetime.datetime(2016, 9, 14, 17, 26, 40)))
db.session.add(
    Post(uid=90, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=78, c2_number=127, league="Hardcore",
         name="Cross Thread", time=datetime.datetime(2016, 4, 2, 20, 32, 34)))
db.session.add(
    Post(uid=91, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=138, c2_number=215, league="Hardcore",
         name="Midnight Rambler", time=datetime.datetime(2016, 5, 20, 17, 4, 48)))
db.session.add(
    Post(uid=92, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=256, c2_number=228, league="Hardcore",
         name="Swampmasher", time=datetime.datetime(2016, 8, 5, 5, 52, 18)))
db.session.add(
    Post(uid=93, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=226, c2_number=226, league="Hardcore",
         name="Cujo", time=datetime.datetime(2016, 7, 4, 14, 38, 45)))
db.session.add(
    Post(uid=94, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=153, c2_number=116, league="Hardcore",
         name="Midnight Rider", time=datetime.datetime(2016, 1, 11, 13, 38, 16)))
db.session.add(
    Post(uid=95, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=140, c2_number=167, league="Hardcore",
         name="Swerve", time=datetime.datetime(2016, 12, 14, 11, 47, 5)))
db.session.add(
    Post(uid=96, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=256, c2_number=157, league="Hardcore",
         name="Dancing Madman", time=datetime.datetime(2016, 1, 5, 11, 43, 30)))
db.session.add(
    Post(uid=97, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=230, c2_number=115, league="Hardcore",
         name="Mindless Bobcat", time=datetime.datetime(2016, 11, 28, 22, 54, 29)))
db.session.add(Post(uid=98, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=29, c2_number=73, league="Hardcore",
                    name="Tacklebox", time=datetime.datetime(2016, 6, 6, 2, 16, 7)))
db.session.add(
    Post(uid=99, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=295, c2_number=236, league="Hardcore",
         name="Dangle", time=datetime.datetime(2016, 1, 15, 10, 25, 11)))
db.session.add(
    Post(uid=100, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=248, c2_number=44, league="Hardcore",
         name="Mr. 44", time=datetime.datetime(2016, 12, 16, 14, 8, 26)))
db.session.add(
    Post(uid=101, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=155, c2_number=138, league="Hardcore",
         name="Take Away", time=datetime.datetime(2016, 3, 21, 2, 37, 22)))
db.session.add(
    Post(uid=102, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=196, c2_number=76, league="Hardcore",
         name="Dark Horse", time=datetime.datetime(2016, 8, 25, 0, 10, 13)))
db.session.add(Post(uid=103, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=210, c2_number=130,
                    league="Hardcore", name="Mr. Fabulous", time=datetime.datetime(2016, 8, 2, 14, 45, 10)))
db.session.add(
    Post(uid=104, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=210, c2_number=186, league="Hardcore",
         name="Tan Stallion", time=datetime.datetime(2016, 8, 21, 18, 52, 12)))
db.session.add(
    Post(uid=105, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=20, c2_number=117, league="Hardcore",
         name="Day Hawk", time=datetime.datetime(2016, 5, 26, 16, 48, 57)))
db.session.add(
    Post(uid=106, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=126, c2_number=188, league="Hardcore",
         name="Mr. Gadget", time=datetime.datetime(2016, 6, 15, 17, 57, 49)))
db.session.add(
    Post(uid=107, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=314, c2_number=107, league="Hardcore",
         name="The China Wall", time=datetime.datetime(2016, 9, 4, 21, 58, 18)))
db.session.add(
    Post(uid=108, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=33, c2_number=256, league="Hardcore",
         name="Desert Haze", time=datetime.datetime(2016, 9, 9, 21, 30, 20)))
db.session.add(
    Post(uid=109, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=48, c2_number=193, league="Hardcore",
         name="Mr. Lucky", time=datetime.datetime(2016, 11, 18, 10, 10, 44)))
db.session.add(
    Post(uid=110, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=101, c2_number=173, league="Hardcore",
         name="The Dude", time=datetime.datetime(2016, 5, 23, 16, 43, 24)))
db.session.add(
    Post(uid=111, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=277, c2_number=89, league="Hardcore",
         name="Digger", time=datetime.datetime(2016, 1, 10, 11, 48, 11)))
db.session.add(
    Post(uid=112, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=266, c2_number=257, league="Hardcore",
         name="Mr. Peppermint", time=datetime.datetime(2016, 2, 14, 10, 51, 57)))
db.session.add(
    Post(uid=113, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=124, c2_number=72, league="Hardcore",
         name="The Flying Mouse", time=datetime.datetime(2016, 7, 5, 21, 28, 32)))
db.session.add(
    Post(uid=114, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=114, c2_number=173, league="Hardcore",
         name="Disco Thunder", time=datetime.datetime(2016, 2, 17, 10, 50, 25)))
db.session.add(
    Post(uid=115, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=290, c2_number=34, league="Hardcore",
         name="Mr. Spy", time=datetime.datetime(2016, 11, 6, 5, 13, 14)))
db.session.add(
    Post(uid=116, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=275, c2_number=246, league="Hardcore",
         name="The Happy Jock", time=datetime.datetime(2016, 6, 1, 4, 43, 20)))
db.session.add(
    Post(uid=117, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=60, c2_number=204, league="Hardcore",
         name="Disco Potato", time=datetime.datetime(2016, 12, 23, 16, 37, 11)))
db.session.add(
    Post(uid=118, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=248, c2_number=25, league="Hardcore",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 10, 8, 17, 36, 24)))
db.session.add(
    Post(uid=119, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=48, c2_number=232, league="Hardcore",
         name="The Howling Swede", time=datetime.datetime(2016, 4, 27, 8, 22, 0)))
db.session.add(
    Post(uid=120, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=280, c2_number=275, league="Hardcore",
         name="Dr. Cocktail", time=datetime.datetime(2016, 1, 19, 7, 29, 23)))
db.session.add(Post(uid=121, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=56, c2_number=262,
                    league="Hardcore", name="Mr. Wholesome", time=datetime.datetime(2016, 3, 23, 11, 39, 15)))
db.session.add(
    Post(uid=122, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=226, c2_number=238, league="Hardcore",
         name="Thrasher", time=datetime.datetime(2016, 3, 11, 10, 38, 12)))
db.session.add(
    Post(uid=123, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=105, c2_number=86, league="Hardcore",
         name="Dredd", time=datetime.datetime(2016, 4, 1, 11, 42, 30)))
db.session.add(
    Post(uid=124, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=204, c2_number=297, league="Hardcore",
         name="Mud Pie Man", time=datetime.datetime(2016, 7, 6, 1, 33, 46)))
db.session.add(
    Post(uid=125, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=71, c2_number=236, league="Hardcore",
         name="Toe", time=datetime.datetime(2016, 8, 22, 9, 1, 52)))
db.session.add(
    Post(uid=126, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=215, c2_number=231, league="Hardcore",
         name="Dropkick", time=datetime.datetime(2016, 11, 11, 4, 17, 52)))
db.session.add(
    Post(uid=127, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=35, c2_number=147, league="Hardcore",
         name="Mule Skinner", time=datetime.datetime(2016, 4, 10, 9, 41, 1)))
db.session.add(
    Post(uid=128, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=48, c2_number=235, league="Hardcore",
         name="Toolmaker", time=datetime.datetime(2016, 4, 20, 1, 9, 31)))
db.session.add(
    Post(uid=129, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=175, c2_number=215, league="Hardcore",
         name="Drop Stone", time=datetime.datetime(2016, 7, 25, 3, 44, 13)))
db.session.add(
    Post(uid=130, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=198, c2_number=168, league="Hardcore",
         name="Murmur", time=datetime.datetime(2016, 1, 14, 18, 24, 57)))
db.session.add(
    Post(uid=131, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=69, c2_number=229, league="Hardcore",
         name="Tough Nut", time=datetime.datetime(2016, 7, 21, 18, 41, 10)))
db.session.add(
    Post(uid=132, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=34, c2_number=193, league="Hardcore",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 10, 22, 0, 56, 6)))
db.session.add(
    Post(uid=133, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=253, c2_number=205, league="Hardcore",
         name="Nacho", time=datetime.datetime(2016, 8, 7, 17, 40, 8)))
db.session.add(
    Post(uid=134, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=23, c2_number=175, league="Hardcore",
         name="Trip", time=datetime.datetime(2016, 2, 9, 21, 37, 19)))
db.session.add(
    Post(uid=135, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=203, c2_number=244, league="Hardcore",
         name="Easy Sweep", time=datetime.datetime(2016, 12, 27, 6, 54, 4)))
db.session.add(
    Post(uid=136, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=165, c2_number=289, league="Hardcore",
         name="Natural Mess", time=datetime.datetime(2016, 11, 24, 11, 1, 8)))
db.session.add(
    Post(uid=137, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=150, c2_number=30, league="Hardcore",
         name="Troubadour", time=datetime.datetime(2016, 11, 24, 7, 54, 33)))
db.session.add(
    Post(uid=138, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=27, c2_number=262, league="Hardcore",
         name="Electric Player", time=datetime.datetime(2016, 5, 21, 0, 48, 56)))
db.session.add(Post(uid=139, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=306, c2_number=100,
                    league="Hardcore", name="Necromancer", time=datetime.datetime(2016, 2, 11, 18, 52, 37)))
db.session.add(
    Post(uid=140, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=314, c2_number=315, league="Hardcore",
         name="Turnip King", time=datetime.datetime(2016, 1, 3, 3, 22, 43)))
db.session.add(
    Post(uid=141, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=61, c2_number=267, league="Hardcore",
         name="Esquire", time=datetime.datetime(2016, 4, 22, 1, 3, 53)))
db.session.add(
    Post(uid=142, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=158, c2_number=68, league="Hardcore",
         name="Neophyte Believer", time=datetime.datetime(2016, 3, 18, 2, 54, 28)))
db.session.add(
    Post(uid=143, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=146, c2_number=237, league="Hardcore",
         name="Twitch", time=datetime.datetime(2016, 10, 7, 12, 11, 45)))
db.session.add(Post(uid=144, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=175, c2_number=39,
                    league="Hardcore", name="Fast Draw", time=datetime.datetime(2016, 11, 4, 14, 47, 48)))
db.session.add(
    Post(uid=145, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=48, c2_number=101, league="Hardcore",
         name="Nessie", time=datetime.datetime(2016, 8, 10, 20, 44, 0)))
db.session.add(
    Post(uid=146, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=315, c2_number=196, league="Hardcore",
         name="Vagabond Warrior", time=datetime.datetime(2016, 9, 15, 16, 52, 26)))
db.session.add(Post(uid=147, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=276, c2_number=229,
                    league="Hardcore", name="Flakes", time=datetime.datetime(2016, 8, 2, 7, 56, 13)))
db.session.add(
    Post(uid=148, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=316, c2_number=222, league="Hardcore",
         name="New Cycle", time=datetime.datetime(2016, 5, 15, 4, 27, 16)))
db.session.add(
    Post(uid=149, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=161, c2_number=101, league="Hardcore",
         name="Voluntary", time=datetime.datetime(2016, 12, 3, 17, 42, 4)))
db.session.add(
    Post(uid=150, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=95, c2_number=287, league="Hardcore",
         name="Flint", time=datetime.datetime(2016, 10, 11, 11, 35, 33)))
db.session.add(
    Post(uid=151, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=100, c2_number=20, league="Hardcore",
         name="Nickname Master", time=datetime.datetime(2016, 11, 4, 4, 41, 19)))
db.session.add(
    Post(uid=152, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=46, c2_number=199, league="Hardcore",
         name="Vortex", time=datetime.datetime(2016, 1, 18, 3, 36, 24)))
db.session.add(
    Post(uid=153, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=214, c2_number=108, league="Hardcore",
         name="Freak", time=datetime.datetime(2016, 1, 18, 21, 50, 42)))
db.session.add(
    Post(uid=154, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=182, c2_number=273, league="Hardcore",
         name="Nightmare King", time=datetime.datetime(2016, 9, 2, 22, 48, 10)))
db.session.add(
    Post(uid=155, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=140, c2_number=170, league="Hardcore",
         name="Washer", time=datetime.datetime(2016, 7, 23, 16, 29, 28)))
db.session.add(
    Post(uid=156, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=300, c2_number=291, league="Hardcore",
         name="Gas Man", time=datetime.datetime(2016, 7, 1, 18, 22, 24)))
db.session.add(
    Post(uid=157, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=225, c2_number=74, league="Hardcore",
         name="Night Train", time=datetime.datetime(2016, 11, 23, 21, 54, 50)))
db.session.add(Post(uid=158, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=185, c2_number=150, league="Hardcore",
                    name="Waylay Dave", time=datetime.datetime(2016, 10, 28, 12, 38, 2)))
db.session.add(
    Post(uid=159, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=60, c2_number=241, league="Hardcore",
         name="Glyph", time=datetime.datetime(2016, 10, 26, 19, 21, 11)))
db.session.add(Post(uid=160, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=278, c2_number=220, league="Hardcore",
                    name="Old Man Winter", time=datetime.datetime(2016, 5, 8, 19, 19, 8)))
db.session.add(
    Post(uid=161, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=100, c2_number=277, league="Hardcore",
         name="Wheels", time=datetime.datetime(2016, 4, 13, 16, 30, 10)))
db.session.add(
    Post(uid=162, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=27, c2_number=69, league="Hardcore",
         name="Grave Digger", time=datetime.datetime(2016, 3, 18, 3, 57, 17)))
db.session.add(
    Post(uid=163, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=125, c2_number=191, league="Hardcore",
         name="Old Orange Eyes", time=datetime.datetime(2016, 6, 14, 12, 34, 38)))
db.session.add(
    Post(uid=164, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=21, c2_number=47, league="Hardcore",
         name="Wooden Man", time=datetime.datetime(2016, 4, 2, 15, 45, 24)))
db.session.add(
    Post(uid=165, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=272, c2_number=161, league="Hardcore",
         name="Guillotine", time=datetime.datetime(2016, 1, 16, 2, 8, 45)))
db.session.add(
    Post(uid=166, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=181, c2_number=129, league="Hardcore",
         name="Old Regret", time=datetime.datetime(2016, 8, 12, 18, 53, 36)))
db.session.add(
    Post(uid=167, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=71, c2_number=259, league="Hardcore",
         name="Woo Woo", time=datetime.datetime(2016, 6, 17, 5, 27, 35)))
db.session.add(
    Post(uid=168, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=205, c2_number=264, league="Hardcore",
         name="Gunhawk", time=datetime.datetime(2016, 7, 9, 18, 25, 31)))
db.session.add(
    Post(uid=169, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=158, c2_number=239, league="Hardcore",
         name="Onion King", time=datetime.datetime(2016, 3, 22, 17, 43, 13)))
db.session.add(Post(uid=170, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=77, c2_number=292, league="Hardcore",
                    name="Yellow Menace", time=datetime.datetime(2016, 6, 8, 15, 31, 0)))
db.session.add(Post(uid=171, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=49, c2_number=42, league="Hardcore",
                    name="High Kingdom Warrior", time=datetime.datetime(2016, 6, 6, 7, 58, 52)))
db.session.add(
    Post(uid=172, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=276, c2_number=115, league="Hardcore",
         name="Osprey", time=datetime.datetime(2016, 4, 5, 18, 52, 58)))
db.session.add(Post(uid=173, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=115, c2_number=55, league="Hardcore",
                    name="Zero Charisma", time=datetime.datetime(2016, 7, 12, 14, 53, 53)))
db.session.add(Post(uid=174, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=36, c2_number=202, league="Hardcore",
                    name="Highlander Monk", time=datetime.datetime(2016, 7, 27, 22, 43, 45)))
db.session.add(
    Post(uid=175, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=315, c2_number=253, league="Hardcore",
         name="Overrun", time=datetime.datetime(2016, 9, 20, 1, 33, 20)))
db.session.add(Post(uid=176, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=153, c2_number=76, league="Hardcore",
                    name="Zesty Dragon", time=datetime.datetime(2016, 8, 10, 1, 10, 18)))
db.session.add(
    Post(uid=177, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=202, c2_number=143, league="Hardcore",
         name="Zod", time=datetime.datetime(2016, 3, 22, 14, 49, 19)))
db.session.add(
    Post(uid=0, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=51, c2_number=312, league="Hardcore", name="101",
         time=datetime.datetime(2016, 12, 13, 16, 28, 57)))
db.session.add(Post(uid=1, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=90, c2_number=98, league="Hardcore",
                    name="Houston", time=datetime.datetime(2016, 8, 13, 9, 51, 16)))
db.session.add(
    Post(uid=2, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=282, c2_number=77, league="Hardcore",
         name="Pinball Wizard", time=datetime.datetime(2016, 4, 12, 1, 26, 13)))
db.session.add(Post(uid=3, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=255, c2_number=73, league="Hardcore",
                    name="Accidental Genius", time=datetime.datetime(2016, 4, 3, 5, 14, 10)))
db.session.add(
    Post(uid=4, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=262, c2_number=290, league="Hardcore",
         name="Hyper", time=datetime.datetime(2016, 8, 21, 5, 54, 54)))
db.session.add(
    Post(uid=5, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=300, c2_number=192, league="Hardcore",
         name="Pluto", time=datetime.datetime(2016, 8, 15, 1, 13, 16)))
db.session.add(Post(uid=6, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=290, c2_number=290, league="Hardcore",
                    name="Alpha", time=datetime.datetime(2016, 1, 16, 15, 35, 34)))
db.session.add(Post(uid=7, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=307, c2_number=86, league="Hardcore",
                    name="Jester", time=datetime.datetime(2016, 1, 1, 17, 41, 7)))
db.session.add(Post(uid=8, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=21, c2_number=22, league="Hardcore",
                    name="Pogue", time=datetime.datetime(2016, 5, 27, 13, 35, 57)))
db.session.add(Post(uid=9, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=45, c2_number=51, league="Hardcore",
                    name="Airport Hobo", time=datetime.datetime(2016, 8, 28, 15, 29, 23)))
db.session.add(Post(uid=10, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=260, c2_number=204, league="Hardcore",
                    name="Jigsaw", time=datetime.datetime(2016, 6, 6, 13, 22, 40)))
db.session.add(Post(uid=11, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=127, c2_number=167, league="Hardcore",
                    name="Prometheus", time=datetime.datetime(2016, 1, 4, 12, 58, 6)))
db.session.add(
    Post(uid=12, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=159, c2_number=130, league="Hardcore",
         name="Bearded Angler", time=datetime.datetime(2016, 3, 21, 2, 36, 0)))
db.session.add(Post(uid=13, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=130, c2_number=201, league="Hardcore",
                    name="Joker's Grin", time=datetime.datetime(2016, 12, 12, 15, 42, 10)))
db.session.add(
    Post(uid=14, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=147, c2_number=77, league="Hardcore",
         name="Psycho Thinker", time=datetime.datetime(2016, 8, 9, 5, 49, 50)))
db.session.add(Post(uid=15, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=204, c2_number=286,
                    league="Hardcore", name="Beetle King", time=datetime.datetime(2016, 8, 15, 13, 10, 22)))
db.session.add(
    Post(uid=16, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=167, c2_number=139, league="Hardcore",
         name="Judge", time=datetime.datetime(2016, 12, 2, 16, 42, 34)))
db.session.add(
    Post(uid=17, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=76, c2_number=286, league="Hardcore",
         name="Pusher", time=datetime.datetime(2016, 11, 26, 2, 2, 17)))
db.session.add(
    Post(uid=18, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=51, c2_number=104, league="Hardcore",
         name="Bitmap", time=datetime.datetime(2016, 7, 26, 3, 22, 45)))
db.session.add(
    Post(uid=19, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=194, c2_number=83, league="Hardcore",
         name="Junkyard Dog", time=datetime.datetime(2016, 4, 18, 4, 39, 19)))
db.session.add(
    Post(uid=20, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=52, c2_number=183, league="Hardcore",
         name="Riff Raff", time=datetime.datetime(2016, 11, 20, 16, 42, 10)))
db.session.add(
    Post(uid=21, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=319, c2_number=291, league="Hardcore",
         name="Blister", time=datetime.datetime(2016, 4, 24, 17, 37, 2)))
db.session.add(
    Post(uid=22, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=208, c2_number=99, league="Hardcore",
         name="K-9", time=datetime.datetime(2016, 11, 22, 12, 25, 9)))
db.session.add(
    Post(uid=23, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=84, c2_number=297, league="Hardcore",
         name="Roadblock", time=datetime.datetime(2016, 3, 17, 16, 25, 9)))
db.session.add(
    Post(uid=24, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=235, c2_number=174, league="Hardcore",
         name="Bowie", time=datetime.datetime(2016, 9, 3, 2, 35, 42)))
db.session.add(
    Post(uid=25, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=67, c2_number=79, league="Hardcore",
         name="Keystone", time=datetime.datetime(2016, 8, 11, 9, 54, 55)))
db.session.add(
    Post(uid=26, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=284, c2_number=310, league="Hardcore",
         name="Rooster", time=datetime.datetime(2016, 11, 3, 11, 53, 6)))
db.session.add(
    Post(uid=27, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=34, c2_number=227, league="Hardcore",
         name="Bowler", time=datetime.datetime(2016, 5, 11, 4, 30, 26)))
db.session.add(
    Post(uid=28, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=282, c2_number=169, league="Hardcore",
         name="Kickstart", time=datetime.datetime(2016, 5, 18, 7, 10, 49)))
db.session.add(
    Post(uid=29, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=263, c2_number=209, league="Hardcore",
         name="Sandbox", time=datetime.datetime(2016, 4, 5, 13, 55, 7)))
db.session.add(
    Post(uid=30, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=111, c2_number=47, league="Hardcore",
         name="Breadmaker", time=datetime.datetime(2016, 5, 17, 2, 57, 54)))
db.session.add(
    Post(uid=31, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=112, c2_number=144, league="Hardcore",
         name="Kill Switch", time=datetime.datetime(2016, 3, 5, 13, 1, 49)))
db.session.add(
    Post(uid=32, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=158, c2_number=297, league="Hardcore",
         name="Scrapper", time=datetime.datetime(2016, 4, 17, 6, 3, 22)))
db.session.add(Post(uid=33, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=124, c2_number=289,
                    league="Hardcore", name="Broomspun", time=datetime.datetime(2016, 12, 19, 2, 56, 36)))
db.session.add(Post(uid=34, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=93, c2_number=289, league="Hardcore",
                    name="Kingfisher", time=datetime.datetime(2016, 11, 7, 10, 7, 30)))
db.session.add(
    Post(uid=35, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=283, c2_number=130, league="Hardcore",
         name="Screwtape", time=datetime.datetime(2016, 5, 7, 21, 11, 25)))
db.session.add(
    Post(uid=36, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=254, c2_number=291, league="Hardcore",
         name="Buckshot", time=datetime.datetime(2016, 4, 15, 15, 51, 12)))
db.session.add(
    Post(uid=37, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=97, c2_number=251, league="Hardcore",
         name="Kitchen", time=datetime.datetime(2016, 5, 10, 6, 57, 3)))
db.session.add(
    Post(uid=38, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=85, c2_number=173, league="Hardcore",
         name="Sexual Chocolate", time=datetime.datetime(2016, 4, 5, 6, 9, 31)))
db.session.add(
    Post(uid=39, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=232, c2_number=28, league="Hardcore",
         name="Bugger", time=datetime.datetime(2016, 6, 6, 12, 7, 0)))
db.session.add(
    Post(uid=40, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=98, c2_number=200, league="Hardcore",
         name="Knuckles", time=datetime.datetime(2016, 1, 21, 21, 5, 2)))
db.session.add(
    Post(uid=41, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=94, c2_number=39, league="Hardcore",
         name="Shadow Chaser", time=datetime.datetime(2016, 6, 13, 15, 12, 46)))
db.session.add(
    Post(uid=42, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=134, c2_number=255, league="Hardcore",
         name="Cabbie", time=datetime.datetime(2016, 10, 7, 12, 0, 50)))
db.session.add(
    Post(uid=43, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=109, c2_number=230, league="Hardcore",
         name="Lady Killer", time=datetime.datetime(2016, 7, 28, 13, 58, 34)))
db.session.add(
    Post(uid=44, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=319, c2_number=84, league="Hardcore",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 12, 10, 1, 9, 8)))
db.session.add(
    Post(uid=45, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=192, c2_number=47, league="Hardcore",
         name="Candy Butcher", time=datetime.datetime(2016, 11, 27, 4, 30, 54)))
db.session.add(Post(uid=46, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=37, c2_number=134, league="Hardcore",
                    name="Liquid Science", time=datetime.datetime(2016, 1, 7, 6, 51, 42)))
db.session.add(Post(uid=47, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=104, c2_number=136, league="Hardcore",
                    name="Shooter", time=datetime.datetime(2016, 1, 15, 18, 17, 47)))
db.session.add(
    Post(uid=48, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=21, c2_number=137, league="Hardcore",
         name="Capital F", time=datetime.datetime(2016, 8, 5, 12, 26, 20)))
db.session.add(
    Post(uid=49, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=195, c2_number=20, league="Hardcore",
         name="Little Cobra", time=datetime.datetime(2016, 10, 27, 17, 43, 23)))
db.session.add(Post(uid=50, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=247, c2_number=110, league="Legacy",
                    name="Sidewalk Enforcer", time=datetime.datetime(2016, 12, 16, 10, 23, 35)))
db.session.add(
    Post(uid=51, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=42, c2_number=106, league="Legacy",
         name="Captain Peroxide", time=datetime.datetime(2016, 10, 5, 12, 31, 20)))
db.session.add(Post(uid=52, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=63, c2_number=94, league="Legacy",
                    name="Little General", time=datetime.datetime(2016, 7, 23, 8, 13, 0)))
db.session.add(
    Post(uid=53, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=172, c2_number=180, league="Legacy",
         name="Skull Crusher", time=datetime.datetime(2016, 1, 11, 16, 46, 13)))
db.session.add(Post(uid=54, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=50, c2_number=219, league="Legacy",
                    name="Celtic Charger", time=datetime.datetime(2016, 2, 2, 22, 7, 4)))
db.session.add(Post(uid=55, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=299, c2_number=48, league="Legacy",
                    name="Lord Nikon", time=datetime.datetime(2016, 5, 2, 14, 16, 50)))
db.session.add(
    Post(uid=56, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=198, c2_number=69, league="Legacy",
         name="Sky Bully", time=datetime.datetime(2016, 12, 18, 12, 27, 6)))
db.session.add(
    Post(uid=57, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=166, c2_number=233, league="Legacy",
         name="Cereal Killer", time=datetime.datetime(2016, 5, 8, 17, 12, 33)))
db.session.add(
    Post(uid=58, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=85, c2_number=51, league="Legacy",
         name="Lord Pistachio", time=datetime.datetime(2016, 8, 16, 2, 47, 13)))
db.session.add(
    Post(uid=59, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=188, c2_number=226, league="Legacy",
         name="Slow Trot", time=datetime.datetime(2016, 10, 23, 17, 35, 5)))
db.session.add(
    Post(uid=60, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=126, c2_number=289, league="Legacy",
         name="Chicago Blackout", time=datetime.datetime(2016, 1, 12, 0, 56, 34)))
db.session.add(
    Post(uid=61, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=263, c2_number=232, league="Legacy",
         name="Mad Irishman", time=datetime.datetime(2016, 3, 4, 20, 12, 4)))
db.session.add(
    Post(uid=62, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=154, c2_number=225, league="Legacy",
         name="Snake Eyes", time=datetime.datetime(2016, 1, 5, 9, 56, 37)))
db.session.add(
    Post(uid=63, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=256, c2_number=319, league="Legacy",
         name="Chocolate Thunder", time=datetime.datetime(2016, 5, 2, 4, 20, 4)))
db.session.add(Post(uid=64, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=217, c2_number=167, league="Legacy",
                    name="Mad Jack", time=datetime.datetime(2016, 1, 13, 17, 24, 47)))
db.session.add(Post(uid=65, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=93, c2_number=175, league="Legacy",
                    name="Snow Hound", time=datetime.datetime(2016, 3, 2, 2, 1, 14)))
db.session.add(
    Post(uid=66, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=286, c2_number=217, league="Legacy",
         name="Chuckles", time=datetime.datetime(2016, 11, 13, 0, 24, 40)))
db.session.add(Post(uid=67, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=188, c2_number=210, league="Legacy",
                    name="Mad Rascal", time=datetime.datetime(2016, 7, 20, 0, 19, 13)))
db.session.add(
    Post(uid=68, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=57, c2_number=240, league="Legacy",
         name="Sofa King", time=datetime.datetime(2016, 4, 7, 18, 44, 31)))
db.session.add(
    Post(uid=69, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=83, c2_number=57,
         league="Legacy", name="Commando", time=datetime.datetime(2016, 6, 5, 2, 56, 52)))
db.session.add(
    Post(uid=70, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=297, c2_number=299, league="Legacy",
         name="Manimal", time=datetime.datetime(2016, 1, 13, 12, 25, 2)))
db.session.add(Post(uid=71, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=260, c2_number=202,
                    league="Legacy", name="Speedwell", time=datetime.datetime(2016, 9, 5, 8, 39, 56)))
db.session.add(
    Post(uid=72, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=133, c2_number=248, league="Legacy",
         name="Cool Whip", time=datetime.datetime(2016, 6, 9, 4, 47, 5)))
db.session.add(
    Post(uid=73, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=164, c2_number=242, league="Legacy",
         name="Marbles", time=datetime.datetime(2016, 6, 27, 11, 57, 22)))
db.session.add(Post(uid=74, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=63, c2_number=154,
                    league="Legacy", name="Spider Fuji", time=datetime.datetime(2016, 4, 8, 21, 25, 17)))
db.session.add(Post(uid=75, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=119, c2_number=206,
                    league="Legacy", name="Cosmo", time=datetime.datetime(2016, 12, 22, 3, 51, 23)))
db.session.add(Post(uid=76, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=94, c2_number=233,
                    league="Legacy", name="Married Man", time=datetime.datetime(2016, 7, 4, 1, 33, 54)))
db.session.add(Post(uid=77, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=263, c2_number=111,
                    league="Legacy", name="Springheel Jack", time=datetime.datetime(2016, 7, 13, 0, 55, 39)))
db.session.add(
    Post(uid=78, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=313, c2_number=60, league="Legacy",
         name="Crash Override", time=datetime.datetime(2016, 4, 11, 9, 35, 49)))
db.session.add(Post(uid=79, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=116, c2_number=214,
                    league="Legacy", name="Marshmallow", time=datetime.datetime(2016, 11, 11, 19, 53, 1)))
db.session.add(
    Post(uid=80, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=294, c2_number=27, league="Legacy",
         name="Squatch", time=datetime.datetime(2016, 9, 24, 6, 47, 2)))
db.session.add(Post(uid=81, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=264, c2_number=176,
                    league="Legacy", name="Crash Test", time=datetime.datetime(2016, 10, 9, 2, 58, 21)))
db.session.add(
    Post(uid=82, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=49, c2_number=141, league="Legacy",
         name="Mental", time=datetime.datetime(2016, 12, 8, 12, 35, 13)))
db.session.add(
    Post(uid=83, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=126, c2_number=35, league="Legacy",
         name="Stacker of Wheat", time=datetime.datetime(2016, 12, 21, 22, 22, 41)))
db.session.add(Post(uid=84, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=129, c2_number=103,
                    league="Legacy", name="Crazy Eights", time=datetime.datetime(2016, 9, 28, 8, 17, 32)))
db.session.add(
    Post(uid=85, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=40, c2_number=312, league="Legacy",
         name="Mercury Reborn", time=datetime.datetime(2016, 3, 12, 5, 36, 30)))
db.session.add(Post(uid=86, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=65, c2_number=182, league="Legacy",
                    name="Sugar Man", time=datetime.datetime(2016, 10, 7, 2, 51, 46)))
db.session.add(
    Post(uid=87, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=108, c2_number=74, league="Legacy",
         name="Criss Cross", time=datetime.datetime(2016, 12, 4, 1, 10, 42)))
db.session.add(
    Post(uid=88, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=23, c2_number=37, league="Legacy", name="Midas",
         time=datetime.datetime(2016, 3, 10, 11, 27, 55)))
db.session.add(Post(uid=89, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=98, c2_number=102, league="Legacy",
                    name="Suicide Jockey", time=datetime.datetime(2016, 8, 9, 16, 39, 2)))
db.session.add(Post(uid=90, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=101, c2_number=192, league="Legacy",
                    name="Cross Thread", time=datetime.datetime(2016, 4, 8, 4, 50, 4)))
db.session.add(Post(uid=91, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=253, c2_number=152, league="Legacy",
                    name="Midnight Rambler", time=datetime.datetime(2016, 3, 6, 3, 57, 2)))
db.session.add(
    Post(uid=92, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=285, c2_number=193, league="Legacy",
         name="Swampmasher", time=datetime.datetime(2016, 3, 10, 12, 54, 22)))
db.session.add(
    Post(uid=93, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=258, c2_number=292, league="Legacy",
         name="Cujo", time=datetime.datetime(2016, 4, 8, 4, 48, 54)))
db.session.add(Post(uid=94, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=22, c2_number=186, league="Legacy",
                    name="Midnight Rider", time=datetime.datetime(2016, 9, 14, 19, 4, 36)))
db.session.add(
    Post(uid=95, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=79, c2_number=263, league="Legacy",
         name="Swerve", time=datetime.datetime(2016, 6, 25, 2, 39, 40)))
db.session.add(Post(uid=96, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=242, c2_number=136, league="Legacy",
                    name="Dancing Madman", time=datetime.datetime(2016, 6, 7, 13, 53, 1)))
db.session.add(Post(uid=97, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=28, c2_number=128, league="Legacy",
                    name="Mindless Bobcat", time=datetime.datetime(2016, 1, 27, 2, 55, 32)))
db.session.add(Post(uid=98, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=178, c2_number=119, league="Legacy",
                    name="Tacklebox", time=datetime.datetime(2016, 2, 1, 2, 6, 21)))
db.session.add(
    Post(uid=99, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=199, c2_number=135, league="Legacy",
         name="Dangle", time=datetime.datetime(2016, 1, 17, 1, 54, 9)))
db.session.add(Post(uid=100, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=115, c2_number=183, league="Legacy",
                    name="Mr. 44", time=datetime.datetime(2016, 1, 10, 13, 27, 11)))
db.session.add(Post(uid=101, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=292, c2_number=70, league="Legacy",
                    name="Take Away", time=datetime.datetime(2016, 12, 21, 16, 24, 1)))
db.session.add(Post(uid=102, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=189, c2_number=72, league="Legacy",
                    name="Dark Horse", time=datetime.datetime(2016, 5, 18, 2, 32, 12)))
db.session.add(Post(uid=103, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=274, c2_number=289, league="Legacy",
                    name="Mr. Fabulous", time=datetime.datetime(2016, 7, 9, 8, 56, 31)))
db.session.add(
    Post(uid=104, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=169, c2_number=100, league="Legacy",
         name="Tan Stallion", time=datetime.datetime(2016, 10, 9, 0, 43, 35)))
db.session.add(Post(uid=105, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=145, c2_number=298,
                    league="Legacy", name="Day Hawk", time=datetime.datetime(2016, 12, 25, 18, 35, 36)))
db.session.add(
    Post(uid=106, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=122, c2_number=239, league="Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 4, 20, 15, 56, 1)))
db.session.add(
    Post(uid=107, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=21, c2_number=90, league="Legacy",
         name="The China Wall", time=datetime.datetime(2016, 11, 24, 11, 10, 49)))
db.session.add(
    Post(uid=108, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=108, c2_number=39, league="Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 4, 20, 3, 15, 14)))
db.session.add(
    Post(uid=109, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=252, c2_number=264, league="Legacy",
         name="Mr. Lucky", time=datetime.datetime(2016, 1, 1, 3, 28, 55)))
db.session.add(
    Post(uid=110, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=189, c2_number=309, league="Legacy",
         name="The Dude", time=datetime.datetime(2016, 2, 9, 19, 40, 11)))
db.session.add(
    Post(uid=111, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=216, c2_number=249, league="Legacy",
         name="Digger", time=datetime.datetime(2016, 9, 24, 13, 44, 19)))
db.session.add(
    Post(uid=112, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=223, c2_number=276, league="Legacy",
         name="Mr. Peppermint", time=datetime.datetime(2016, 2, 4, 6, 34, 7)))
db.session.add(
    Post(uid=113, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=302, c2_number=25, league="Legacy",
         name="The Flying Mouse", time=datetime.datetime(2016, 1, 13, 12, 53, 12)))
db.session.add(
    Post(uid=114, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=316, c2_number=262, league="Legacy",
         name="Disco Thunder", time=datetime.datetime(2016, 4, 17, 10, 32, 57)))
db.session.add(
    Post(uid=115, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=158, c2_number=238, league="Legacy",
         name="Mr. Spy", time=datetime.datetime(2016, 5, 18, 22, 6, 32)))
db.session.add(
    Post(uid=116, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=260, c2_number=187, league="Legacy",
         name="The Happy Jock", time=datetime.datetime(2016, 11, 25, 12, 20, 38)))
db.session.add(
    Post(uid=117, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=147, c2_number=110, league="Legacy",
         name="Disco Potato", time=datetime.datetime(2016, 6, 12, 2, 34, 52)))
db.session.add(Post(uid=118, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=86, c2_number=143, league="Legacy",
                    name="Mr. Thanksgiving", time=datetime.datetime(2016, 12, 28, 11, 44, 37)))
db.session.add(Post(uid=119, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=26, c2_number=122, league="Legacy",
                    name="The Howling Swede", time=datetime.datetime(2016, 6, 25, 15, 16, 15)))
db.session.add(
    Post(uid=120, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=221, c2_number=49, league="Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 7, 12, 8, 9, 20)))
db.session.add(
    Post(uid=121, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=308, c2_number=143, league="Legacy",
         name="Mr. Wholesome", time=datetime.datetime(2016, 12, 15, 10, 13, 43)))
db.session.add(Post(uid=122, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=111, c2_number=261, league="Legacy",
                    name="Thrasher", time=datetime.datetime(2016, 4, 19, 8, 53, 37)))
db.session.add(
    Post(uid=123, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=152, c2_number=317, league="Legacy",
         name="Dredd", time=datetime.datetime(2016, 2, 15, 13, 1, 13)))
db.session.add(Post(uid=124, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=143, c2_number=200, league="Legacy",
                    name="Mud Pie Man", time=datetime.datetime(2016, 8, 22, 22, 58, 32)))
db.session.add(
    Post(uid=125, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=319, c2_number=61, league="Legacy",
         name="Toe", time=datetime.datetime(2016, 2, 27, 2, 50, 20)))
db.session.add(Post(uid=126, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=95, c2_number=292, league="Legacy",
                    name="Dropkick", time=datetime.datetime(2016, 2, 13, 21, 8, 12)))
db.session.add(Post(uid=127, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=297, c2_number=246, league="Legacy",
                    name="Mule Skinner", time=datetime.datetime(2016, 7, 12, 6, 53, 33)))
db.session.add(
    Post(uid=128, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=41, c2_number=39, league="Legacy",
         name="Toolmaker", time=datetime.datetime(2016, 3, 20, 5, 36, 44)))
db.session.add(
    Post(uid=129, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=139, c2_number=262, league="Legacy",
         name="Drop Stone", time=datetime.datetime(2016, 9, 21, 5, 40, 57)))
db.session.add(
    Post(uid=130, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=316, c2_number=248, league="Legacy",
         name="Murmur", time=datetime.datetime(2016, 9, 18, 0, 40, 36)))
db.session.add(
    Post(uid=131, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=287, c2_number=233, league="Legacy",
         name="Tough Nut", time=datetime.datetime(2016, 8, 19, 13, 46, 15)))
db.session.add(
    Post(uid=132, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=178, c2_number=157, league="Legacy",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 6, 2, 7, 25, 34)))
db.session.add(
    Post(uid=133, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=70, c2_number=192, league="Legacy",
         name="Nacho", time=datetime.datetime(2016, 4, 23, 12, 25, 0)))
db.session.add(
    Post(uid=134, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=98, c2_number=257, league="Legacy",
         name="Trip", time=datetime.datetime(2016, 9, 28, 6, 20, 58)))
db.session.add(
    Post(uid=135, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=286, c2_number=249, league="Legacy",
         name="Easy Sweep", time=datetime.datetime(2016, 8, 15, 15, 39, 28)))
db.session.add(Post(uid=136, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=102, c2_number=231, league="Legacy",
                    name="Natural Mess", time=datetime.datetime(2016, 3, 5, 5, 51, 34)))
db.session.add(Post(uid=137, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=117, c2_number=92, league="Legacy",
                    name="Troubadour", time=datetime.datetime(2016, 9, 26, 6, 8, 30)))
db.session.add(
    Post(uid=138, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=227, c2_number=294, league="Legacy",
         name="Electric Player", time=datetime.datetime(2016, 8, 9, 21, 53, 25)))
db.session.add(Post(uid=139, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=274, c2_number=121, league="Legacy",
                    name="Necromancer", time=datetime.datetime(2016, 9, 1, 6, 36, 33)))
db.session.add(
    Post(uid=140, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=296, c2_number=210, league="Legacy",
         name="Turnip King", time=datetime.datetime(2016, 4, 23, 0, 36, 1)))
db.session.add(
    Post(uid=141, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=147, c2_number=116, league="Legacy",
         name="Esquire", time=datetime.datetime(2016, 9, 10, 6, 6, 57)))
db.session.add(Post(uid=142, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=282, c2_number=44, league="Legacy",
                    name="Neophyte Believer", time=datetime.datetime(2016, 2, 10, 20, 4, 43)))
db.session.add(
    Post(uid=143, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=275, c2_number=42, league="Legacy",
         name="Twitch", time=datetime.datetime(2016, 7, 4, 4, 33, 47)))
db.session.add(Post(uid=144, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=277, c2_number=113, league="Legacy",
                    name="Fast Draw", time=datetime.datetime(2016, 8, 4, 4, 5, 20)))
db.session.add(
    Post(uid=145, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=168, c2_number=303, league="Legacy",
         name="Nessie", time=datetime.datetime(2016, 3, 23, 13, 49, 32)))
db.session.add(
    Post(uid=146, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=112, c2_number=257, league="Legacy",
         name="Vagabond Warrior", time=datetime.datetime(2016, 12, 1, 14, 18, 30)))
db.session.add(
    Post(uid=147, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=249, c2_number=205, league="Legacy",
         name="Flakes", time=datetime.datetime(2016, 3, 13, 6, 5, 35)))
db.session.add(
    Post(uid=148, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=51, c2_number=281, league="Legacy",
         name="New Cycle", time=datetime.datetime(2016, 2, 10, 21, 18, 35)))
db.session.add(
    Post(uid=149, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=147, c2_number=202, league="Legacy",
         name="Voluntary", time=datetime.datetime(2016, 6, 6, 2, 34, 21)))
db.session.add(
    Post(uid=150, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=68, c2_number=294, league="Legacy",
         name="Flint", time=datetime.datetime(2016, 2, 7, 9, 32, 22)))
db.session.add(
    Post(uid=151, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=233, c2_number=298, league="Legacy",
         name="Nickname Master", time=datetime.datetime(2016, 11, 21, 2, 57, 18)))
db.session.add(
    Post(uid=152, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=129, c2_number=66, league="Legacy",
         name="Vortex", time=datetime.datetime(2016, 12, 20, 18, 46, 42)))
db.session.add(
    Post(uid=153, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=53, c2_number=20, league="Legacy",
         name="Freak", time=datetime.datetime(2016, 3, 11, 14, 52, 5)))
db.session.add(Post(uid=154, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=94, c2_number=315, league="Legacy",
                    name="Nightmare King", time=datetime.datetime(2016, 4, 5, 8, 12, 0)))
db.session.add(Post(uid=155, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=164, c2_number=279, league="Legacy",
                    name="Washer", time=datetime.datetime(2016, 6, 15, 0, 31, 37)))
db.session.add(
    Post(uid=156, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=108, c2_number=54, league="Legacy",
         name="Gas Man", time=datetime.datetime(2016, 9, 7, 13, 3, 0)))
db.session.add(Post(uid=157, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=268, c2_number=54, league="Legacy",
                    name="Night Train", time=datetime.datetime(2016, 10, 20, 6, 14, 30)))
db.session.add(
    Post(uid=158, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=79, c2_number=257, league="Legacy",
         name="Waylay Dave", time=datetime.datetime(2016, 3, 3, 11, 45, 3)))
db.session.add(Post(uid=159, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=163, c2_number=177,
                    league="Legacy", name="Glyph", time=datetime.datetime(2016, 9, 12, 2, 33, 10)))
db.session.add(
    Post(uid=160, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=162, c2_number=36, league="Legacy",
         name="Old Man Winter", time=datetime.datetime(2016, 7, 12, 1, 0, 58)))
db.session.add(
    Post(uid=161, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=151, c2_number=153, league="Legacy",
         name="Wheels", time=datetime.datetime(2016, 9, 11, 11, 6, 3)))
db.session.add(
    Post(uid=162, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=196, c2_number=22, league="Legacy",
         name="Grave Digger", time=datetime.datetime(2016, 9, 19, 7, 7, 22)))
db.session.add(
    Post(uid=163, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=293, c2_number=241, league="Legacy",
         name="Old Orange Eyes", time=datetime.datetime(2016, 12, 11, 14, 37, 19)))
db.session.add(Post(uid=164, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=23, c2_number=147,
                    league="Legacy", name="Wooden Man", time=datetime.datetime(2016, 7, 16, 15, 36, 28)))
db.session.add(
    Post(uid=165, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=124, c2_number=164, league="Legacy",
         name="Guillotine", time=datetime.datetime(2016, 12, 11, 19, 41, 17)))
db.session.add(
    Post(uid=166, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=288, c2_number=56, league="Legacy",
         name="Old Regret", time=datetime.datetime(2016, 10, 10, 12, 17, 56)))
db.session.add(Post(uid=167, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=125, c2_number=52,
                    league="Legacy", name="Woo Woo", time=datetime.datetime(2016, 4, 9, 14, 30, 6)))
db.session.add(
    Post(uid=168, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=196, c2_number=282, league="Legacy",
         name="Gunhawk", time=datetime.datetime(2016, 3, 3, 5, 39, 34)))
db.session.add(
    Post(uid=169, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=315, c2_number=247, league="Legacy",
         name="Onion King", time=datetime.datetime(2016, 9, 28, 6, 1, 43)))
db.session.add(
    Post(uid=170, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=130, c2_number=232, league="Legacy",
         name="Yellow Menace", time=datetime.datetime(2016, 11, 15, 2, 31, 24)))
db.session.add(
    Post(uid=171, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=275, c2_number=151, league="Legacy",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 2, 28, 11, 57, 1)))
db.session.add(
    Post(uid=172, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=194, c2_number=283, league="Legacy",
         name="Osprey", time=datetime.datetime(2016, 10, 17, 5, 6, 52)))
db.session.add(
    Post(uid=173, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=285, c2_number=185, league="Legacy",
         name="Zero Charisma", time=datetime.datetime(2016, 1, 17, 10, 36, 15)))
db.session.add(
    Post(uid=174, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=130, c2_number=237, league="Legacy",
         name="Highlander Monk", time=datetime.datetime(2016, 3, 17, 17, 3, 42)))
db.session.add(
    Post(uid=175, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=67, c2_number=269, league="Legacy",
         name="Overrun", time=datetime.datetime(2016, 11, 16, 6, 48, 54)))
db.session.add(
    Post(uid=176, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=131, c2_number=76, league="Legacy",
         name="Zesty Dragon", time=datetime.datetime(2016, 12, 7, 13, 52, 24)))
db.session.add(Post(uid=177, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=135, c2_number=278,
                    league="Legacy", name="Zod", time=datetime.datetime(2016, 2, 16, 8, 58, 37)))
db.session.add(
    Post(uid=0, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=160, c2_number=39, league="Legacy", name="101",
         time=datetime.datetime(2016, 8, 20, 3, 37, 26)))
db.session.add(
    Post(uid=1, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=173, c2_number=187, league="Legacy",
         name="Houston", time=datetime.datetime(2016, 3, 8, 10, 29, 41)))
db.session.add(Post(uid=2, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=38, c2_number=281, league="Legacy",
                    name="Pinball Wizard", time=datetime.datetime(2016, 6, 26, 14, 45, 30)))
db.session.add(
    Post(uid=3, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=307, c2_number=165, league="Legacy",
         name="Accidental Genius", time=datetime.datetime(2016, 9, 12, 14, 55, 41)))
db.session.add(
    Post(uid=4, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=169, c2_number=87, league="Legacy",
         name="Hyper", time=datetime.datetime(2016, 11, 1, 21, 47, 8)))
db.session.add(
    Post(uid=5, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=301, c2_number=241, league="Legacy",
         name="Pluto", time=datetime.datetime(2016, 12, 18, 11, 9, 35)))
db.session.add(
    Post(uid=6, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=256, c2_number=205, league="Legacy",
         name="Alpha", time=datetime.datetime(2016, 5, 6, 15, 0, 51)))
db.session.add(
    Post(uid=7, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=101, c2_number=30, league="Legacy",
         name="Jester", time=datetime.datetime(2016, 8, 2, 17, 50, 44)))
db.session.add(
    Post(uid=8, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=261, c2_number=166, league="Legacy",
         name="Pogue", time=datetime.datetime(2016, 2, 15, 19, 37, 39)))
db.session.add(
    Post(uid=9, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=213, c2_number=45, league="Legacy",
         name="Airport Hobo", time=datetime.datetime(2016, 7, 13, 2, 32, 49)))
db.session.add(
    Post(uid=10, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=138, c2_number=145, league="Legacy",
         name="Jigsaw", time=datetime.datetime(2016, 7, 21, 3, 17, 12)))
db.session.add(
    Post(uid=11, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=290, c2_number=133, league="Legacy",
         name="Prometheus", time=datetime.datetime(2016, 11, 9, 2, 16, 42)))
db.session.add(
    Post(uid=12, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=167, c2_number=178, league="Legacy",
         name="Bearded Angler", time=datetime.datetime(2016, 4, 20, 8, 28, 35)))
db.session.add(Post(uid=13, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=216, c2_number=145, league="Legacy",
                    name="Joker's Grin", time=datetime.datetime(2016, 12, 18, 16, 32, 9)))
db.session.add(
    Post(uid=14, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=200, c2_number=192, league="Legacy",
         name="Psycho Thinker", time=datetime.datetime(2016, 4, 23, 3, 40, 47)))
db.session.add(
    Post(uid=15, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=223, c2_number=140, league="Legacy",
         name="Beetle King", time=datetime.datetime(2016, 9, 3, 10, 32, 36)))
db.session.add(
    Post(uid=16, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=251, c2_number=272, league="Legacy",
         name="Judge", time=datetime.datetime(2016, 11, 21, 11, 13, 9)))
db.session.add(Post(uid=17, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=136, c2_number=78,
                    league="Legacy", name="Pusher", time=datetime.datetime(2016, 10, 3, 17, 37, 38)))
db.session.add(
    Post(uid=18, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=258, c2_number=126, league="Legacy",
         name="Bitmap", time=datetime.datetime(2016, 8, 9, 18, 52, 30)))
db.session.add(
    Post(uid=19, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=147, c2_number=51, league="Legacy",
         name="Junkyard Dog", time=datetime.datetime(2016, 8, 8, 9, 42, 53)))
db.session.add(
    Post(uid=20, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=182, c2_number=265, league="Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 10, 6, 13, 49, 17)))
db.session.add(
    Post(uid=21, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=105, c2_number=90, league="Legacy",
         name="Blister", time=datetime.datetime(2016, 2, 6, 4, 37, 0)))
db.session.add(
    Post(uid=22, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=160, c2_number=150, league="Legacy",
         name="K-9", time=datetime.datetime(2016, 9, 18, 3, 57, 2)))
db.session.add(
    Post(uid=23, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=253, c2_number=288, league="Legacy",
         name="Roadblock", time=datetime.datetime(2016, 4, 13, 16, 25, 48)))
db.session.add(
    Post(uid=24, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=75, c2_number=261, league="Legacy",
         name="Bowie", time=datetime.datetime(2016, 5, 26, 22, 22, 36)))
db.session.add(
    Post(uid=25, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=90, c2_number=288, league="Legacy",
         name="Keystone", time=datetime.datetime(2016, 4, 1, 9, 10, 10)))
db.session.add(
    Post(uid=26, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=211, c2_number=176, league="Legacy",
         name="Rooster", time=datetime.datetime(2016, 7, 28, 5, 44, 22)))
db.session.add(
    Post(uid=27, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=190, c2_number=153, league="Legacy",
         name="Bowler", time=datetime.datetime(2016, 10, 10, 20, 13, 23)))
db.session.add(
    Post(uid=28, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=289, c2_number=238, league="Legacy",
         name="Kickstart", time=datetime.datetime(2016, 1, 21, 8, 33, 11)))
db.session.add(
    Post(uid=29, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=251, c2_number=62, league="Legacy",
         name="Sandbox", time=datetime.datetime(2016, 9, 22, 13, 33, 13)))
db.session.add(Post(uid=30, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=25, c2_number=120, league="Legacy",
                    name="Breadmaker", time=datetime.datetime(2016, 6, 20, 21, 38, 47)))
db.session.add(Post(uid=31, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=41, c2_number=276, league="Legacy",
                    name="Kill Switch", time=datetime.datetime(2016, 2, 7, 15, 23, 46)))
db.session.add(
    Post(uid=32, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=76, c2_number=132, league="Legacy",
         name="Scrapper", time=datetime.datetime(2016, 8, 23, 18, 13, 9)))
db.session.add(
    Post(uid=33, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=216, c2_number=211, league="Legacy",
         name="Broomspun", time=datetime.datetime(2016, 8, 1, 5, 8, 30)))
db.session.add(
    Post(uid=34, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=141, c2_number=115, league="Legacy",
         name="Kingfisher", time=datetime.datetime(2016, 5, 4, 4, 31, 58)))
db.session.add(Post(uid=35, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=71, c2_number=239,
                    league="Legacy", name="Screwtape", time=datetime.datetime(2016, 9, 24, 14, 32, 14)))
db.session.add(
    Post(uid=36, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=24, c2_number=218, league="Legacy",
         name="Buckshot", time=datetime.datetime(2016, 4, 19, 14, 10, 30)))
db.session.add(
    Post(uid=37, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=196, c2_number=166, league="Legacy",
         name="Kitchen", time=datetime.datetime(2016, 10, 22, 21, 36, 31)))
db.session.add(
    Post(uid=38, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=201, c2_number=64, league="Legacy",
         name="Sexual Chocolate", time=datetime.datetime(2016, 6, 10, 20, 55, 25)))
db.session.add(
    Post(uid=39, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=95, c2_number=209, league="Legacy",
         name="Bugger", time=datetime.datetime(2016, 11, 17, 11, 9, 5)))
db.session.add(Post(uid=40, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=254, c2_number=180,
                    league="Legacy", name="Knuckles", time=datetime.datetime(2016, 4, 18, 18, 57, 47)))
db.session.add(
    Post(uid=41, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=129, c2_number=156, league="Legacy",
         name="Shadow Chaser", time=datetime.datetime(2016, 12, 25, 9, 43, 55)))
db.session.add(
    Post(uid=42, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=152, c2_number=104, league="Legacy",
         name="Cabbie", time=datetime.datetime(2016, 11, 15, 19, 42, 16)))
db.session.add(Post(uid=43, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=107, c2_number=201,
                    league="Legacy", name="Lady Killer", time=datetime.datetime(2016, 12, 20, 15, 22, 22)))
db.session.add(
    Post(uid=44, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=175, c2_number=148, league="Legacy",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 2, 21, 12, 14, 46)))
db.session.add(
    Post(uid=45, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=303, c2_number=137, league="Legacy",
         name="Candy Butcher", time=datetime.datetime(2016, 3, 22, 12, 4, 14)))
db.session.add(
    Post(uid=46, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=193, c2_number=128, league="Legacy",
         name="Liquid Science", time=datetime.datetime(2016, 8, 27, 6, 28, 19)))
db.session.add(
    Post(uid=47, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=129, c2_number=289, league="Legacy",
         name="Shooter", time=datetime.datetime(2016, 5, 7, 9, 58, 21)))
db.session.add(
    Post(uid=48, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=28, c2_number=153, league="Legacy",
         name="Capital F", time=datetime.datetime(2016, 4, 16, 17, 0, 0)))
db.session.add(
    Post(uid=49, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=97, c2_number=98, league="Legacy",
         name="Little Cobra", time=datetime.datetime(2016, 12, 10, 0, 7, 47)))
db.session.add(
    Post(uid=50, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=192, c2_number=168, league="Legacy",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 7, 17, 15, 36, 56)))
db.session.add(
    Post(uid=51, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=113, c2_number=194, league="Legacy",
         name="Captain Peroxide", time=datetime.datetime(2016, 5, 17, 16, 56, 31)))
db.session.add(
    Post(uid=52, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=61, c2_number=201, league="Legacy",
         name="Little General", time=datetime.datetime(2016, 1, 28, 4, 44, 4)))
db.session.add(Post(uid=53, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=266, c2_number=163,
                    league="Legacy", name="Skull Crusher", time=datetime.datetime(2016, 9, 21, 16, 8, 52)))
db.session.add(Post(uid=54, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=109, c2_number=266, league="Legacy",
                    name="Celtic Charger", time=datetime.datetime(2016, 11, 5, 17, 13, 41)))
db.session.add(
    Post(uid=55, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=40, c2_number=180, league="Legacy",
         name="Lord Nikon", time=datetime.datetime(2016, 10, 21, 21, 50, 48)))
db.session.add(Post(uid=56, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=44, c2_number=226, league="Legacy",
                    name="Sky Bully", time=datetime.datetime(2016, 1, 2, 3, 40, 54)))
db.session.add(
    Post(uid=57, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=149, c2_number=119, league="Legacy",
         name="Cereal Killer", time=datetime.datetime(2016, 10, 28, 12, 43, 27)))
db.session.add(
    Post(uid=58, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=270, c2_number=21, league="Legacy",
         name="Lord Pistachio", time=datetime.datetime(2016, 3, 8, 0, 46, 8)))
db.session.add(
    Post(uid=59, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=196, c2_number=183, league="Legacy",
         name="Slow Trot", time=datetime.datetime(2016, 10, 25, 2, 32, 10)))
db.session.add(
    Post(uid=60, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=309, c2_number=128, league="Legacy",
         name="Chicago Blackout", time=datetime.datetime(2016, 3, 12, 19, 40, 54)))
db.session.add(
    Post(uid=61, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=134, c2_number=61, league="Legacy",
         name="Mad Irishman", time=datetime.datetime(2016, 9, 22, 14, 33, 20)))
db.session.add(
    Post(uid=62, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=86, c2_number=211, league="Legacy",
         name="Snake Eyes", time=datetime.datetime(2016, 4, 3, 20, 26, 45)))
db.session.add(
    Post(uid=63, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=317, c2_number=91, league="Legacy",
         name="Chocolate Thunder", time=datetime.datetime(2016, 6, 23, 0, 1, 58)))
db.session.add(
    Post(uid=64, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=171, c2_number=128, league="Legacy",
         name="Mad Jack", time=datetime.datetime(2016, 9, 12, 17, 19, 58)))
db.session.add(
    Post(uid=65, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=290, c2_number=62, league="Legacy",
         name="Snow Hound", time=datetime.datetime(2016, 6, 25, 11, 15, 34)))
db.session.add(Post(uid=66, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=271, c2_number=196, league="Legacy",
                    name="Chuckles", time=datetime.datetime(2016, 12, 9, 20, 14, 56)))
db.session.add(Post(uid=67, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=288, c2_number=124, league="Legacy",
                    name="Mad Rascal", time=datetime.datetime(2016, 6, 16, 19, 24, 7)))
db.session.add(
    Post(uid=68, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=184, c2_number=202, league="Legacy",
         name="Sofa King", time=datetime.datetime(2016, 4, 2, 4, 2, 53)))
db.session.add(
    Post(uid=69, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=157, c2_number=195, league="Legacy",
         name="Commando", time=datetime.datetime(2016, 6, 11, 4, 44, 12)))
db.session.add(
    Post(uid=70, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=253, c2_number=241, league="Legacy",
         name="Manimal", time=datetime.datetime(2016, 11, 26, 22, 22, 28)))
db.session.add(Post(uid=71, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=200, c2_number=105,
                    league="Legacy", name="Speedwell", time=datetime.datetime(2016, 10, 21, 15, 15, 47)))
db.session.add(Post(uid=72, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=217, c2_number=56, league="Legacy",
                    name="Cool Whip", time=datetime.datetime(2016, 6, 5, 2, 37, 58)))
db.session.add(
    Post(uid=73, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=288, c2_number=42, league="Legacy",
         name="Marbles", time=datetime.datetime(2016, 5, 24, 12, 48, 30)))
db.session.add(
    Post(uid=74, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=206, c2_number=167, league="Legacy",
         name="Spider Fuji", time=datetime.datetime(2016, 1, 17, 8, 57, 31)))
db.session.add(Post(uid=75, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=36, c2_number=58, league="Legacy",
                    name="Cosmo", time=datetime.datetime(2016, 4, 19, 2, 5, 15)))
db.session.add(
    Post(uid=76, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=247, c2_number=240, league="Legacy",
         name="Married Man", time=datetime.datetime(2016, 8, 15, 9, 1, 53)))
db.session.add(
    Post(uid=77, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=73, c2_number=127, league="Legacy",
         name="Springheel Jack", time=datetime.datetime(2016, 11, 4, 9, 6, 14)))
db.session.add(
    Post(uid=78, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=283, c2_number=248, league="Legacy",
         name="Crash Override", time=datetime.datetime(2016, 7, 8, 8, 46, 50)))
db.session.add(
    Post(uid=79, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=31, c2_number=45, league="Legacy",
         name="Marshmallow", time=datetime.datetime(2016, 2, 16, 10, 14, 30)))
db.session.add(
    Post(uid=80, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=28, c2_number=151, league="Legacy",
         name="Squatch", time=datetime.datetime(2016, 4, 20, 2, 25, 47)))
db.session.add(
    Post(uid=81, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=269, c2_number=213, league="Legacy",
         name="Crash Test", time=datetime.datetime(2016, 10, 22, 12, 48, 49)))
db.session.add(
    Post(uid=82, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=285, c2_number=30, league="Legacy",
         name="Mental", time=datetime.datetime(2016, 1, 14, 16, 30, 38)))
db.session.add(
    Post(uid=83, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=155, c2_number=41, league="Legacy",
         name="Stacker of Wheat", time=datetime.datetime(2016, 6, 1, 2, 30, 48)))
db.session.add(Post(uid=84, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=149, c2_number=109, league="Legacy",
                    name="Crazy Eights", time=datetime.datetime(2016, 6, 15, 0, 58, 43)))
db.session.add(Post(uid=85, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=285, c2_number=34, league="Legacy",
                    name="Mercury Reborn", time=datetime.datetime(2016, 9, 5, 17, 58, 52)))
db.session.add(
    Post(uid=86, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=97, c2_number=137, league="Legacy",
         name="Sugar Man", time=datetime.datetime(2016, 6, 22, 2, 41, 27)))
db.session.add(
    Post(uid=87, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=256, c2_number=143, league="Legacy",
         name="Criss Cross", time=datetime.datetime(2016, 7, 1, 5, 57, 6)))
db.session.add(
    Post(uid=88, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=260, c2_number=218, league="Legacy",
         name="Midas", time=datetime.datetime(2016, 12, 11, 17, 14, 18)))
db.session.add(Post(uid=89, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=123, c2_number=101,
                    league="Legacy", name="Suicide Jockey", time=datetime.datetime(2016, 6, 21, 11, 16, 58)))
db.session.add(Post(uid=90, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=22, c2_number=73, league="Legacy",
                    name="Cross Thread", time=datetime.datetime(2016, 10, 8, 12, 29, 32)))
db.session.add(
    Post(uid=91, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=135, c2_number=222, league="Legacy",
         name="Midnight Rambler", time=datetime.datetime(2016, 10, 23, 8, 38, 56)))
db.session.add(Post(uid=92, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=79, c2_number=139, league="Legacy",
                    name="Swampmasher", time=datetime.datetime(2016, 1, 27, 17, 30, 22)))
db.session.add(
    Post(uid=93, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=303, c2_number=140, league="Legacy",
         name="Cujo", time=datetime.datetime(2016, 7, 20, 15, 47, 12)))
db.session.add(
    Post(uid=94, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=32, c2_number=94, league="Legacy",
         name="Midnight Rider", time=datetime.datetime(2016, 10, 14, 19, 6, 48)))
db.session.add(
    Post(uid=95, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=88, c2_number=171, league="Legacy",
         name="Swerve", time=datetime.datetime(2016, 9, 2, 2, 12, 45)))
db.session.add(
    Post(uid=96, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=40, c2_number=220, league="Legacy",
         name="Dancing Madman", time=datetime.datetime(2016, 4, 20, 2, 33, 26)))
db.session.add(
    Post(uid=97, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=27, c2_number=255, league="Legacy",
         name="Mindless Bobcat", time=datetime.datetime(2016, 2, 7, 22, 44, 32)))
db.session.add(
    Post(uid=98, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=119, c2_number=145, league="Legacy",
         name="Tacklebox", time=datetime.datetime(2016, 10, 15, 18, 25, 42)))
db.session.add(
    Post(uid=99, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=133, c2_number=243, league="Legacy",
         name="Dangle", time=datetime.datetime(2016, 4, 22, 5, 10, 35)))
db.session.add(
    Post(uid=100, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=30, c2_number=208, league="Legacy",
         name="Mr. 44", time=datetime.datetime(2016, 3, 9, 14, 22, 13)))
db.session.add(
    Post(uid=101, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=50, c2_number=45, league="Legacy",
         name="Take Away", time=datetime.datetime(2016, 9, 24, 20, 35, 49)))
db.session.add(Post(uid=102, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=60, c2_number=309, league="Legacy",
                    name="Dark Horse", time=datetime.datetime(2016, 6, 28, 4, 16, 29)))
db.session.add(Post(uid=103, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=128, c2_number=134, league="Legacy",
                    name="Mr. Fabulous", time=datetime.datetime(2016, 8, 16, 14, 3, 53)))
db.session.add(
    Post(uid=104, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=153, c2_number=76, league="Legacy",
         name="Tan Stallion", time=datetime.datetime(2016, 1, 1, 8, 32, 7)))
db.session.add(
    Post(uid=105, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=220, c2_number=55, league="Legacy",
         name="Day Hawk", time=datetime.datetime(2016, 8, 7, 19, 18, 1)))
db.session.add(
    Post(uid=106, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=148, c2_number=224, league="Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 2, 26, 4, 17, 4)))
db.session.add(Post(uid=107, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=314, c2_number=241,
                    league="Legacy", name="The China Wall", time=datetime.datetime(2016, 11, 8, 20, 22, 56)))
db.session.add(
    Post(uid=108, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=145, c2_number=269, league="Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 5, 20, 14, 43, 56)))
db.session.add(
    Post(uid=109, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=152, c2_number=243, league="Legacy",
         name="Mr. Lucky", time=datetime.datetime(2016, 5, 4, 9, 42, 32)))
db.session.add(
    Post(uid=110, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=157, c2_number=45, league="Legacy",
         name="The Dude", time=datetime.datetime(2016, 3, 21, 22, 3, 24)))
db.session.add(
    Post(uid=111, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=112, c2_number=48, league="Legacy",
         name="Digger", time=datetime.datetime(2016, 7, 15, 4, 34, 56)))
db.session.add(
    Post(uid=112, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=26, c2_number=45, league="Legacy",
         name="Mr. Peppermint", time=datetime.datetime(2016, 4, 25, 22, 17, 40)))
db.session.add(
    Post(uid=113, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=91, c2_number=295, league="Legacy",
         name="The Flying Mouse", time=datetime.datetime(2016, 2, 23, 3, 56, 39)))
db.session.add(
    Post(uid=114, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=171, c2_number=21, league="Legacy",
         name="Disco Thunder", time=datetime.datetime(2016, 10, 27, 18, 42, 16)))
db.session.add(
    Post(uid=115, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=208, c2_number=55, league="Legacy",
         name="Mr. Spy", time=datetime.datetime(2016, 10, 21, 9, 54, 51)))
db.session.add(
    Post(uid=116, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=58, c2_number=39, league="Legacy",
         name="The Happy Jock", time=datetime.datetime(2016, 5, 21, 20, 35, 50)))
db.session.add(
    Post(uid=117, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=70, c2_number=69, league="Legacy",
         name="Disco Potato", time=datetime.datetime(2016, 7, 23, 9, 3, 49)))
db.session.add(
    Post(uid=118, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=28, c2_number=270, league="Legacy",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 4, 18, 0, 13, 22)))
db.session.add(
    Post(uid=119, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=114, c2_number=245, league="Legacy",
         name="The Howling Swede", time=datetime.datetime(2016, 3, 6, 8, 46, 24)))
db.session.add(
    Post(uid=120, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=284, c2_number=66, league="Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 10, 20, 8, 21, 54)))
db.session.add(
    Post(uid=121, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=275, c2_number=32, league="Legacy",
         name="Mr. Wholesome", time=datetime.datetime(2016, 11, 11, 9, 26, 55)))
db.session.add(
    Post(uid=122, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=47, c2_number=85, league="Legacy",
         name="Thrasher", time=datetime.datetime(2016, 4, 6, 21, 24, 24)))
db.session.add(
    Post(uid=123, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=202, c2_number=274, league="Legacy",
         name="Dredd", time=datetime.datetime(2016, 3, 18, 3, 27, 12)))
db.session.add(Post(uid=124, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=48, c2_number=154, league="Legacy",
                    name="Mud Pie Man", time=datetime.datetime(2016, 3, 28, 17, 8, 6)))
db.session.add(
    Post(uid=125, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=233, c2_number=217, league="Legacy",
         name="Toe", time=datetime.datetime(2016, 2, 15, 2, 55, 30)))
db.session.add(Post(uid=126, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=146, c2_number=28, league="Legacy",
                    name="Dropkick", time=datetime.datetime(2016, 3, 15, 9, 55, 9)))
db.session.add(
    Post(uid=127, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=146, c2_number=174, league="Legacy",
         name="Mule Skinner", time=datetime.datetime(2016, 2, 4, 7, 20, 18)))
db.session.add(Post(uid=128, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=213, c2_number=109, league="Legacy",
                    name="Toolmaker", time=datetime.datetime(2016, 12, 3, 1, 2, 55)))
db.session.add(Post(uid=129, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=150, c2_number=65, league="Legacy",
                    name="Drop Stone", time=datetime.datetime(2016, 5, 23, 0, 37, 45)))
db.session.add(
    Post(uid=130, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=214, c2_number=292, league="Legacy",
         name="Murmur", time=datetime.datetime(2016, 8, 26, 13, 40, 27)))
db.session.add(Post(uid=131, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=85, c2_number=92, league="Legacy",
                    name="Tough Nut", time=datetime.datetime(2016, 4, 8, 11, 14, 47)))
db.session.add(
    Post(uid=132, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=267, c2_number=280, league="Legacy",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 8, 21, 6, 51, 44)))
db.session.add(
    Post(uid=133, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=292, c2_number=307, league="Legacy",
         name="Nacho", time=datetime.datetime(2016, 5, 1, 20, 56, 6)))
db.session.add(Post(uid=134, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=75, c2_number=184, league="Legacy",
                    name="Trip", time=datetime.datetime(2016, 4, 5, 19, 32, 25)))
db.session.add(Post(uid=135, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=26, c2_number=304, league="Legacy",
                    name="Easy Sweep", time=datetime.datetime(2016, 8, 22, 5, 11, 54)))
db.session.add(Post(uid=136, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=246, c2_number=32, league="Legacy",
                    name="Natural Mess", time=datetime.datetime(2016, 7, 14, 19, 15, 34)))
db.session.add(
    Post(uid=137, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=298, c2_number=275, league="Legacy",
         name="Troubadour", time=datetime.datetime(2016, 2, 14, 6, 31, 22)))
db.session.add(Post(uid=138, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=252, c2_number=134, league="Legacy",
                    name="Electric Player", time=datetime.datetime(2016, 4, 19, 5, 53, 45)))
db.session.add(Post(uid=139, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=207, c2_number=234, league="Legacy",
                    name="Necromancer", time=datetime.datetime(2016, 2, 23, 15, 3, 32)))
db.session.add(
    Post(uid=140, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=108, c2_number=229, league="Legacy",
         name="Turnip King", time=datetime.datetime(2016, 8, 12, 12, 30, 54)))
db.session.add(Post(uid=141, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=88, c2_number=108, league="Legacy",
                    name="Esquire", time=datetime.datetime(2016, 2, 7, 11, 58, 37)))
db.session.add(Post(uid=142, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=61, c2_number=74, league="Legacy",
                    name="Neophyte Believer", time=datetime.datetime(2016, 8, 3, 9, 39, 22)))
db.session.add(
    Post(uid=143, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=288, c2_number=131, league="Legacy",
         name="Twitch", time=datetime.datetime(2016, 2, 3, 9, 29, 17)))
db.session.add(Post(uid=144, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=165, c2_number=251, league="Legacy",
                    name="Fast Draw", time=datetime.datetime(2016, 1, 15, 10, 31, 44)))
db.session.add(Post(uid=145, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=54, c2_number=52, league="Legacy",
                    name="Nessie", time=datetime.datetime(2016, 8, 4, 3, 55, 41)))
db.session.add(Post(uid=146, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=61, c2_number=136, league="Legacy",
                    name="Vagabond Warrior", time=datetime.datetime(2016, 2, 2, 3, 8, 49)))
db.session.add(
    Post(uid=147, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=35, c2_number=89, league="Legacy", name="Flakes",
         time=datetime.datetime(2016, 7, 28, 18, 11, 3)))
db.session.add(
    Post(uid=148, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=125, c2_number=301, league="Legacy",
         name="New Cycle", time=datetime.datetime(2016, 7, 22, 21, 57, 11)))
db.session.add(
    Post(uid=149, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=125, c2_number=145, league="Legacy",
         name="Voluntary", time=datetime.datetime(2016, 9, 15, 12, 27, 2)))
db.session.add(
    Post(uid=150, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=234, c2_number=269, league="Legacy",
         name="Flint", time=datetime.datetime(2016, 7, 28, 3, 3, 53)))
db.session.add(
    Post(uid=151, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=189, c2_number=59, league="Legacy",
         name="Nickname Master", time=datetime.datetime(2016, 8, 4, 9, 51, 6)))
db.session.add(Post(uid=152, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=273, c2_number=99, league="Legacy",
                    name="Vortex", time=datetime.datetime(2016, 8, 17, 1, 11, 11)))
db.session.add(Post(uid=153, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=180, c2_number=295, league="Legacy",
                    name="Freak", time=datetime.datetime(2016, 7, 8, 22, 2, 22)))
db.session.add(Post(uid=154, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=114, c2_number=268, league="Legacy",
                    name="Nightmare King", time=datetime.datetime(2016, 5, 9, 11, 45, 10)))
db.session.add(
    Post(uid=155, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=102, c2_number=148, league="Legacy",
         name="Washer", time=datetime.datetime(2016, 4, 27, 0, 24, 26)))
db.session.add(
    Post(uid=156, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=25, c2_number=177, league="Legacy", name="Gas Man",
         time=datetime.datetime(2016, 11, 16, 18, 58, 14)))
db.session.add(Post(uid=157, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=175, c2_number=225, league="Legacy",
                    name="Night Train", time=datetime.datetime(2016, 3, 2, 18, 24, 29)))
db.session.add(Post(uid=158, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=234, c2_number=105, league="Legacy",
                    name="Waylay Dave", time=datetime.datetime(2016, 2, 27, 13, 38, 35)))
db.session.add(Post(uid=159, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=308, c2_number=301, league="Legacy",
                    name="Glyph", time=datetime.datetime(2016, 4, 8, 18, 44, 50)))
db.session.add(
    Post(uid=160, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=288, c2_number=87, league="Legacy",
         name="Old Man Winter", time=datetime.datetime(2016, 4, 3, 21, 35, 32)))
db.session.add(Post(uid=161, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=316, c2_number=144,
                    league="Legacy", name="Wheels", time=datetime.datetime(2016, 1, 23, 11, 38, 54)))
db.session.add(Post(uid=162, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=63, c2_number=249, league="Legacy",
                    name="Grave Digger", time=datetime.datetime(2016, 10, 28, 16, 10, 43)))
db.session.add(
    Post(uid=163, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=189, c2_number=247, league="Legacy",
         name="Old Orange Eyes", time=datetime.datetime(2016, 2, 1, 2, 51, 34)))
db.session.add(
    Post(uid=164, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=87, c2_number=229, league="Legacy",
         name="Wooden Man", time=datetime.datetime(2016, 12, 23, 14, 14, 14)))
db.session.add(
    Post(uid=165, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=156, c2_number=189, league="Legacy",
         name="Guillotine", time=datetime.datetime(2016, 11, 28, 15, 52, 8)))
db.session.add(
    Post(uid=166, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=74, c2_number=49, league="Legacy",
         name="Old Regret", time=datetime.datetime(2016, 4, 8, 17, 2, 8)))
db.session.add(
    Post(uid=167, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=249, c2_number=217, league="Legacy",
         name="Woo Woo", time=datetime.datetime(2016, 9, 28, 12, 23, 15)))
db.session.add(
    Post(uid=168, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=61, c2_number=24, league="Legacy",
         name="Gunhawk", time=datetime.datetime(2016, 6, 2, 21, 19, 36)))
db.session.add(
    Post(uid=169, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=201, c2_number=291, league="Legacy",
         name="Onion King", time=datetime.datetime(2016, 5, 10, 8, 50, 42)))
db.session.add(
    Post(uid=170, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=119, c2_number=118, league="Legacy",
         name="Yellow Menace", time=datetime.datetime(2016, 1, 22, 10, 23, 22)))
db.session.add(
    Post(uid=171, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=186, c2_number=53, league="Legacy",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 12, 27, 7, 36, 40)))
db.session.add(
    Post(uid=172, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=282, c2_number=199, league="Legacy",
         name="Osprey", time=datetime.datetime(2016, 9, 8, 14, 56, 33)))
db.session.add(
    Post(uid=173, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=271, c2_number=58, league="Legacy",
         name="Zero Charisma", time=datetime.datetime(2016, 8, 7, 21, 55, 57)))
db.session.add(Post(uid=174, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=89, c2_number=110, league="Legacy",
                    name="Highlander Monk", time=datetime.datetime(2016, 12, 12, 10, 57, 32)))
db.session.add(Post(uid=175, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=304, c2_number=91, league="Legacy",
                    name="Overrun", time=datetime.datetime(2016, 8, 16, 22, 41, 30)))
db.session.add(
    Post(uid=176, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=26, c2_number=251, league="Legacy",
         name="Zesty Dragon", time=datetime.datetime(2016, 6, 11, 10, 35, 6)))
db.session.add(
    Post(uid=177, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=184, c2_number=177, league="Legacy",
         name="Zod", time=datetime.datetime(2016, 7, 26, 15, 7, 42)))
db.session.add(
    Post(uid=0, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=110, c2_number=165, league="Legacy", name="101",
         time=datetime.datetime(2016, 7, 22, 0, 5, 26)))
db.session.add(
    Post(uid=1, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=223, c2_number=245, league="Legacy",
         name="Houston", time=datetime.datetime(2016, 9, 25, 16, 11, 57)))
db.session.add(Post(uid=2, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=111, c2_number=196, league="Legacy",
                    name="Pinball Wizard", time=datetime.datetime(2016, 6, 2, 12, 19, 51)))
db.session.add(
    Post(uid=3, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=188, c2_number=133, league="Legacy",
         name="Accidental Genius", time=datetime.datetime(2016, 6, 12, 15, 9, 9)))
db.session.add(
    Post(uid=4, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=35, c2_number=304, league="Legacy", name="Hyper",
         time=datetime.datetime(2016, 11, 7, 21, 55, 28)))
db.session.add(Post(uid=5, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=129, c2_number=212, league="Legacy",
                    name="Pluto", time=datetime.datetime(2016, 3, 3, 18, 3, 50)))
db.session.add(
    Post(uid=6, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=221, c2_number=184, league="Legacy",
         name="Alpha", time=datetime.datetime(2016, 1, 4, 1, 9, 35)))
db.session.add(
    Post(uid=7, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=229, c2_number=175, league="Legacy",
         name="Jester", time=datetime.datetime(2016, 11, 25, 17, 21, 5)))
db.session.add(
    Post(uid=8, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=224, c2_number=223, league="Legacy",
         name="Pogue", time=datetime.datetime(2016, 12, 12, 7, 2, 5)))
db.session.add(
    Post(uid=9, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=62, c2_number=185, league="Legacy",
         name="Airport Hobo", time=datetime.datetime(2016, 6, 20, 21, 18, 10)))
db.session.add(
    Post(uid=10, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=151, c2_number=287, league="Legacy",
         name="Jigsaw", time=datetime.datetime(2016, 2, 14, 3, 20, 23)))
db.session.add(
    Post(uid=11, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=110, c2_number=172, league="Legacy",
         name="Prometheus", time=datetime.datetime(2016, 10, 8, 19, 27, 52)))
db.session.add(
    Post(uid=12, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=146, c2_number=239, league="Legacy",
         name="Bearded Angler", time=datetime.datetime(2016, 4, 6, 22, 33, 38)))
db.session.add(
    Post(uid=13, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=135, c2_number=307, league="Legacy",
         name="Joker's Grin", time=datetime.datetime(2016, 11, 25, 8, 51, 19)))
db.session.add(Post(uid=14, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=139, c2_number=93, league="Legacy",
                    name="Psycho Thinker", time=datetime.datetime(2016, 5, 27, 22, 26, 11)))
db.session.add(Post(uid=15, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=29, c2_number=107, league="Legacy",
                    name="Beetle King", time=datetime.datetime(2016, 5, 15, 6, 16, 10)))
db.session.add(
    Post(uid=16, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=261, c2_number=258, league="Legacy",
         name="Judge", time=datetime.datetime(2016, 3, 15, 5, 16, 23)))
db.session.add(Post(uid=17, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=194, c2_number=269, league="Legacy",
                    name="Pusher", time=datetime.datetime(2016, 2, 25, 12, 36, 39)))
db.session.add(
    Post(uid=18, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=112, c2_number=195, league="Hardcore Legacy",
         name="Bitmap", time=datetime.datetime(2016, 3, 18, 19, 53, 19)))
db.session.add(Post(uid=19, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=52, c2_number=141,
                    league="Hardcore Legacy", name="Junkyard Dog", time=datetime.datetime(2016, 1, 18, 3, 25, 25)))
db.session.add(
    Post(uid=20, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=158, c2_number=73, league="Hardcore Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 9, 24, 2, 43, 3)))
db.session.add(
    Post(uid=21, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=306, c2_number=50, league="Hardcore Legacy",
         name="Blister", time=datetime.datetime(2016, 3, 13, 3, 17, 58)))
db.session.add(
    Post(uid=22, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=222, c2_number=141, league="Hardcore Legacy",
         name="K-9", time=datetime.datetime(2016, 2, 7, 12, 58, 1)))
db.session.add(
    Post(uid=23, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=152, c2_number=259, league="Hardcore Legacy",
         name="Roadblock", time=datetime.datetime(2016, 11, 2, 18, 9, 33)))
db.session.add(Post(uid=24, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=58, c2_number=30,
                    league="Hardcore Legacy", name="Bowie", time=datetime.datetime(2016, 2, 22, 5, 38, 4)))
db.session.add(Post(uid=25, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=284, c2_number=111,
                    league="Hardcore Legacy", name="Keystone", time=datetime.datetime(2016, 1, 7, 1, 11, 38)))
db.session.add(
    Post(uid=26, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=239, c2_number=34, league="Hardcore Legacy",
         name="Rooster", time=datetime.datetime(2016, 1, 26, 13, 57, 21)))
db.session.add(Post(uid=27, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=33, c2_number=28,
                    league="Hardcore Legacy", name="Bowler", time=datetime.datetime(2016, 9, 13, 6, 49, 6)))
db.session.add(
    Post(uid=28, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=150, c2_number=73, league="Hardcore Legacy",
         name="Kickstart", time=datetime.datetime(2016, 3, 3, 1, 35, 12)))
db.session.add(
    Post(uid=29, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=191, c2_number=235, league="Hardcore Legacy",
         name="Sandbox", time=datetime.datetime(2016, 5, 23, 10, 26, 40)))
db.session.add(
    Post(uid=30, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=172, c2_number=78, league="Hardcore Legacy",
         name="Breadmaker", time=datetime.datetime(2016, 9, 13, 16, 10, 1)))
db.session.add(Post(uid=31, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=92, c2_number=275,
                    league="Hardcore Legacy", name="Kill Switch", time=datetime.datetime(2016, 11, 17, 20, 52, 3)))
db.session.add(
    Post(uid=32, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=174, c2_number=187, league="Hardcore Legacy",
         name="Scrapper", time=datetime.datetime(2016, 4, 21, 0, 4, 13)))
db.session.add(
    Post(uid=33, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=261, c2_number=305, league="Hardcore Legacy",
         name="Broomspun", time=datetime.datetime(2016, 5, 4, 2, 7, 49)))
db.session.add(
    Post(uid=34, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=79, c2_number=118, league="Hardcore Legacy",
         name="Kingfisher", time=datetime.datetime(2016, 10, 28, 0, 26, 55)))
db.session.add(
    Post(uid=35, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=50, c2_number=162, league="Hardcore Legacy",
         name="Screwtape", time=datetime.datetime(2016, 8, 22, 19, 44, 22)))
db.session.add(Post(uid=36, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=277, c2_number=260,
                    league="Hardcore Legacy", name="Buckshot", time=datetime.datetime(2016, 10, 14, 9, 29, 13)))
db.session.add(
    Post(uid=37, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=33, c2_number=91,
         league="Hardcore Legacy", name="Kitchen", time=datetime.datetime(2016, 10, 18, 13, 16, 18)))
db.session.add(Post(uid=38, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=168, c2_number=44,
                    league="Hardcore Legacy", name="Sexual Chocolate", time=datetime.datetime(2016, 7, 1, 6, 45, 17)))
db.session.add(Post(uid=39, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=205, c2_number=155,
                    league="Hardcore Legacy", name="Bugger", time=datetime.datetime(2016, 11, 4, 13, 49, 51)))
db.session.add(Post(uid=40, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=235, c2_number=42,
                    league="Hardcore Legacy", name="Knuckles", time=datetime.datetime(2016, 6, 1, 16, 55, 49)))
db.session.add(Post(uid=41, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=128, c2_number=252,
                    league="Hardcore Legacy", name="Shadow Chaser", time=datetime.datetime(2016, 3, 17, 6, 25, 22)))
db.session.add(Post(uid=42, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=144, c2_number=53,
                    league="Hardcore Legacy", name="Cabbie", time=datetime.datetime(2016, 8, 26, 22, 9, 41)))
db.session.add(Post(uid=43, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=286, c2_number=267,
                    league="Hardcore Legacy", name="Lady Killer", time=datetime.datetime(2016, 7, 24, 17, 30, 9)))
db.session.add(Post(uid=44, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=82, c2_number=230,
                    league="Hardcore Legacy", name="Sherwood Gladiator",
                    time=datetime.datetime(2016, 4, 16, 3, 58, 49)))
db.session.add(Post(uid=45, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=38, c2_number=80,
                    league="Hardcore Legacy", name="Candy Butcher", time=datetime.datetime(2016, 1, 25, 4, 39, 8)))
db.session.add(Post(uid=46, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=299, c2_number=48,
                    league="Hardcore Legacy", name="Liquid Science", time=datetime.datetime(2016, 8, 24, 17, 58, 51)))
db.session.add(Post(uid=47, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=243, c2_number=99,
                    league="Hardcore Legacy", name="Shooter", time=datetime.datetime(2016, 10, 8, 15, 50, 21)))
db.session.add(Post(uid=48, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=177, c2_number=224,
                    league="Hardcore Legacy", name="Capital F", time=datetime.datetime(2016, 6, 16, 4, 37, 41)))
db.session.add(Post(uid=49, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=62, c2_number=259,
                    league="Hardcore Legacy", name="Little Cobra", time=datetime.datetime(2016, 1, 24, 13, 4, 5)))
db.session.add(Post(uid=50, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=313, c2_number=97,
                    league="Hardcore Legacy", name="Sidewalk Enforcer", time=datetime.datetime(2016, 6, 16, 22, 45, 9)))
db.session.add(Post(uid=51, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=273, c2_number=54,
                    league="Hardcore Legacy", name="Captain Peroxide", time=datetime.datetime(2016, 6, 27, 0, 34, 12)))
db.session.add(Post(uid=52, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=316, c2_number=188,
                    league="Hardcore Legacy", name="Little General", time=datetime.datetime(2016, 2, 11, 13, 21, 0)))
db.session.add(Post(uid=53, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=278, c2_number=101,
                    league="Hardcore Legacy", name="Skull Crusher", time=datetime.datetime(2016, 8, 22, 13, 21, 39)))
db.session.add(
    Post(uid=54, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=259, c2_number=211, league="Hardcore Legacy",
         name="Celtic Charger", time=datetime.datetime(2016, 4, 22, 1, 2, 4)))
db.session.add(Post(uid=55, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=128, c2_number=233,
                    league="Hardcore Legacy", name="Lord Nikon", time=datetime.datetime(2016, 5, 23, 16, 34, 4)))
db.session.add(
    Post(uid=56, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=144, c2_number=198, league="Hardcore Legacy",
         name="Sky Bully", time=datetime.datetime(2016, 1, 23, 8, 45, 0)))
db.session.add(
    Post(uid=57, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=25, c2_number=250, league="Hardcore Legacy",
         name="Cereal Killer", time=datetime.datetime(2016, 7, 16, 21, 49, 56)))
db.session.add(
    Post(uid=58, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=51, c2_number=22, league="Hardcore Legacy",
         name="Lord Pistachio", time=datetime.datetime(2016, 8, 18, 3, 33, 38)))
db.session.add(
    Post(uid=59, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=316, c2_number=25, league="Hardcore Legacy",
         name="Slow Trot", time=datetime.datetime(2016, 6, 15, 9, 44, 4)))
db.session.add(Post(uid=60, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=303, c2_number=131,
                    league="Hardcore Legacy", name="Chicago Blackout", time=datetime.datetime(2016, 5, 20, 16, 0, 44)))
db.session.add(
    Post(uid=61, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=207, c2_number=199, league="Hardcore Legacy",
         name="Mad Irishman", time=datetime.datetime(2016, 7, 20, 3, 3, 54)))
db.session.add(
    Post(uid=62, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=167, c2_number=90, league="Hardcore Legacy",
         name="Snake Eyes", time=datetime.datetime(2016, 12, 11, 4, 7, 26)))
db.session.add(Post(uid=63, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=311, c2_number=161,
                    league="Hardcore Legacy", name="Chocolate Thunder",
                    time=datetime.datetime(2016, 10, 25, 19, 51, 55)))
db.session.add(
    Post(uid=64, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=227, c2_number=227, league="Hardcore Legacy",
         name="Mad Jack", time=datetime.datetime(2016, 9, 9, 6, 51, 37)))
db.session.add(
    Post(uid=65, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=281, c2_number=132, league="Hardcore Legacy",
         name="Snow Hound", time=datetime.datetime(2016, 1, 15, 5, 25, 53)))
db.session.add(
    Post(uid=66, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=151, c2_number=135, league="Hardcore Legacy",
         name="Chuckles", time=datetime.datetime(2016, 6, 18, 19, 39, 6)))
db.session.add(
    Post(uid=67, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=142, c2_number=49, league="Hardcore Legacy",
         name="Mad Rascal", time=datetime.datetime(2016, 6, 13, 18, 36, 48)))
db.session.add(
    Post(uid=68, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=233, c2_number=157, league="Hardcore Legacy",
         name="Sofa King", time=datetime.datetime(2016, 4, 25, 5, 54, 1)))
db.session.add(
    Post(uid=69, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=114, c2_number=139, league="Hardcore Legacy",
         name="Commando", time=datetime.datetime(2016, 12, 14, 5, 37, 16)))
db.session.add(
    Post(uid=70, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=191, c2_number=242, league="Hardcore Legacy",
         name="Manimal", time=datetime.datetime(2016, 10, 26, 5, 35, 10)))
db.session.add(
    Post(uid=71, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=25, c2_number=89, league="Hardcore Legacy",
         name="Speedwell", time=datetime.datetime(2016, 9, 24, 5, 49, 55)))
db.session.add(
    Post(uid=72, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=146, c2_number=295, league="Hardcore Legacy",
         name="Cool Whip", time=datetime.datetime(2016, 3, 6, 12, 33, 17)))
db.session.add(Post(uid=73, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=125, c2_number=21,
                    league="Hardcore Legacy", name="Marbles", time=datetime.datetime(2016, 6, 28, 16, 58, 2)))
db.session.add(
    Post(uid=74, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=125, c2_number=141, league="Hardcore Legacy",
         name="Spider Fuji", time=datetime.datetime(2016, 3, 2, 19, 5, 5)))
db.session.add(Post(uid=75, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=26, c2_number=222,
                    league="Hardcore Legacy", name="Cosmo", time=datetime.datetime(2016, 11, 27, 11, 54, 58)))
db.session.add(
    Post(uid=76, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=67, c2_number=207, league="Hardcore Legacy",
         name="Married Man", time=datetime.datetime(2016, 8, 2, 12, 0, 15)))
db.session.add(
    Post(uid=77, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=52, c2_number=303, league="Hardcore Legacy",
         name="Springheel Jack", time=datetime.datetime(2016, 10, 9, 4, 17, 25)))
db.session.add(Post(uid=78, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=311, c2_number=261,
                    league="Hardcore Legacy", name="Crash Override", time=datetime.datetime(2016, 1, 3, 10, 53, 23)))
db.session.add(Post(uid=79, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=222, c2_number=25,
                    league="Hardcore Legacy", name="Marshmallow", time=datetime.datetime(2016, 8, 11, 1, 0, 32)))
db.session.add(Post(uid=80, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=216, c2_number=303,
                    league="Hardcore Legacy", name="Squatch", time=datetime.datetime(2016, 4, 13, 20, 18, 39)))
db.session.add(Post(uid=81, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=255, c2_number=113,
                    league="Hardcore Legacy", name="Crash Test", time=datetime.datetime(2016, 10, 9, 0, 47, 48)))
db.session.add(
    Post(uid=82, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=95, c2_number=42, league="Hardcore Legacy",
         name="Mental", time=datetime.datetime(2016, 11, 1, 0, 22, 15)))
db.session.add(Post(uid=83, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=129, c2_number=225,
                    league="Hardcore Legacy", name="Stacker of Wheat", time=datetime.datetime(2016, 6, 11, 16, 24, 55)))
db.session.add(Post(uid=84, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=77, c2_number=252,
                    league="Hardcore Legacy", name="Crazy Eights", time=datetime.datetime(2016, 7, 13, 7, 0, 28)))
db.session.add(Post(uid=85, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=216, c2_number=122,
                    league="Hardcore Legacy", name="Mercury Reborn", time=datetime.datetime(2016, 5, 1, 0, 11, 38)))
db.session.add(
    Post(uid=86, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=137, c2_number=223, league="Hardcore Legacy",
         name="Sugar Man", time=datetime.datetime(2016, 6, 1, 5, 57, 39)))
db.session.add(
    Post(uid=87, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=47, c2_number=174, league="Hardcore Legacy",
         name="Criss Cross", time=datetime.datetime(2016, 9, 6, 17, 34, 40)))
db.session.add(Post(uid=88, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=245, c2_number=244,
                    league="Hardcore Legacy", name="Midas", time=datetime.datetime(2016, 6, 24, 22, 23, 16)))
db.session.add(
    Post(uid=89, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=224, c2_number=56, league="Hardcore Legacy",
         name="Suicide Jockey", time=datetime.datetime(2016, 12, 5, 16, 3, 1)))
db.session.add(
    Post(uid=90, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=258, c2_number=121, league="Hardcore Legacy",
         name="Cross Thread", time=datetime.datetime(2016, 2, 11, 15, 4, 7)))
db.session.add(Post(uid=91, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=122, c2_number=64,
                    league="Hardcore Legacy", name="Midnight Rambler", time=datetime.datetime(2016, 12, 12, 0, 16, 52)))
db.session.add(
    Post(uid=92, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=276, c2_number=277, league="Hardcore Legacy",
         name="Swampmasher", time=datetime.datetime(2016, 8, 15, 8, 19, 13)))
db.session.add(
    Post(uid=93, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=252, c2_number=246, league="Hardcore Legacy",
         name="Cujo", time=datetime.datetime(2016, 9, 21, 6, 44, 38)))
db.session.add(
    Post(uid=94, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=269, c2_number=219, league="Hardcore Legacy",
         name="Midnight Rider", time=datetime.datetime(2016, 3, 21, 12, 43, 42)))
db.session.add(
    Post(uid=95, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=100, c2_number=39, league="Hardcore Legacy",
         name="Swerve", time=datetime.datetime(2016, 2, 22, 5, 36, 9)))
db.session.add(Post(uid=96, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=264, c2_number=296,
                    league="Hardcore Legacy", name="Dancing Madman", time=datetime.datetime(2016, 10, 1, 6, 57, 55)))
db.session.add(
    Post(uid=97, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=187, c2_number=152, league="Hardcore Legacy",
         name="Mindless Bobcat", time=datetime.datetime(2016, 1, 6, 5, 49, 19)))
db.session.add(
    Post(uid=98, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=34, c2_number=144, league="Hardcore Legacy",
         name="Tacklebox", time=datetime.datetime(2016, 2, 19, 2, 5, 44)))
db.session.add(Post(uid=99, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=102, c2_number=314,
                    league="Hardcore Legacy", name="Dangle", time=datetime.datetime(2016, 11, 2, 7, 12, 15)))
db.session.add(
    Post(uid=100, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=292, c2_number=49, league="Hardcore Legacy",
         name="Mr. 44", time=datetime.datetime(2016, 5, 23, 9, 45, 45)))
db.session.add(
    Post(uid=101, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=126, c2_number=316, league="Hardcore Legacy",
         name="Take Away", time=datetime.datetime(2016, 8, 23, 4, 44, 57)))
db.session.add(
    Post(uid=102, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=167, c2_number=248, league="Hardcore Legacy",
         name="Dark Horse", time=datetime.datetime(2016, 1, 23, 7, 38, 13)))
db.session.add(Post(uid=103, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=274, c2_number=138,
                    league="Hardcore Legacy", name="Mr. Fabulous", time=datetime.datetime(2016, 1, 12, 10, 51, 36)))
db.session.add(
    Post(uid=104, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=170, c2_number=279, league="Hardcore Legacy",
         name="Tan Stallion", time=datetime.datetime(2016, 9, 8, 21, 46, 37)))
db.session.add(
    Post(uid=105, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=308, c2_number=212, league="Hardcore Legacy",
         name="Day Hawk", time=datetime.datetime(2016, 3, 23, 0, 40, 56)))
db.session.add(
    Post(uid=106, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=312, c2_number=79, league="Hardcore Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 4, 11, 0, 44, 54)))
db.session.add(
    Post(uid=107, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=216, c2_number=132, league="Hardcore Legacy",
         name="The China Wall", time=datetime.datetime(2016, 8, 6, 2, 47, 0)))
db.session.add(
    Post(uid=108, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=104, c2_number=244, league="Hardcore Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 3, 8, 4, 17, 28)))
db.session.add(Post(uid=109, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=188, c2_number=185,
                    league="Hardcore Legacy", name="Mr. Lucky", time=datetime.datetime(2016, 6, 25, 22, 57, 20)))
db.session.add(
    Post(uid=110, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=166, c2_number=113, league="Hardcore Legacy",
         name="The Dude", time=datetime.datetime(2016, 5, 28, 19, 23, 9)))
db.session.add(
    Post(uid=111, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=187, c2_number=74, league="Hardcore Legacy",
         name="Digger", time=datetime.datetime(2016, 1, 15, 5, 20, 41)))
db.session.add(
    Post(uid=112, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=255, c2_number=85, league="Hardcore Legacy",
         name="Mr. Peppermint", time=datetime.datetime(2016, 4, 16, 2, 17, 42)))
db.session.add(
    Post(uid=113, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=293, c2_number=30, league="Hardcore Legacy",
         name="The Flying Mouse", time=datetime.datetime(2016, 2, 17, 14, 28, 39)))
db.session.add(Post(uid=114, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=268, c2_number=221,
                    league="Hardcore Legacy", name="Disco Thunder", time=datetime.datetime(2016, 7, 22, 16, 17, 41)))
db.session.add(Post(uid=115, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=146, c2_number=315,
                    league="Hardcore Legacy", name="Mr. Spy", time=datetime.datetime(2016, 10, 10, 2, 38, 8)))
db.session.add(Post(uid=116, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=30, c2_number=280,
                    league="Hardcore Legacy", name="The Happy Jock", time=datetime.datetime(2016, 1, 10, 19, 14, 55)))
db.session.add(Post(uid=117, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=208, c2_number=215,
                    league="Hardcore Legacy", name="Disco Potato", time=datetime.datetime(2016, 3, 9, 7, 51, 23)))
db.session.add(
    Post(uid=118, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=54, c2_number=235, league="Hardcore Legacy",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 6, 17, 15, 20, 43)))
db.session.add(
    Post(uid=119, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=33, c2_number=26, league="Hardcore Legacy",
         name="The Howling Swede", time=datetime.datetime(2016, 5, 9, 3, 2, 52)))
db.session.add(
    Post(uid=120, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=129, c2_number=78, league="Hardcore Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 6, 12, 0, 16, 12)))
db.session.add(Post(uid=121, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=74, c2_number=144,
                    league="Hardcore Legacy", name="Mr. Wholesome", time=datetime.datetime(2016, 11, 23, 14, 28, 6)))
db.session.add(
    Post(uid=122, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=102, c2_number=170, league="Hardcore Legacy",
         name="Thrasher", time=datetime.datetime(2016, 12, 26, 8, 37, 30)))
db.session.add(
    Post(uid=123, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=231, c2_number=184, league="Hardcore Legacy",
         name="Dredd", time=datetime.datetime(2016, 5, 11, 4, 34, 31)))
db.session.add(Post(uid=124, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=254, c2_number=284,
                    league="Hardcore Legacy", name="Mud Pie Man", time=datetime.datetime(2016, 9, 27, 14, 23, 24)))
db.session.add(
    Post(uid=125, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=256, c2_number=234, league="Hardcore Legacy",
         name="Toe", time=datetime.datetime(2016, 5, 3, 17, 35, 8)))
db.session.add(Post(uid=126, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=203, c2_number=182,
                    league="Hardcore Legacy", name="Dropkick", time=datetime.datetime(2016, 9, 23, 6, 6, 32)))
db.session.add(Post(uid=127, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=122, c2_number=150,
                    league="Hardcore Legacy", name="Mule Skinner", time=datetime.datetime(2016, 1, 6, 13, 19, 55)))
db.session.add(Post(uid=128, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=271, c2_number=201,
                    league="Hardcore Legacy", name="Toolmaker", time=datetime.datetime(2016, 1, 7, 13, 3, 53)))
db.session.add(Post(uid=129, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=50, c2_number=113,
                    league="Hardcore Legacy", name="Drop Stone", time=datetime.datetime(2016, 6, 13, 6, 36, 8)))
db.session.add(Post(uid=130, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=124, c2_number=99,
                    league="Hardcore Legacy", name="Murmur", time=datetime.datetime(2016, 3, 17, 0, 6, 12)))
db.session.add(Post(uid=131, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=114, c2_number=259,
                    league="Hardcore Legacy", name="Tough Nut", time=datetime.datetime(2016, 8, 1, 3, 40, 0)))
db.session.add(Post(uid=132, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=215, c2_number=292,
                    league="Hardcore Legacy", name="Drugstore Cowboy", time=datetime.datetime(2016, 7, 24, 14, 8, 52)))
db.session.add(Post(uid=133, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=76, c2_number=138,
                    league="Hardcore Legacy", name="Nacho", time=datetime.datetime(2016, 11, 19, 3, 25, 35)))
db.session.add(Post(uid=134, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=211, c2_number=174,
                    league="Hardcore Legacy", name="Trip", time=datetime.datetime(2016, 5, 24, 4, 43, 1)))
db.session.add(Post(uid=135, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=100, c2_number=295,
                    league="Hardcore Legacy", name="Easy Sweep", time=datetime.datetime(2016, 8, 3, 5, 54, 18)))
db.session.add(Post(uid=136, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=275, c2_number=256,
                    league="Hardcore Legacy", name="Natural Mess", time=datetime.datetime(2016, 12, 9, 6, 51, 35)))
db.session.add(Post(uid=137, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=268, c2_number=25,
                    league="Hardcore Legacy", name="Troubadour", time=datetime.datetime(2016, 6, 26, 0, 36, 53)))
db.session.add(Post(uid=138, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=193, c2_number=313,
                    league="Hardcore Legacy", name="Electric Player", time=datetime.datetime(2016, 2, 21, 7, 22, 46)))
db.session.add(Post(uid=139, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=157, c2_number=232,
                    league="Hardcore Legacy", name="Necromancer", time=datetime.datetime(2016, 4, 5, 7, 11, 48)))
db.session.add(Post(uid=140, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=99, c2_number=46,
                    league="Hardcore Legacy", name="Turnip King", time=datetime.datetime(2016, 2, 20, 5, 25, 32)))
db.session.add(Post(uid=141, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=260, c2_number=73,
                    league="Hardcore Legacy", name="Esquire", time=datetime.datetime(2016, 9, 11, 2, 14, 39)))
db.session.add(Post(uid=142, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=308, c2_number=111,
                    league="Hardcore Legacy", name="Neophyte Believer", time=datetime.datetime(2016, 2, 12, 0, 54, 13)))
db.session.add(Post(uid=143, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=136, c2_number=97,
                    league="Hardcore Legacy", name="Twitch", time=datetime.datetime(2016, 4, 8, 9, 25, 49)))
db.session.add(Post(uid=144, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=256, c2_number=243,
                    league="Hardcore Legacy", name="Fast Draw", time=datetime.datetime(2016, 7, 24, 8, 11, 28)))
db.session.add(Post(uid=145, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=91, c2_number=210,
                    league="Hardcore Legacy", name="Nessie", time=datetime.datetime(2016, 8, 25, 6, 25, 28)))
db.session.add(
    Post(uid=146, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=284, c2_number=276, league="Hardcore Legacy",
         name="Vagabond Warrior", time=datetime.datetime(2016, 8, 3, 1, 37, 25)))
db.session.add(Post(uid=147, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=147, c2_number=162,
                    league="Hardcore Legacy", name="Flakes", time=datetime.datetime(2016, 9, 4, 8, 19, 25)))
db.session.add(Post(uid=148, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=116, c2_number=157,
                    league="Hardcore Legacy", name="New Cycle", time=datetime.datetime(2016, 4, 20, 14, 16, 27)))
db.session.add(Post(uid=149, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=223, c2_number=316,
                    league="Hardcore Legacy", name="Voluntary", time=datetime.datetime(2016, 8, 6, 2, 48, 17)))
db.session.add(Post(uid=150, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=319, c2_number=46,
                    league="Hardcore Legacy", name="Flint", time=datetime.datetime(2016, 12, 7, 4, 25, 54)))
db.session.add(Post(uid=151, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=150, c2_number=180,
                    league="Hardcore Legacy", name="Nickname Master", time=datetime.datetime(2016, 4, 22, 21, 53, 18)))
db.session.add(Post(uid=152, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=244, c2_number=64,
                    league="Hardcore Legacy", name="Vortex", time=datetime.datetime(2016, 4, 5, 12, 58, 35)))
db.session.add(Post(uid=153, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=293, c2_number=219,
                    league="Hardcore Legacy", name="Freak", time=datetime.datetime(2016, 9, 3, 19, 57, 33)))
db.session.add(Post(uid=154, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=31, c2_number=172,
                    league="Hardcore Legacy", name="Nightmare King", time=datetime.datetime(2016, 12, 6, 15, 41, 29)))
db.session.add(Post(uid=155, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=101, c2_number=244,
                    league="Hardcore Legacy", name="Washer", time=datetime.datetime(2016, 6, 14, 3, 39, 0)))
db.session.add(Post(uid=156, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=243, c2_number=34,
                    league="Hardcore Legacy", name="Gas Man", time=datetime.datetime(2016, 9, 13, 21, 4, 1)))
db.session.add(Post(uid=157, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=42, c2_number=165,
                    league="Hardcore Legacy", name="Night Train", time=datetime.datetime(2016, 5, 17, 11, 53, 13)))
db.session.add(
    Post(uid=158, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=100, c2_number=86, league="Hardcore Legacy",
         name="Waylay Dave", time=datetime.datetime(2016, 2, 17, 12, 54, 14)))
db.session.add(
    Post(uid=159, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=106, c2_number=198, league="Hardcore Legacy",
         name="Glyph", time=datetime.datetime(2016, 9, 18, 15, 53, 6)))
db.session.add(Post(uid=160, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=281, c2_number=33,
                    league="Hardcore Legacy", name="Old Man Winter", time=datetime.datetime(2016, 5, 23, 3, 52, 49)))
db.session.add(Post(uid=161, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=284, c2_number=309,
                    league="Hardcore Legacy", name="Wheels", time=datetime.datetime(2016, 3, 16, 18, 15, 35)))
db.session.add(Post(uid=162, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=287, c2_number=314,
                    league="Hardcore Legacy", name="Grave Digger", time=datetime.datetime(2016, 7, 12, 20, 3, 13)))
db.session.add(Post(uid=163, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=227, c2_number=33,
                    league="Hardcore Legacy", name="Old Orange Eyes", time=datetime.datetime(2016, 11, 8, 15, 39, 2)))
db.session.add(
    Post(uid=164, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=168, c2_number=92, league="Hardcore Legacy",
         name="Wooden Man", time=datetime.datetime(2016, 7, 8, 6, 0, 8)))
db.session.add(Post(uid=165, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=105, c2_number=296,
                    league="Hardcore Legacy", name="Guillotine", time=datetime.datetime(2016, 4, 23, 6, 24, 7)))
db.session.add(Post(uid=166, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=287, c2_number=192,
                    league="Hardcore Legacy", name="Old Regret", time=datetime.datetime(2016, 12, 15, 8, 19, 29)))
db.session.add(Post(uid=167, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=287, c2_number=280,
                    league="Hardcore Legacy", name="Woo Woo", time=datetime.datetime(2016, 7, 27, 2, 1, 44)))
db.session.add(Post(uid=168, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=102, c2_number=155,
                    league="Hardcore Legacy", name="Gunhawk", time=datetime.datetime(2016, 12, 7, 8, 26, 2)))
db.session.add(Post(uid=169, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=35, c2_number=31,
                    league="Hardcore Legacy", name="Onion King", time=datetime.datetime(2016, 4, 17, 6, 25, 57)))
db.session.add(Post(uid=170, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=178, c2_number=122,
                    league="Hardcore Legacy", name="Yellow Menace", time=datetime.datetime(2016, 2, 5, 18, 30, 29)))
db.session.add(Post(uid=171, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=203, c2_number=120,
                    league="Hardcore Legacy", name="High Kingdom Warrior",
                    time=datetime.datetime(2016, 12, 18, 18, 25, 9)))
db.session.add(Post(uid=172, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=168, c2_number=217,
                    league="Hardcore Legacy", name="Osprey", time=datetime.datetime(2016, 12, 1, 3, 13, 22)))
db.session.add(Post(uid=173, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=86, c2_number=229,
                    league="Hardcore Legacy", name="Zero Charisma", time=datetime.datetime(2016, 10, 21, 5, 16, 44)))
db.session.add(Post(uid=174, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=212, c2_number=124,
                    league="Hardcore Legacy", name="Highlander Monk", time=datetime.datetime(2016, 1, 28, 22, 50, 44)))
db.session.add(Post(uid=175, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=233, c2_number=274,
                    league="Hardcore Legacy", name="Overrun", time=datetime.datetime(2016, 8, 25, 18, 50, 11)))
db.session.add(
    Post(uid=176, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=49, c2_number=54, league="Hardcore Legacy",
         name="Zesty Dragon", time=datetime.datetime(2016, 12, 26, 2, 15, 1)))
db.session.add(
    Post(uid=177, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=172, c2_number=319, league="Hardcore Legacy",
         name="Zod", time=datetime.datetime(2016, 6, 7, 8, 13, 30)))
db.session.add(Post(uid=0, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=58, c2_number=242,
                    league="Hardcore Legacy", name="101", time=datetime.datetime(2016, 1, 14, 11, 58, 55)))
db.session.add(
    Post(uid=1, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=102, c2_number=82, league="Hardcore Legacy",
         name="Houston", time=datetime.datetime(2016, 5, 27, 1, 41, 49)))
db.session.add(Post(uid=2, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=103, c2_number=318,
                    league="Hardcore Legacy", name="Pinball Wizard", time=datetime.datetime(2016, 5, 18, 3, 29, 42)))
db.session.add(Post(uid=3, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=37, c2_number=40,
                    league="Hardcore Legacy", name="Accidental Genius", time=datetime.datetime(2016, 8, 16, 5, 39, 27)))
db.session.add(
    Post(uid=4, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=99, c2_number=148, league="Hardcore Legacy",
         name="Hyper", time=datetime.datetime(2016, 8, 4, 17, 9, 27)))
db.session.add(Post(uid=5, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=217, c2_number=200,
                    league="Hardcore Legacy", name="Pluto", time=datetime.datetime(2016, 9, 1, 13, 47, 6)))
db.session.add(Post(uid=6, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=170, c2_number=65,
                    league="Hardcore Legacy", name="Alpha", time=datetime.datetime(2016, 10, 6, 20, 56, 32)))
db.session.add(Post(uid=7, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=60, c2_number=214,
                    league="Hardcore Legacy", name="Jester", time=datetime.datetime(2016, 3, 4, 17, 47, 19)))
db.session.add(Post(uid=8, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=92, c2_number=60,
                    league="Hardcore Legacy", name="Pogue", time=datetime.datetime(2016, 11, 4, 16, 9, 55)))
db.session.add(Post(uid=9, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=237, c2_number=84,
                    league="Hardcore Legacy", name="Airport Hobo", time=datetime.datetime(2016, 12, 8, 14, 51, 40)))
db.session.add(Post(uid=10, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=110, c2_number=214,
                    league="Hardcore Legacy", name="Jigsaw", time=datetime.datetime(2016, 4, 17, 6, 48, 5)))
db.session.add(Post(uid=11, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=165, c2_number=205,
                    league="Hardcore Legacy", name="Prometheus", time=datetime.datetime(2016, 8, 12, 22, 38, 17)))
db.session.add(Post(uid=12, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=22, c2_number=191,
                    league="Hardcore Legacy", name="Bearded Angler", time=datetime.datetime(2016, 4, 2, 19, 19, 10)))
db.session.add(Post(uid=13, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=172, c2_number=50,
                    league="Hardcore Legacy", name="Joker's Grin", time=datetime.datetime(2016, 11, 27, 5, 15, 26)))
db.session.add(Post(uid=14, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=190, c2_number=131,
                    league="Hardcore Legacy", name="Psycho Thinker", time=datetime.datetime(2016, 4, 10, 9, 26, 49)))
db.session.add(Post(uid=15, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=91, c2_number=188,
                    league="Hardcore Legacy", name="Beetle King", time=datetime.datetime(2016, 3, 5, 2, 12, 36)))
db.session.add(Post(uid=16, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=208, c2_number=45,
                    league="Hardcore Legacy", name="Judge", time=datetime.datetime(2016, 4, 6, 9, 19, 44)))
db.session.add(
    Post(uid=17, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=39, c2_number=66, league="Hardcore Legacy",
         name="Pusher", time=datetime.datetime(2016, 6, 19, 6, 23, 31)))
db.session.add(Post(uid=18, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=31, c2_number=30,
                    league="Hardcore Legacy", name="Bitmap", time=datetime.datetime(2016, 6, 15, 18, 52, 34)))
db.session.add(Post(uid=19, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=143, c2_number=139,
                    league="Hardcore Legacy", name="Junkyard Dog", time=datetime.datetime(2016, 12, 19, 19, 32, 25)))
db.session.add(
    Post(uid=20, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=197, c2_number=21, league="Hardcore Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 8, 19, 5, 32, 58)))
db.session.add(Post(uid=21, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=109, c2_number=105,
                    league="Hardcore Legacy", name="Blister", time=datetime.datetime(2016, 4, 16, 0, 10, 22)))
db.session.add(
    Post(uid=22, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=155, c2_number=154, league="Hardcore Legacy",
         name="K-9", time=datetime.datetime(2016, 8, 20, 19, 35, 44)))
db.session.add(
    Post(uid=23, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=36, c2_number=51, league="Hardcore Legacy",
         name="Roadblock", time=datetime.datetime(2016, 4, 9, 5, 41, 4)))
db.session.add(
    Post(uid=24, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=312, c2_number=122, league="Hardcore Legacy",
         name="Bowie", time=datetime.datetime(2016, 4, 12, 9, 4, 34)))
db.session.add(
    Post(uid=25, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=274, c2_number=162, league="Hardcore Legacy",
         name="Keystone", time=datetime.datetime(2016, 8, 17, 2, 49, 25)))
db.session.add(Post(uid=26, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=109, c2_number=301,
                    league="Hardcore Legacy", name="Rooster", time=datetime.datetime(2016, 7, 28, 15, 28, 21)))
db.session.add(Post(uid=27, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=62, c2_number=293,
                    league="Hardcore Legacy", name="Bowler", time=datetime.datetime(2016, 10, 17, 3, 36, 37)))
db.session.add(Post(uid=28, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=47, c2_number=90,
                    league="Hardcore Legacy", name="Kickstart", time=datetime.datetime(2016, 6, 15, 15, 39, 31)))
db.session.add(Post(uid=29, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=82, c2_number=55,
                    league="Hardcore Legacy", name="Sandbox", time=datetime.datetime(2016, 8, 14, 14, 45, 46)))
db.session.add(Post(uid=30, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=97, c2_number=101,
                    league="Hardcore Legacy", name="Breadmaker", time=datetime.datetime(2016, 10, 7, 7, 28, 3)))
db.session.add(Post(uid=31, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=148, c2_number=233,
                    league="Hardcore Legacy", name="Kill Switch", time=datetime.datetime(2016, 7, 27, 11, 41, 4)))
db.session.add(
    Post(uid=32, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=55, c2_number=60, league="Hardcore Legacy",
         name="Scrapper", time=datetime.datetime(2016, 5, 18, 3, 31, 8)))
db.session.add(Post(uid=33, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=156, c2_number=44,
                    league="Hardcore Legacy", name="Broomspun", time=datetime.datetime(2016, 3, 10, 5, 33, 17)))
db.session.add(
    Post(uid=34, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=129, c2_number=111, league="Hardcore Legacy",
         name="Kingfisher", time=datetime.datetime(2016, 4, 25, 5, 14, 58)))
db.session.add(
    Post(uid=35, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=120, c2_number=115, league="Hardcore Legacy",
         name="Screwtape", time=datetime.datetime(2016, 6, 26, 12, 33, 2)))
db.session.add(Post(uid=36, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=147, c2_number=51,
                    league="Hardcore Legacy", name="Buckshot", time=datetime.datetime(2016, 10, 2, 13, 10, 24)))
db.session.add(
    Post(uid=37, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=293, c2_number=34, league="Hardcore Legacy",
         name="Kitchen", time=datetime.datetime(2016, 2, 4, 0, 7, 25)))
db.session.add(
    Post(uid=38, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=155, c2_number=62, league="Hardcore Legacy",
         name="Sexual Chocolate", time=datetime.datetime(2016, 6, 1, 10, 47, 19)))
db.session.add(Post(uid=39, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=314, c2_number=299,
                    league="Hardcore Legacy", name="Bugger", time=datetime.datetime(2016, 12, 14, 18, 12, 33)))
db.session.add(
    Post(uid=40, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=184, c2_number=128, league="Hardcore Legacy",
         name="Knuckles", time=datetime.datetime(2016, 8, 14, 4, 19, 18)))
db.session.add(Post(uid=41, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=140, c2_number=68,
                    league="Hardcore Legacy", name="Shadow Chaser", time=datetime.datetime(2016, 11, 19, 1, 42, 55)))
db.session.add(
    Post(uid=42, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=296, c2_number=102, league="Hardcore Legacy",
         name="Cabbie", time=datetime.datetime(2016, 6, 8, 1, 29, 44)))
db.session.add(
    Post(uid=43, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=127, c2_number=178, league="Hardcore Legacy",
         name="Lady Killer", time=datetime.datetime(2016, 7, 13, 1, 22, 33)))
db.session.add(Post(uid=44, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=150, c2_number=156,
                    league="Hardcore Legacy", name="Sherwood Gladiator",
                    time=datetime.datetime(2016, 5, 12, 6, 11, 30)))
db.session.add(Post(uid=45, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=140, c2_number=213,
                    league="Hardcore Legacy", name="Candy Butcher", time=datetime.datetime(2016, 11, 22, 18, 55, 23)))
db.session.add(Post(uid=46, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=260, c2_number=216,
                    league="Hardcore Legacy", name="Liquid Science", time=datetime.datetime(2016, 10, 16, 7, 12, 13)))
db.session.add(Post(uid=47, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=184, c2_number=35,
                    league="Hardcore Legacy", name="Shooter", time=datetime.datetime(2016, 2, 20, 1, 57, 36)))
db.session.add(Post(uid=48, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=123, c2_number=45,
                    league="Hardcore Legacy", name="Capital F", time=datetime.datetime(2016, 10, 5, 16, 26, 55)))
db.session.add(Post(uid=49, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=270, c2_number=275,
                    league="Hardcore Legacy", name="Little Cobra", time=datetime.datetime(2016, 8, 11, 17, 2, 25)))
db.session.add(Post(uid=50, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=280, c2_number=153,
                    league="Hardcore Legacy", name="Sidewalk Enforcer",
                    time=datetime.datetime(2016, 2, 11, 20, 38, 52)))
db.session.add(Post(uid=51, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=247, c2_number=45,
                    league="Hardcore Legacy", name="Captain Peroxide", time=datetime.datetime(2016, 4, 16, 0, 8, 30)))
db.session.add(
    Post(uid=52, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=245, c2_number=292, league="Hardcore Legacy",
         name="Little General", time=datetime.datetime(2016, 9, 9, 7, 26, 33)))
db.session.add(
    Post(uid=53, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=251, c2_number=122, league="Hardcore Legacy",
         name="Skull Crusher", time=datetime.datetime(2016, 3, 18, 5, 26, 2)))
db.session.add(Post(uid=54, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=74, c2_number=134,
                    league="Hardcore Legacy", name="Celtic Charger", time=datetime.datetime(2016, 11, 24, 20, 21, 30)))
db.session.add(
    Post(uid=55, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=242, c2_number=103, league="Hardcore Legacy",
         name="Lord Nikon", time=datetime.datetime(2016, 12, 21, 13, 30, 53)))
db.session.add(
    Post(uid=56, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=283, c2_number=38, league="Hardcore Legacy",
         name="Sky Bully", time=datetime.datetime(2016, 7, 9, 21, 39, 39)))
db.session.add(Post(uid=57, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=231, c2_number=275,
                    league="Hardcore Legacy", name="Cereal Killer", time=datetime.datetime(2016, 6, 5, 8, 35, 24)))
db.session.add(
    Post(uid=58, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=155, c2_number=197, league="Hardcore Legacy",
         name="Lord Pistachio", time=datetime.datetime(2016, 10, 4, 13, 50, 6)))
db.session.add(Post(uid=59, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=317, c2_number=317,
                    league="Hardcore Legacy", name="Slow Trot", time=datetime.datetime(2016, 6, 7, 4, 1, 18)))
db.session.add(
    Post(uid=60, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=302, c2_number=198, league="Hardcore Legacy",
         name="Chicago Blackout", time=datetime.datetime(2016, 8, 14, 3, 13, 49)))
db.session.add(
    Post(uid=61, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=166, c2_number=167, league="Hardcore Legacy",
         name="Mad Irishman", time=datetime.datetime(2016, 7, 8, 17, 29, 6)))
db.session.add(Post(uid=62, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=231, c2_number=246,
                    league="Hardcore Legacy", name="Snake Eyes", time=datetime.datetime(2016, 12, 18, 0, 11, 41)))
db.session.add(Post(uid=63, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=285, c2_number=256,
                    league="Hardcore Legacy", name="Chocolate Thunder", time=datetime.datetime(2016, 6, 5, 9, 6, 26)))
db.session.add(Post(uid=64, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=259, c2_number=74,
                    league="Hardcore Legacy", name="Mad Jack", time=datetime.datetime(2016, 3, 11, 6, 20, 29)))
db.session.add(Post(uid=65, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=134, c2_number=113,
                    league="Hardcore Legacy", name="Snow Hound", time=datetime.datetime(2016, 6, 23, 6, 36, 29)))
db.session.add(Post(uid=66, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=123, c2_number=126,
                    league="Hardcore Legacy", name="Chuckles", time=datetime.datetime(2016, 12, 14, 13, 45, 41)))
db.session.add(Post(uid=67, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=214, c2_number=277,
                    league="Hardcore Legacy", name="Mad Rascal", time=datetime.datetime(2016, 2, 15, 17, 36, 33)))
db.session.add(Post(uid=68, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=203, c2_number=289,
                    league="Hardcore Legacy", name="Sofa King", time=datetime.datetime(2016, 10, 9, 5, 16, 57)))
db.session.add(Post(uid=69, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=41, c2_number=91,
                    league="Hardcore Legacy", name="Commando", time=datetime.datetime(2016, 2, 16, 10, 13, 20)))
db.session.add(
    Post(uid=70, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=315, c2_number=248, league="Hardcore Legacy",
         name="Manimal", time=datetime.datetime(2016, 8, 12, 5, 50, 31)))
db.session.add(
    Post(uid=71, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=236, c2_number=70, league="Hardcore Legacy",
         name="Speedwell", time=datetime.datetime(2016, 10, 9, 11, 8, 40)))
db.session.add(
    Post(uid=72, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=96, c2_number=42, league="Hardcore Legacy",
         name="Cool Whip", time=datetime.datetime(2016, 2, 3, 12, 28, 24)))
db.session.add(
    Post(uid=73, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=224, c2_number=201, league="Hardcore Legacy",
         name="Marbles", time=datetime.datetime(2016, 6, 3, 4, 50, 55)))
db.session.add(Post(uid=74, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=210, c2_number=215,
                    league="Hardcore Legacy", name="Spider Fuji", time=datetime.datetime(2016, 8, 15, 2, 23, 9)))
db.session.add(Post(uid=75, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=264, c2_number=37,
                    league="Hardcore Legacy", name="Cosmo", time=datetime.datetime(2016, 9, 15, 17, 9, 32)))
db.session.add(
    Post(uid=76, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=159, c2_number=163, league="Hardcore Legacy",
         name="Married Man", time=datetime.datetime(2016, 7, 3, 15, 31, 12)))
db.session.add(Post(uid=77, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=111, c2_number=285,
                    league="Hardcore Legacy", name="Springheel Jack", time=datetime.datetime(2016, 7, 23, 19, 48, 48)))
db.session.add(Post(uid=78, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=193, c2_number=107,
                    league="Hardcore Legacy", name="Crash Override", time=datetime.datetime(2016, 8, 24, 18, 44, 20)))
db.session.add(Post(uid=79, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=189, c2_number=21,
                    league="Hardcore Legacy", name="Marshmallow", time=datetime.datetime(2016, 1, 28, 7, 24, 31)))
db.session.add(Post(uid=80, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=124, c2_number=92,
                    league="Hardcore Legacy", name="Squatch", time=datetime.datetime(2016, 10, 26, 7, 40, 23)))
db.session.add(Post(uid=81, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=194, c2_number=254,
                    league="Hardcore Legacy", name="Crash Test", time=datetime.datetime(2016, 4, 16, 21, 16, 24)))
db.session.add(Post(uid=82, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=249, c2_number=249,
                    league="Hardcore Legacy", name="Mental", time=datetime.datetime(2016, 7, 21, 2, 42, 50)))
db.session.add(Post(uid=83, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=103, c2_number=257,
                    league="Hardcore Legacy", name="Stacker of Wheat", time=datetime.datetime(2016, 9, 5, 22, 30, 6)))
db.session.add(Post(uid=84, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=175, c2_number=82,
                    league="Hardcore Legacy", name="Crazy Eights", time=datetime.datetime(2016, 2, 4, 10, 26, 31)))
db.session.add(Post(uid=85, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=113, c2_number=239,
                    league="Hardcore Legacy", name="Mercury Reborn", time=datetime.datetime(2016, 6, 5, 14, 20, 1)))
db.session.add(Post(uid=86, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=275, c2_number=115,
                    league="Hardcore Legacy", name="Sugar Man", time=datetime.datetime(2016, 11, 21, 4, 14, 22)))
db.session.add(Post(uid=87, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=283, c2_number=224,
                    league="Hardcore Legacy", name="Criss Cross", time=datetime.datetime(2016, 1, 3, 21, 23, 54)))
db.session.add(
    Post(uid=88, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=86, c2_number=151, league="Hardcore Legacy",
         name="Midas", time=datetime.datetime(2016, 12, 24, 4, 9, 23)))
db.session.add(
    Post(uid=89, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=43, c2_number=274, league="Hardcore Legacy",
         name="Suicide Jockey", time=datetime.datetime(2016, 10, 27, 1, 53, 15)))
db.session.add(Post(uid=90, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=303, c2_number=147,
                    league="Hardcore Legacy", name="Cross Thread", time=datetime.datetime(2016, 1, 10, 3, 7, 35)))
db.session.add(Post(uid=91, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=235, c2_number=70,
                    league="Hardcore Legacy", name="Midnight Rambler",
                    time=datetime.datetime(2016, 10, 15, 16, 40, 31)))
db.session.add(
    Post(uid=92, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=297, c2_number=244, league="Hardcore Legacy",
         name="Swampmasher", time=datetime.datetime(2016, 5, 24, 7, 22, 34)))
db.session.add(Post(uid=93, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=66, c2_number=206,
                    league="Hardcore Legacy", name="Cujo", time=datetime.datetime(2016, 5, 5, 8, 29, 16)))
db.session.add(
    Post(uid=94, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=261, c2_number=85, league="Hardcore Legacy",
         name="Midnight Rider", time=datetime.datetime(2016, 5, 1, 14, 43, 18)))
db.session.add(
    Post(uid=95, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=137, c2_number=212, league="Hardcore Legacy",
         name="Swerve", time=datetime.datetime(2016, 1, 19, 3, 34, 3)))
db.session.add(
    Post(uid=96, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=112, c2_number=96, league="Hardcore Legacy",
         name="Dancing Madman", time=datetime.datetime(2016, 2, 7, 2, 1, 21)))
db.session.add(
    Post(uid=97, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=318, c2_number=75, league="Hardcore Legacy",
         name="Mindless Bobcat", time=datetime.datetime(2016, 9, 15, 10, 12, 53)))
db.session.add(Post(uid=98, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=205, c2_number=111,
                    league="Hardcore Legacy", name="Tacklebox", time=datetime.datetime(2016, 5, 12, 11, 27, 1)))
db.session.add(
    Post(uid=99, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=73, c2_number=252, league="Hardcore Legacy",
         name="Dangle", time=datetime.datetime(2016, 10, 6, 19, 33, 41)))
db.session.add(
    Post(uid=100, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=67, c2_number=290, league="Hardcore Legacy",
         name="Mr. 44", time=datetime.datetime(2016, 9, 11, 7, 1, 13)))
db.session.add(Post(uid=101, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=264, c2_number=202,
                    league="Hardcore Legacy", name="Take Away", time=datetime.datetime(2016, 2, 10, 21, 52, 52)))
db.session.add(
    Post(uid=102, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=218, c2_number=292, league="Hardcore Legacy",
         name="Dark Horse", time=datetime.datetime(2016, 12, 2, 3, 50, 33)))
db.session.add(
    Post(uid=103, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=103, c2_number=208, league="Hardcore Legacy",
         name="Mr. Fabulous", time=datetime.datetime(2016, 5, 19, 11, 14, 35)))
db.session.add(
    Post(uid=104, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=217, c2_number=28, league="Hardcore Legacy",
         name="Tan Stallion", time=datetime.datetime(2016, 5, 8, 1, 29, 16)))
db.session.add(Post(uid=105, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=220, c2_number=218,
                    league="Hardcore Legacy", name="Day Hawk", time=datetime.datetime(2016, 3, 27, 2, 21, 52)))
db.session.add(
    Post(uid=106, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=289, c2_number=238, league="Hardcore Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 10, 4, 2, 37, 43)))
db.session.add(
    Post(uid=107, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=112, c2_number=113, league="Hardcore Legacy",
         name="The China Wall", time=datetime.datetime(2016, 12, 12, 19, 53, 51)))
db.session.add(
    Post(uid=108, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=159, c2_number=308, league="Hardcore Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 9, 14, 15, 12, 11)))
db.session.add(
    Post(uid=109, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=222, c2_number=175, league="Hardcore Legacy",
         name="Mr. Lucky", time=datetime.datetime(2016, 3, 17, 5, 13, 16)))
db.session.add(
    Post(uid=110, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=80, c2_number=203, league="Hardcore Legacy",
         name="The Dude", time=datetime.datetime(2016, 11, 3, 6, 36, 31)))
db.session.add(Post(uid=111, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=316, c2_number=238,
                    league="Hardcore Legacy", name="Digger", time=datetime.datetime(2016, 8, 7, 10, 20, 8)))
db.session.add(
    Post(uid=112, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=133, c2_number=190, league="Hardcore Legacy",
         name="Mr. Peppermint", time=datetime.datetime(2016, 4, 1, 0, 42, 40)))
db.session.add(
    Post(uid=113, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=262, c2_number=129, league="Hardcore Legacy",
         name="The Flying Mouse", time=datetime.datetime(2016, 5, 15, 13, 6, 2)))
db.session.add(
    Post(uid=114, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=58, c2_number=193, league="Hardcore Legacy",
         name="Disco Thunder", time=datetime.datetime(2016, 8, 12, 1, 22, 11)))
db.session.add(
    Post(uid=115, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=110, c2_number=96, league="Hardcore Legacy",
         name="Mr. Spy", time=datetime.datetime(2016, 11, 10, 3, 51, 30)))
db.session.add(Post(uid=116, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=282, c2_number=233,
                    league="Hardcore Legacy", name="The Happy Jock", time=datetime.datetime(2016, 8, 23, 18, 15, 13)))
db.session.add(
    Post(uid=117, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=280, c2_number=118, league="Hardcore Legacy",
         name="Disco Potato", time=datetime.datetime(2016, 8, 15, 21, 24, 10)))
db.session.add(
    Post(uid=118, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=64, c2_number=155, league="Hardcore Legacy",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 10, 11, 3, 17, 15)))
db.session.add(Post(uid=119, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=240, c2_number=75,
                    league="Hardcore Legacy", name="The Howling Swede",
                    time=datetime.datetime(2016, 2, 14, 11, 26, 45)))
db.session.add(
    Post(uid=120, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=174, c2_number=121, league="Hardcore Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 7, 22, 12, 25, 30)))
db.session.add(
    Post(uid=121, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=318, c2_number=307, league="Hardcore Legacy",
         name="Mr. Wholesome", time=datetime.datetime(2016, 2, 16, 19, 20, 44)))
db.session.add(
    Post(uid=122, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=316, c2_number=205, league="Hardcore Legacy",
         name="Thrasher", time=datetime.datetime(2016, 10, 24, 7, 36, 32)))
db.session.add(
    Post(uid=123, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=163, c2_number=223, league="Hardcore Legacy",
         name="Dredd", time=datetime.datetime(2016, 8, 6, 9, 38, 28)))
db.session.add(
    Post(uid=124, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=62, c2_number=267, league="Hardcore Legacy",
         name="Mud Pie Man", time=datetime.datetime(2016, 11, 10, 7, 45, 37)))
db.session.add(
    Post(uid=125, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=57, c2_number=200, league="Hardcore Legacy",
         name="Toe", time=datetime.datetime(2016, 10, 16, 4, 32, 8)))
db.session.add(
    Post(uid=126, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=63, c2_number=66, league="Hardcore Legacy",
         name="Dropkick", time=datetime.datetime(2016, 7, 10, 18, 21, 29)))
db.session.add(
    Post(uid=127, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=254, c2_number=113, league="Hardcore Legacy",
         name="Mule Skinner", time=datetime.datetime(2016, 1, 28, 11, 48, 50)))
db.session.add(
    Post(uid=128, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=30, c2_number=47, league="Hardcore Legacy",
         name="Toolmaker", time=datetime.datetime(2016, 11, 25, 19, 35, 42)))
db.session.add(Post(uid=129, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=199, c2_number=32,
                    league="Hardcore Legacy", name="Drop Stone", time=datetime.datetime(2016, 7, 16, 5, 17, 3)))
db.session.add(
    Post(uid=130, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=251, c2_number=248, league="Hardcore Legacy",
         name="Murmur", time=datetime.datetime(2016, 3, 17, 1, 24, 39)))
db.session.add(Post(uid=131, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=281, c2_number=208,
                    league="Hardcore Legacy", name="Tough Nut", time=datetime.datetime(2016, 4, 2, 5, 50, 7)))
db.session.add(
    Post(uid=132, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=151, c2_number=232, league="Hardcore Legacy",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 2, 8, 9, 40, 1)))
db.session.add(Post(uid=133, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=318, c2_number=152,
                    league="Hardcore Legacy", name="Nacho", time=datetime.datetime(2016, 7, 11, 16, 7, 20)))
db.session.add(Post(uid=134, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=36, c2_number=189,
                    league="Hardcore Legacy", name="Trip", time=datetime.datetime(2016, 4, 15, 3, 5, 17)))
db.session.add(Post(uid=135, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=317, c2_number=319,
                    league="Hardcore Legacy", name="Easy Sweep", time=datetime.datetime(2016, 10, 8, 8, 8, 5)))
db.session.add(Post(uid=136, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=222, c2_number=32,
                    league="Hardcore Legacy", name="Natural Mess", time=datetime.datetime(2016, 5, 14, 19, 46, 21)))
db.session.add(Post(uid=137, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=41, c2_number=53,
                    league="Hardcore Legacy", name="Troubadour", time=datetime.datetime(2016, 4, 7, 4, 15, 14)))
db.session.add(Post(uid=138, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=238, c2_number=28,
                    league="Hardcore Legacy", name="Electric Player", time=datetime.datetime(2016, 12, 22, 3, 36, 33)))
db.session.add(Post(uid=139, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=142, c2_number=232,
                    league="Hardcore Legacy", name="Necromancer", time=datetime.datetime(2016, 8, 8, 1, 53, 8)))
db.session.add(Post(uid=140, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=215, c2_number=72,
                    league="Hardcore Legacy", name="Turnip King", time=datetime.datetime(2016, 7, 10, 22, 54, 51)))
db.session.add(Post(uid=141, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=177, c2_number=212,
                    league="Hardcore Legacy", name="Esquire", time=datetime.datetime(2016, 8, 13, 20, 11, 22)))
db.session.add(
    Post(uid=142, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=222, c2_number=252, league="Hardcore Legacy",
         name="Neophyte Believer", time=datetime.datetime(2016, 8, 26, 14, 23, 21)))
db.session.add(
    Post(uid=143, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=104, c2_number=204, league="Hardcore Legacy",
         name="Twitch", time=datetime.datetime(2016, 4, 10, 12, 20, 28)))
db.session.add(Post(uid=144, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=258, c2_number=55,
                    league="Hardcore Legacy", name="Fast Draw", time=datetime.datetime(2016, 11, 15, 17, 38, 6)))
db.session.add(Post(uid=145, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=287, c2_number=299,
                    league="Hardcore Legacy", name="Nessie", time=datetime.datetime(2016, 10, 21, 19, 1, 13)))
db.session.add(
    Post(uid=146, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=225, c2_number=69, league="Hardcore Legacy",
         name="Vagabond Warrior", time=datetime.datetime(2016, 7, 9, 7, 25, 31)))
db.session.add(Post(uid=147, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=141, c2_number=255,
                    league="Hardcore Legacy", name="Flakes", time=datetime.datetime(2016, 12, 2, 20, 24, 36)))
db.session.add(
    Post(uid=148, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=201, c2_number=141, league="Hardcore Legacy",
         name="New Cycle", time=datetime.datetime(2016, 5, 28, 9, 43, 2)))
db.session.add(
    Post(uid=149, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=274, c2_number=39, league="Hardcore Legacy",
         name="Voluntary", time=datetime.datetime(2016, 6, 6, 18, 6, 24)))
db.session.add(
    Post(uid=150, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=37, c2_number=37, league="Hardcore Legacy",
         name="Flint", time=datetime.datetime(2016, 5, 25, 6, 5, 41)))
db.session.add(
    Post(uid=151, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=313, c2_number=108, league="Hardcore Legacy",
         name="Nickname Master", time=datetime.datetime(2016, 5, 26, 10, 41, 50)))
db.session.add(Post(uid=152, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=180, c2_number=287,
                    league="Hardcore Legacy", name="Vortex", time=datetime.datetime(2016, 8, 15, 12, 24, 6)))
db.session.add(Post(uid=153, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=210, c2_number=154,
                    league="Hardcore Legacy", name="Freak", time=datetime.datetime(2016, 6, 12, 22, 34, 42)))
db.session.add(
    Post(uid=154, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=98, c2_number=74, league="Hardcore Legacy",
         name="Nightmare King", time=datetime.datetime(2016, 12, 11, 18, 47, 53)))
db.session.add(Post(uid=155, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=177, c2_number=306,
                    league="Hardcore Legacy", name="Washer", time=datetime.datetime(2016, 9, 16, 19, 24, 5)))
db.session.add(
    Post(uid=156, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=196, c2_number=52, league="Hardcore Legacy",
         name="Gas Man", time=datetime.datetime(2016, 12, 15, 20, 53, 21)))
db.session.add(
    Post(uid=157, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=75, c2_number=145, league="Hardcore Legacy",
         name="Night Train", time=datetime.datetime(2016, 7, 14, 10, 7, 53)))
db.session.add(
    Post(uid=158, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=39, c2_number=291, league="Hardcore Legacy",
         name="Waylay Dave", time=datetime.datetime(2016, 5, 26, 10, 33, 36)))
db.session.add(Post(uid=159, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=74, c2_number=300,
                    league="Hardcore Legacy", name="Glyph", time=datetime.datetime(2016, 1, 21, 14, 3, 58)))
db.session.add(
    Post(uid=160, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=296, c2_number=73, league="Hardcore Legacy",
         name="Old Man Winter", time=datetime.datetime(2016, 11, 3, 22, 34, 56)))
db.session.add(
    Post(uid=161, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=304, c2_number=179, league="Hardcore Legacy",
         name="Wheels", time=datetime.datetime(2016, 2, 7, 6, 40, 6)))
db.session.add(Post(uid=162, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=140, c2_number=120,
                    league="Hardcore Legacy", name="Grave Digger", time=datetime.datetime(2016, 11, 8, 5, 8, 14)))
db.session.add(
    Post(uid=163, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=155, c2_number=78, league="Hardcore Legacy",
         name="Old Orange Eyes", time=datetime.datetime(2016, 5, 21, 13, 47, 44)))
db.session.add(
    Post(uid=164, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=305, c2_number=267, league="Standard",
         name="Wooden Man", time=datetime.datetime(2016, 8, 23, 18, 19, 8)))
db.session.add(Post(uid=165, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=96, c2_number=281,
                    league="Standard", name="Guillotine", time=datetime.datetime(2016, 2, 8, 9, 8, 52)))
db.session.add(
    Post(uid=166, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=278, c2_number=272, league="Standard",
         name="Old Regret", time=datetime.datetime(2016, 4, 22, 0, 35, 57)))
db.session.add(
    Post(uid=167, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=210, c2_number=141, league="Standard",
         name="Woo Woo", time=datetime.datetime(2016, 7, 11, 0, 56, 36)))
db.session.add(
    Post(uid=168, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=228, c2_number=152, league="Standard",
         name="Gunhawk", time=datetime.datetime(2016, 12, 10, 4, 23, 4)))
db.session.add(
    Post(uid=169, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=130, c2_number=77, league="Standard",
         name="Onion King", time=datetime.datetime(2016, 8, 15, 15, 17, 24)))
db.session.add(
    Post(uid=170, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=48, c2_number=89, league="Standard",
         name="Yellow Menace", time=datetime.datetime(2016, 2, 12, 13, 54, 12)))
db.session.add(
    Post(uid=171, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=279, c2_number=113, league="Standard",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 3, 12, 1, 37, 21)))
db.session.add(
    Post(uid=172, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=241, c2_number=267, league="Standard",
         name="Osprey", time=datetime.datetime(2016, 8, 2, 0, 19, 51)))
db.session.add(
    Post(uid=173, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=54, c2_number=113, league="Standard",
         name="Zero Charisma", time=datetime.datetime(2016, 6, 17, 13, 5, 21)))
db.session.add(
    Post(uid=174, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=133, c2_number=282, league="Standard",
         name="Highlander Monk", time=datetime.datetime(2016, 12, 25, 7, 4, 6)))
db.session.add(
    Post(uid=175, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=250, c2_number=240, league="Standard",
         name="Overrun", time=datetime.datetime(2016, 12, 9, 1, 49, 45)))
db.session.add(
    Post(uid=176, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=23, c2_number=165, league="Standard",
         name="Zesty Dragon", time=datetime.datetime(2016, 4, 7, 9, 14, 40)))
db.session.add(
    Post(uid=177, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=113, c2_number=39, league="Standard",
         name="Zod", time=datetime.datetime(2016, 12, 12, 6, 14, 48)))
db.session.add(
    Post(uid=0, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=149, c2_number=63, league="Standard", name="101",
         time=datetime.datetime(2016, 9, 23, 21, 6, 40)))
db.session.add(Post(uid=1, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=172, c2_number=61, league="Standard",
                    name="Houston", time=datetime.datetime(2016, 3, 18, 7, 42, 13)))
db.session.add(
    Post(uid=2, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=172, c2_number=316, league="Standard",
         name="Pinball Wizard", time=datetime.datetime(2016, 12, 2, 16, 12, 42)))
db.session.add(Post(uid=3, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=279, c2_number=52, league="Standard",
                    name="Accidental Genius", time=datetime.datetime(2016, 9, 7, 10, 53, 21)))
db.session.add(
    Post(uid=4, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=41, c2_number=222, league="Standard",
         name="Hyper", time=datetime.datetime(2016, 5, 23, 21, 17, 56)))
db.session.add(
    Post(uid=5, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=261, c2_number=118,
         league="Standard", name="Pluto", time=datetime.datetime(2016, 12, 4, 22, 44, 9)))
db.session.add(
    Post(uid=6, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=117, c2_number=38, league="Standard",
         name="Alpha", time=datetime.datetime(2016, 9, 6, 21, 26, 13)))
db.session.add(Post(uid=7, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=210, c2_number=106,
                    league="Standard", name="Jester", time=datetime.datetime(2016, 5, 20, 16, 13, 49)))
db.session.add(
    Post(uid=8, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=146, c2_number=224, league="Standard",
         name="Pogue", time=datetime.datetime(2016, 7, 21, 16, 20, 44)))
db.session.add(
    Post(uid=9, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=145, c2_number=44, league="Standard",
         name="Airport Hobo", time=datetime.datetime(2016, 7, 4, 12, 52, 14)))
db.session.add(Post(uid=10, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=295, c2_number=216,
                    league="Standard", name="Jigsaw", time=datetime.datetime(2016, 6, 18, 4, 30, 34)))
db.session.add(Post(uid=11, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=260, c2_number=217,
                    league="Standard", name="Prometheus", time=datetime.datetime(2016, 8, 21, 21, 8, 51)))
db.session.add(Post(uid=12, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=158, c2_number=294,
                    league="Standard", name="Bearded Angler", time=datetime.datetime(2016, 11, 21, 22, 28, 21)))
db.session.add(Post(uid=13, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=75, c2_number=164,
                    league="Standard", name="Joker's Grin", time=datetime.datetime(2016, 10, 5, 21, 11, 40)))
db.session.add(Post(uid=14, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=26, c2_number=142,
                    league="Standard", name="Psycho Thinker", time=datetime.datetime(2016, 7, 28, 17, 17, 1)))
db.session.add(Post(uid=15, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=202, c2_number=44,
                    league="Standard", name="Beetle King", time=datetime.datetime(2016, 9, 19, 9, 26, 38)))
db.session.add(Post(uid=16, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=79, c2_number=138,
                    league="Standard", name="Judge", time=datetime.datetime(2016, 6, 11, 13, 32, 24)))
db.session.add(Post(uid=17, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=208, c2_number=167,
                    league="Standard", name="Pusher", time=datetime.datetime(2016, 9, 19, 21, 5, 8)))
db.session.add(
    Post(uid=18, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=218, c2_number=124, league="Standard",
         name="Bitmap", time=datetime.datetime(2016, 11, 9, 0, 11, 40)))
db.session.add(
    Post(uid=19, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=298, c2_number=72, league="Standard",
         name="Junkyard Dog", time=datetime.datetime(2016, 8, 27, 17, 33, 23)))
db.session.add(Post(uid=20, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=91, c2_number=113,
                    league="Standard", name="Riff Raff", time=datetime.datetime(2016, 11, 14, 22, 46, 25)))
db.session.add(Post(uid=21, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=225, c2_number=233,
                    league="Standard", name="Blister", time=datetime.datetime(2016, 2, 23, 19, 57, 13)))
db.session.add(Post(uid=22, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=232, c2_number=256, league="Standard",
                    name="K-9", time=datetime.datetime(2016, 3, 21, 2, 31, 21)))
db.session.add(
    Post(uid=23, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=85, c2_number=216, league="Standard",
         name="Roadblock", time=datetime.datetime(2016, 8, 1, 0, 0, 33)))
db.session.add(
    Post(uid=24, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=181, c2_number=29, league="Standard", name="Bowie",
         time=datetime.datetime(2016, 12, 22, 4, 19, 31)))
db.session.add(
    Post(uid=25, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=286, c2_number=139, league="Standard",
         name="Keystone", time=datetime.datetime(2016, 1, 5, 8, 44, 17)))
db.session.add(Post(uid=26, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=269, c2_number=254, league="Standard",
                    name="Rooster", time=datetime.datetime(2016, 12, 17, 21, 36, 56)))
db.session.add(Post(uid=27, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=284, c2_number=138, league="Standard",
                    name="Bowler", time=datetime.datetime(2016, 3, 20, 5, 22, 2)))
db.session.add(
    Post(uid=28, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=310, c2_number=116, league="Standard",
         name="Kickstart", time=datetime.datetime(2016, 8, 4, 17, 36, 31)))
db.session.add(
    Post(uid=29, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=303, c2_number=228, league="Standard",
         name="Sandbox", time=datetime.datetime(2016, 10, 26, 17, 21, 18)))
db.session.add(
    Post(uid=30, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=71, c2_number=191, league="Standard",
         name="Breadmaker", time=datetime.datetime(2016, 3, 23, 0, 21, 25)))
db.session.add(
    Post(uid=31, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=52, c2_number=88, league="Standard",
         name="Kill Switch", time=datetime.datetime(2016, 5, 8, 21, 19, 38)))
db.session.add(
    Post(uid=32, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=267, c2_number=142, league="Standard",
         name="Scrapper", time=datetime.datetime(2016, 6, 11, 1, 6, 11)))
db.session.add(
    Post(uid=33, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=88, c2_number=214, league="Standard",
         name="Broomspun", time=datetime.datetime(2016, 1, 8, 6, 14, 35)))
db.session.add(
    Post(uid=34, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=275, c2_number=222, league="Standard",
         name="Kingfisher", time=datetime.datetime(2016, 3, 23, 18, 1, 54)))
db.session.add(
    Post(uid=35, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=239, c2_number=87, league="Standard",
         name="Screwtape", time=datetime.datetime(2016, 8, 15, 1, 42, 22)))
db.session.add(Post(uid=36, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=221, c2_number=180, league="Standard",
                    name="Buckshot", time=datetime.datetime(2016, 6, 27, 6, 10, 16)))
db.session.add(Post(uid=37, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=122, c2_number=269, league="Standard",
                    name="Kitchen", time=datetime.datetime(2016, 3, 1, 6, 39, 22)))
db.session.add(
    Post(uid=38, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=144, c2_number=163, league="Standard",
         name="Sexual Chocolate", time=datetime.datetime(2016, 1, 24, 20, 43, 44)))
db.session.add(Post(uid=39, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=195, c2_number=121, league="Standard",
                    name="Bugger", time=datetime.datetime(2016, 7, 21, 1, 0, 34)))
db.session.add(
    Post(uid=40, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=280, c2_number=81, league="Standard",
         name="Knuckles", time=datetime.datetime(2016, 8, 10, 21, 13, 22)))
db.session.add(Post(uid=41, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=143, c2_number=164,
                    league="Standard", name="Shadow Chaser", time=datetime.datetime(2016, 1, 23, 20, 33, 31)))
db.session.add(
    Post(uid=42, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=163, c2_number=66, league="Standard",
         name="Cabbie", time=datetime.datetime(2016, 9, 9, 16, 6, 37)))
db.session.add(
    Post(uid=43, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=74, c2_number=166, league="Standard",
         name="Lady Killer", time=datetime.datetime(2016, 8, 21, 2, 49, 23)))
db.session.add(
    Post(uid=44, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=261, c2_number=85, league="Standard",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 10, 11, 16, 35, 31)))
db.session.add(
    Post(uid=45, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=119, c2_number=236, league="Standard",
         name="Candy Butcher", time=datetime.datetime(2016, 3, 1, 8, 19, 26)))
db.session.add(
    Post(uid=46, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=108, c2_number=305, league="Standard",
         name="Liquid Science", time=datetime.datetime(2016, 11, 5, 22, 34, 50)))
db.session.add(
    Post(uid=47, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=178, c2_number=219, league="Standard",
         name="Shooter", time=datetime.datetime(2016, 6, 15, 0, 35, 42)))
db.session.add(
    Post(uid=48, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=95, c2_number=58, league="Standard",
         name="Capital F", time=datetime.datetime(2016, 10, 12, 20, 15, 45)))
db.session.add(
    Post(uid=49, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=195, c2_number=24, league="Standard",
         name="Little Cobra", time=datetime.datetime(2016, 7, 19, 14, 28, 15)))
db.session.add(
    Post(uid=50, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=189, c2_number=281, league="Standard",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 9, 18, 8, 22, 46)))
db.session.add(
    Post(uid=51, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=58, c2_number=106, league="Standard",
         name="Captain Peroxide", time=datetime.datetime(2016, 6, 28, 4, 55, 28)))
db.session.add(
    Post(uid=52, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=147, c2_number=184, league="Standard",
         name="Little General", time=datetime.datetime(2016, 7, 2, 18, 4, 27)))
db.session.add(
    Post(uid=53, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=264, c2_number=36, league="Standard",
         name="Skull Crusher", time=datetime.datetime(2016, 12, 16, 21, 47, 47)))
db.session.add(
    Post(uid=54, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=219, c2_number=259, league="Standard",
         name="Celtic Charger", time=datetime.datetime(2016, 9, 9, 5, 9, 41)))
db.session.add(Post(uid=55, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=52, c2_number=42, league="Standard",
                    name="Lord Nikon", time=datetime.datetime(2016, 3, 2, 0, 52, 47)))
db.session.add(
    Post(uid=56, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=40, c2_number=83, league="Standard",
         name="Sky Bully", time=datetime.datetime(2016, 5, 6, 10, 7, 3)))
db.session.add(
    Post(uid=57, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=230, c2_number=100, league="Standard",
         name="Cereal Killer", time=datetime.datetime(2016, 4, 27, 16, 24, 17)))
db.session.add(Post(uid=58, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=194, c2_number=43, league="Standard",
                    name="Lord Pistachio", time=datetime.datetime(2016, 12, 8, 11, 4, 19)))
db.session.add(
    Post(uid=59, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=210, c2_number=215, league="Standard",
         name="Slow Trot", time=datetime.datetime(2016, 10, 15, 7, 36, 56)))
db.session.add(Post(uid=60, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=188, c2_number=160, league="Standard",
                    name="Chicago Blackout", time=datetime.datetime(2016, 11, 12, 22, 47, 49)))
db.session.add(
    Post(uid=61, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=39, c2_number=240, league="Standard",
         name="Mad Irishman", time=datetime.datetime(2016, 1, 18, 2, 11, 51)))
db.session.add(Post(uid=62, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=39, c2_number=200, league="Standard",
                    name="Snake Eyes", time=datetime.datetime(2016, 5, 7, 3, 43, 49)))
db.session.add(
    Post(uid=63, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=201, c2_number=213, league="Standard",
         name="Chocolate Thunder", time=datetime.datetime(2016, 1, 12, 21, 4, 32)))
db.session.add(
    Post(uid=64, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=88, c2_number=92, league="Standard",
         name="Mad Jack", time=datetime.datetime(2016, 11, 17, 0, 0, 4)))
db.session.add(
    Post(uid=65, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=172, c2_number=203, league="Standard",
         name="Snow Hound", time=datetime.datetime(2016, 6, 21, 18, 15, 18)))
db.session.add(
    Post(uid=66, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=44, c2_number=92, league="Standard",
         name="Chuckles", time=datetime.datetime(2016, 7, 16, 1, 17, 58)))
db.session.add(
    Post(uid=67, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=236, c2_number=156, league="Standard",
         name="Mad Rascal", time=datetime.datetime(2016, 2, 27, 4, 26, 41)))
db.session.add(
    Post(uid=68, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=36, c2_number=97, league="Standard",
         name="Sofa King", time=datetime.datetime(2016, 4, 8, 8, 36, 27)))
db.session.add(
    Post(uid=69, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=99, c2_number=90, league="Standard",
         name="Commando", time=datetime.datetime(2016, 3, 28, 21, 6, 12)))
db.session.add(
    Post(uid=70, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=118, c2_number=172, league="Standard",
         name="Manimal", time=datetime.datetime(2016, 11, 2, 9, 14, 19)))
db.session.add(
    Post(uid=71, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=271, c2_number=252, league="Standard",
         name="Speedwell", time=datetime.datetime(2016, 11, 16, 18, 6, 25)))
db.session.add(Post(uid=72, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=243, c2_number=191, league="Standard",
                    name="Cool Whip", time=datetime.datetime(2016, 11, 7, 16, 12, 33)))
db.session.add(Post(uid=73, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=64, c2_number=276, league="Standard",
                    name="Marbles", time=datetime.datetime(2016, 3, 2, 15, 55, 4)))
db.session.add(
    Post(uid=74, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=191, c2_number=28, league="Standard",
         name="Spider Fuji", time=datetime.datetime(2016, 5, 18, 16, 46, 40)))
db.session.add(
    Post(uid=75, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=196, c2_number=272, league="Standard",
         name="Cosmo", time=datetime.datetime(2016, 3, 2, 14, 57, 15)))
db.session.add(
    Post(uid=76, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=151, c2_number=80, league="Standard",
         name="Married Man", time=datetime.datetime(2016, 8, 26, 17, 45, 18)))
db.session.add(Post(uid=77, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=259, c2_number=155,
                    league="Standard", name="Springheel Jack", time=datetime.datetime(2016, 8, 19, 19, 21, 23)))
db.session.add(Post(uid=78, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=219, c2_number=139, league="Standard",
                    name="Crash Override", time=datetime.datetime(2016, 10, 13, 0, 35, 56)))
db.session.add(
    Post(uid=79, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=290, c2_number=250, league="Standard",
         name="Marshmallow", time=datetime.datetime(2016, 5, 13, 9, 10, 6)))
db.session.add(
    Post(uid=80, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=206, c2_number=256, league="Standard",
         name="Squatch", time=datetime.datetime(2016, 1, 13, 8, 0, 31)))
db.session.add(
    Post(uid=81, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=237, c2_number=100, league="Standard",
         name="Crash Test", time=datetime.datetime(2016, 3, 28, 21, 46, 17)))
db.session.add(
    Post(uid=82, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=183, c2_number=223, league="Standard",
         name="Mental", time=datetime.datetime(2016, 8, 28, 14, 43, 30)))
db.session.add(
    Post(uid=83, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=66, c2_number=192, league="Standard",
         name="Stacker of Wheat", time=datetime.datetime(2016, 2, 26, 9, 28, 52)))
db.session.add(
    Post(uid=84, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=190, c2_number=303, league="Standard",
         name="Crazy Eights", time=datetime.datetime(2016, 5, 12, 6, 3, 34)))
db.session.add(
    Post(uid=85, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=227, c2_number=209, league="Standard",
         name="Mercury Reborn", time=datetime.datetime(2016, 9, 7, 13, 29, 31)))
db.session.add(
    Post(uid=86, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=49, c2_number=191, league="Standard",
         name="Sugar Man", time=datetime.datetime(2016, 7, 2, 19, 57, 17)))
db.session.add(
    Post(uid=87, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=96, c2_number=139, league="Standard",
         name="Criss Cross", time=datetime.datetime(2016, 8, 19, 19, 58, 23)))
db.session.add(
    Post(uid=88, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=101, c2_number=319, league="Standard",
         name="Midas", time=datetime.datetime(2016, 7, 25, 2, 40, 16)))
db.session.add(
    Post(uid=89, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=121, c2_number=116, league="Standard",
         name="Suicide Jockey", time=datetime.datetime(2016, 5, 28, 8, 47, 13)))
db.session.add(Post(uid=90, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=194, c2_number=55, league="Standard",
                    name="Cross Thread", time=datetime.datetime(2016, 2, 4, 15, 7, 2)))
db.session.add(Post(uid=91, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=315, c2_number=37, league="Standard",
                    name="Midnight Rambler", time=datetime.datetime(2016, 10, 23, 7, 51, 40)))
db.session.add(
    Post(uid=92, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=54, c2_number=163, league="Standard",
         name="Swampmasher", time=datetime.datetime(2016, 12, 28, 9, 19, 55)))
db.session.add(
    Post(uid=93, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=306, c2_number=44, league="Standard",
         name="Cujo", time=datetime.datetime(2016, 9, 28, 17, 7, 9)))
db.session.add(
    Post(uid=94, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=118, c2_number=136, league="Standard",
         name="Midnight Rider", time=datetime.datetime(2016, 8, 21, 12, 57, 39)))
db.session.add(Post(uid=95, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=135, c2_number=134,
                    league="Standard", name="Swerve", time=datetime.datetime(2016, 12, 17, 0, 29, 54)))
db.session.add(
    Post(uid=96, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=200, c2_number=247, league="Standard",
         name="Dancing Madman", time=datetime.datetime(2016, 10, 2, 3, 55, 50)))
db.session.add(
    Post(uid=97, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=154, c2_number=296, league="Standard",
         name="Mindless Bobcat", time=datetime.datetime(2016, 7, 12, 13, 57, 16)))
db.session.add(
    Post(uid=98, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=255, c2_number=117, league="Standard",
         name="Tacklebox", time=datetime.datetime(2016, 8, 7, 6, 49, 57)))
db.session.add(
    Post(uid=99, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=36, c2_number=319, league="Standard",
         name="Dangle", time=datetime.datetime(2016, 9, 23, 13, 50, 55)))
db.session.add(Post(uid=100, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=52, c2_number=255,
                    league="Standard", name="Mr. 44", time=datetime.datetime(2016, 12, 25, 16, 13, 41)))
db.session.add(Post(uid=101, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=235, c2_number=248,
                    league="Standard", name="Take Away", time=datetime.datetime(2016, 11, 23, 13, 39, 57)))
db.session.add(Post(uid=102, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=117, c2_number=196,
                    league="Standard", name="Dark Horse", time=datetime.datetime(2016, 8, 23, 1, 38, 48)))
db.session.add(Post(uid=103, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=178, c2_number=249,
                    league="Standard", name="Mr. Fabulous", time=datetime.datetime(2016, 9, 15, 18, 52, 26)))
db.session.add(
    Post(uid=104, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=76, c2_number=265, league="Standard",
         name="Tan Stallion", time=datetime.datetime(2016, 12, 12, 3, 27, 16)))
db.session.add(
    Post(uid=105, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=188, c2_number=134, league="Standard",
         name="Day Hawk", time=datetime.datetime(2016, 10, 16, 15, 4, 35)))
db.session.add(
    Post(uid=106, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=317, c2_number=257, league="Standard",
         name="Mr. Gadget", time=datetime.datetime(2016, 1, 18, 9, 20, 19)))
db.session.add(Post(uid=107, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=291, c2_number=287,
                    league="Standard", name="The China Wall", time=datetime.datetime(2016, 12, 20, 10, 16, 4)))
db.session.add(
    Post(uid=108, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=55, c2_number=196, league="Standard",
         name="Desert Haze", time=datetime.datetime(2016, 8, 4, 22, 24, 29)))
db.session.add(
    Post(uid=109, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=122, c2_number=313, league="Standard",
         name="Mr. Lucky", time=datetime.datetime(2016, 4, 11, 17, 1, 1)))
db.session.add(
    Post(uid=110, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=118, c2_number=69, league="Standard",
         name="The Dude", time=datetime.datetime(2016, 2, 25, 0, 54, 19)))
db.session.add(
    Post(uid=111, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=93, c2_number=213, league="Standard",
         name="Digger", time=datetime.datetime(2016, 1, 28, 22, 18, 55)))
db.session.add(
    Post(uid=112, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=67, c2_number=93, league="Standard",
         name="Mr. Peppermint", time=datetime.datetime(2016, 2, 11, 17, 28, 50)))
db.session.add(Post(uid=113, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=210, c2_number=170,
                    league="Standard", name="The Flying Mouse", time=datetime.datetime(2016, 3, 7, 15, 6, 55)))
db.session.add(
    Post(uid=114, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=155, c2_number=63, league="Standard",
         name="Disco Thunder", time=datetime.datetime(2016, 6, 22, 6, 56, 56)))
db.session.add(
    Post(uid=115, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=46, c2_number=275, league="Standard",
         name="Mr. Spy", time=datetime.datetime(2016, 3, 25, 1, 3, 0)))
db.session.add(
    Post(uid=116, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=273, c2_number=255, league="Standard",
         name="The Happy Jock", time=datetime.datetime(2016, 7, 16, 14, 41, 52)))
db.session.add(
    Post(uid=117, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=307, c2_number=242, league="Standard",
         name="Disco Potato", time=datetime.datetime(2016, 10, 2, 20, 8, 36)))
db.session.add(
    Post(uid=118, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=317, c2_number=28, league="Standard",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 12, 12, 8, 29, 32)))
db.session.add(
    Post(uid=119, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=253, c2_number=244, league="Standard",
         name="The Howling Swede", time=datetime.datetime(2016, 4, 20, 7, 42, 33)))
db.session.add(
    Post(uid=120, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=235, c2_number=217, league="Standard",
         name="Dr. Cocktail", time=datetime.datetime(2016, 4, 24, 4, 16, 30)))
db.session.add(Post(uid=121, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=226, c2_number=135,
                    league="Standard", name="Mr. Wholesome", time=datetime.datetime(2016, 2, 19, 2, 55, 49)))
db.session.add(
    Post(uid=122, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=22, c2_number=74, league="Standard",
         name="Thrasher", time=datetime.datetime(2016, 7, 7, 0, 33, 43)))
db.session.add(
    Post(uid=123, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=28, c2_number=141, league="Standard",
         name="Dredd", time=datetime.datetime(2016, 1, 16, 21, 10, 35)))
db.session.add(
    Post(uid=124, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=57, c2_number=157, league="Standard",
         name="Mud Pie Man", time=datetime.datetime(2016, 6, 28, 2, 10, 56)))
db.session.add(
    Post(uid=125, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=53, c2_number=182, league="Standard",
         name="Toe", time=datetime.datetime(2016, 12, 25, 9, 35, 34)))
db.session.add(
    Post(uid=126, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=275, c2_number=274, league="Standard",
         name="Dropkick", time=datetime.datetime(2016, 7, 16, 21, 42, 53)))
db.session.add(
    Post(uid=127, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=165, c2_number=244, league="Standard",
         name="Mule Skinner", time=datetime.datetime(2016, 2, 21, 16, 15, 16)))
db.session.add(
    Post(uid=128, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=157, c2_number=180, league="Standard",
         name="Toolmaker", time=datetime.datetime(2016, 4, 28, 12, 23, 50)))
db.session.add(
    Post(uid=129, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=151, c2_number=301, league="Standard",
         name="Drop Stone", time=datetime.datetime(2016, 8, 15, 18, 45, 3)))
db.session.add(
    Post(uid=130, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=291, c2_number=308, league="Standard",
         name="Murmur", time=datetime.datetime(2016, 4, 5, 13, 33, 53)))
db.session.add(Post(uid=131, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=215, c2_number=125,
                    league="Standard", name="Tough Nut", time=datetime.datetime(2016, 8, 22, 20, 42, 43)))
db.session.add(
    Post(uid=132, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=208, c2_number=189, league="Standard",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 2, 19, 22, 44, 32)))
db.session.add(
    Post(uid=133, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=148, c2_number=200, league="Standard",
         name="Nacho", time=datetime.datetime(2016, 10, 22, 15, 34, 28)))
db.session.add(
    Post(uid=134, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=134, c2_number=259, league="Standard",
         name="Trip", time=datetime.datetime(2016, 10, 14, 20, 43, 48)))
db.session.add(
    Post(uid=135, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=274, c2_number=139, league="Standard",
         name="Easy Sweep", time=datetime.datetime(2016, 5, 17, 9, 43, 53)))
db.session.add(Post(uid=136, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=276, c2_number=287,
                    league="Standard", name="Natural Mess", time=datetime.datetime(2016, 9, 3, 7, 37, 21)))
db.session.add(
    Post(uid=137, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=38, c2_number=70, league="Standard",
         name="Troubadour", time=datetime.datetime(2016, 8, 2, 15, 38, 53)))
db.session.add(
    Post(uid=138, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=252, c2_number=221, league="Standard",
         name="Electric Player", time=datetime.datetime(2016, 12, 20, 1, 37, 31)))
db.session.add(Post(uid=139, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=150, c2_number=247,
                    league="Standard", name="Necromancer", time=datetime.datetime(2016, 8, 9, 10, 5, 7)))
db.session.add(
    Post(uid=140, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=258, c2_number=231, league="Standard",
         name="Turnip King", time=datetime.datetime(2016, 11, 2, 5, 55, 8)))
db.session.add(
    Post(uid=141, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=175, c2_number=268, league="Standard",
         name="Esquire", time=datetime.datetime(2016, 12, 26, 22, 0, 57)))
db.session.add(
    Post(uid=142, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=109, c2_number=52, league="Standard",
         name="Neophyte Believer", time=datetime.datetime(2016, 3, 16, 13, 54, 32)))
db.session.add(
    Post(uid=143, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=244, c2_number=262, league="Standard",
         name="Twitch", time=datetime.datetime(2016, 7, 16, 19, 48, 24)))
db.session.add(
    Post(uid=144, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=193, c2_number=249, league="Standard",
         name="Fast Draw", time=datetime.datetime(2016, 10, 9, 1, 15, 6)))
db.session.add(
    Post(uid=145, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=122, c2_number=237, league="Standard",
         name="Nessie", time=datetime.datetime(2016, 8, 24, 5, 19, 46)))
db.session.add(
    Post(uid=146, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=149, c2_number=144, league="Standard",
         name="Vagabond Warrior", time=datetime.datetime(2016, 6, 25, 13, 0, 46)))
db.session.add(
    Post(uid=147, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=227, c2_number=217, league="Standard",
         name="Flakes", time=datetime.datetime(2016, 5, 13, 22, 27, 42)))
db.session.add(
    Post(uid=148, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=260, c2_number=183, league="Standard",
         name="New Cycle", time=datetime.datetime(2016, 12, 27, 7, 56, 16)))
db.session.add(Post(uid=149, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=177, c2_number=40,
                    league="Standard", name="Voluntary", time=datetime.datetime(2016, 1, 3, 0, 33, 13)))
db.session.add(
    Post(uid=150, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=283, c2_number=205, league="Standard",
         name="Flint", time=datetime.datetime(2016, 10, 10, 12, 34, 41)))
db.session.add(
    Post(uid=151, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=43, c2_number=162, league="Standard",
         name="Nickname Master", time=datetime.datetime(2016, 12, 20, 17, 44, 9)))
db.session.add(
    Post(uid=152, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=194, c2_number=117, league="Standard",
         name="Vortex", time=datetime.datetime(2016, 5, 25, 22, 8, 45)))
db.session.add(
    Post(uid=153, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=254, c2_number=99, league="Standard",
         name="Freak", time=datetime.datetime(2016, 5, 21, 2, 41, 7)))
db.session.add(Post(uid=154, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=176, c2_number=64,
                    league="Standard", name="Nightmare King", time=datetime.datetime(2016, 5, 17, 17, 51, 39)))
db.session.add(
    Post(uid=155, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=109, c2_number=60, league="Standard",
         name="Washer", time=datetime.datetime(2016, 4, 15, 22, 23, 38)))
db.session.add(Post(uid=156, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=175, c2_number=265,
                    league="Standard", name="Gas Man", time=datetime.datetime(2016, 2, 7, 3, 10, 52)))
db.session.add(Post(uid=157, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=22, c2_number=130,
                    league="Standard", name="Night Train", time=datetime.datetime(2016, 10, 12, 17, 55, 20)))
db.session.add(
    Post(uid=158, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=162, c2_number=249, league="Standard",
         name="Waylay Dave", time=datetime.datetime(2016, 7, 12, 11, 12, 4)))
db.session.add(
    Post(uid=159, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=288, c2_number=289, league="Standard",
         name="Glyph", time=datetime.datetime(2016, 12, 17, 1, 11, 16)))
db.session.add(
    Post(uid=160, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=34, c2_number=179, league="Standard",
         name="Old Man Winter", time=datetime.datetime(2016, 10, 21, 11, 21, 42)))
db.session.add(Post(uid=161, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=171, c2_number=209,
                    league="Standard", name="Wheels", time=datetime.datetime(2016, 6, 17, 7, 53, 26)))
db.session.add(
    Post(uid=162, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=77, c2_number=135, league="Standard",
         name="Grave Digger", time=datetime.datetime(2016, 6, 18, 2, 54, 25)))
db.session.add(
    Post(uid=163, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=62, c2_number=240, league="Standard",
         name="Old Orange Eyes", time=datetime.datetime(2016, 7, 20, 4, 11, 45)))
db.session.add(
    Post(uid=164, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=261, c2_number=317, league="Standard",
         name="Wooden Man", time=datetime.datetime(2016, 9, 25, 19, 42, 18)))
db.session.add(
    Post(uid=165, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=50, c2_number=116, league="Standard",
         name="Guillotine", time=datetime.datetime(2016, 11, 20, 16, 32, 6)))
db.session.add(
    Post(uid=166, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=152, c2_number=229, league="Standard",
         name="Old Regret", time=datetime.datetime(2016, 7, 6, 17, 48, 26)))
db.session.add(Post(uid=167, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=195, c2_number=280,
                    league="Standard", name="Woo Woo", time=datetime.datetime(2016, 11, 11, 4, 15, 19)))
db.session.add(
    Post(uid=168, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=216, c2_number=212, league="Standard",
         name="Gunhawk", time=datetime.datetime(2016, 1, 13, 13, 50, 46)))
db.session.add(
    Post(uid=169, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=305, c2_number=300, league="Standard",
         name="Onion King", time=datetime.datetime(2016, 1, 7, 7, 4, 25)))
db.session.add(
    Post(uid=170, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=92, c2_number=154, league="Standard",
         name="Yellow Menace", time=datetime.datetime(2016, 2, 17, 13, 0, 36)))
db.session.add(
    Post(uid=171, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=311, c2_number=158, league="Standard",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 10, 22, 22, 16, 19)))
db.session.add(
    Post(uid=172, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=219, c2_number=309, league="Standard",
         name="Osprey", time=datetime.datetime(2016, 5, 18, 20, 30, 29)))
db.session.add(
    Post(uid=173, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=56, c2_number=242, league="Standard",
         name="Zero Charisma", time=datetime.datetime(2016, 9, 10, 4, 26, 16)))
db.session.add(
    Post(uid=174, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=84, c2_number=151, league="Standard",
         name="Highlander Monk", time=datetime.datetime(2016, 7, 10, 10, 21, 11)))
db.session.add(
    Post(uid=175, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=278, c2_number=249, league="Standard",
         name="Overrun", time=datetime.datetime(2016, 1, 1, 11, 47, 52)))
db.session.add(
    Post(uid=176, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=252, c2_number=30, league="Standard",
         name="Zesty Dragon", time=datetime.datetime(2016, 12, 16, 4, 6, 36)))
db.session.add(
    Post(uid=177, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=252, c2_number=309, league="Standard",
         name="Zod", time=datetime.datetime(2016, 1, 18, 17, 47, 2)))
db.session.add(
    Post(uid=0, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=173, c2_number=118, league="Standard",
         name="101", time=datetime.datetime(2016, 3, 22, 9, 42, 44)))
db.session.add(
    Post(uid=1, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=173, c2_number=256, league="Standard",
         name="Houston", time=datetime.datetime(2016, 9, 24, 11, 49, 30)))
db.session.add(
    Post(uid=2, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=306, c2_number=156, league="Standard",
         name="Pinball Wizard", time=datetime.datetime(2016, 5, 9, 5, 23, 48)))
db.session.add(Post(uid=3, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=40, c2_number=86, league="Standard",
                    name="Accidental Genius", time=datetime.datetime(2016, 1, 11, 1, 22, 43)))
db.session.add(
    Post(uid=4, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=89, c2_number=100, league="Standard",
         name="Hyper", time=datetime.datetime(2016, 1, 21, 19, 3, 46)))
db.session.add(
    Post(uid=5, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=176, c2_number=159, league="Standard",
         name="Pluto", time=datetime.datetime(2016, 2, 16, 15, 24, 53)))
db.session.add(
    Post(uid=6, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=175, c2_number=51, league="Standard",
         name="Alpha", time=datetime.datetime(2016, 8, 7, 7, 44, 55)))
db.session.add(Post(uid=7, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=127, c2_number=193,
                    league="Standard", name="Jester", time=datetime.datetime(2016, 10, 8, 5, 3, 9)))
db.session.add(
    Post(uid=8, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=145, c2_number=164, league="Standard",
         name="Pogue", time=datetime.datetime(2016, 5, 25, 18, 2, 51)))
db.session.add(
    Post(uid=9, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=299, c2_number=141, league="Standard",
         name="Airport Hobo", time=datetime.datetime(2016, 10, 19, 19, 15, 32)))
db.session.add(
    Post(uid=10, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=263, c2_number=294, league="Standard",
         name="Jigsaw", time=datetime.datetime(2016, 2, 25, 3, 48, 42)))
db.session.add(
    Post(uid=11, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=227, c2_number=121, league="Standard",
         name="Prometheus", time=datetime.datetime(2016, 5, 20, 19, 0, 41)))
db.session.add(
    Post(uid=12, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=291, c2_number=259, league="Standard",
         name="Bearded Angler", time=datetime.datetime(2016, 5, 23, 16, 57, 41)))
db.session.add(
    Post(uid=13, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=93, c2_number=226, league="Standard",
         name="Joker's Grin", time=datetime.datetime(2016, 6, 22, 16, 10, 48)))
db.session.add(
    Post(uid=14, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=258, c2_number=88, league="Standard",
         name="Psycho Thinker", time=datetime.datetime(2016, 6, 21, 12, 43, 7)))
db.session.add(
    Post(uid=15, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=294, c2_number=309, league="Standard",
         name="Beetle King", time=datetime.datetime(2016, 5, 7, 21, 20, 16)))
db.session.add(
    Post(uid=16, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=293, c2_number=44, league="Standard",
         name="Judge", time=datetime.datetime(2016, 4, 3, 11, 37, 27)))
db.session.add(
    Post(uid=17, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=46, c2_number=231, league="Standard",
         name="Pusher", time=datetime.datetime(2016, 9, 27, 5, 22, 52)))
db.session.add(
    Post(uid=18, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=305, c2_number=46, league="Standard",
         name="Bitmap", time=datetime.datetime(2016, 11, 28, 4, 20, 33)))
db.session.add(
    Post(uid=19, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=43, c2_number=176, league="Standard",
         name="Junkyard Dog", time=datetime.datetime(2016, 12, 20, 9, 52, 5)))
db.session.add(
    Post(uid=20, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=291, c2_number=136, league="Standard",
         name="Riff Raff", time=datetime.datetime(2016, 10, 10, 16, 39, 27)))
db.session.add(
    Post(uid=21, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=288, c2_number=287, league="Standard",
         name="Blister", time=datetime.datetime(2016, 12, 26, 3, 37, 40)))
db.session.add(
    Post(uid=22, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=252, c2_number=25, league="Standard",
         name="K-9", time=datetime.datetime(2016, 5, 21, 16, 20, 47)))
db.session.add(
    Post(uid=23, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=49, c2_number=307, league="Standard",
         name="Roadblock", time=datetime.datetime(2016, 6, 5, 20, 50, 6)))
db.session.add(
    Post(uid=24, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=99, c2_number=191, league="Standard",
         name="Bowie", time=datetime.datetime(2016, 1, 10, 3, 19, 41)))
db.session.add(Post(uid=25, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=54, c2_number=64,
                    league="Standard", name="Keystone", time=datetime.datetime(2016, 2, 3, 6, 29, 33)))
db.session.add(
    Post(uid=26, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=149, c2_number=206, league="Standard",
         name="Rooster", time=datetime.datetime(2016, 3, 22, 15, 3, 2)))
db.session.add(
    Post(uid=27, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=288, c2_number=284, league="Standard",
         name="Bowler", time=datetime.datetime(2016, 7, 6, 22, 34, 46)))
db.session.add(
    Post(uid=28, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=141, c2_number=272, league="Standard",
         name="Kickstart", time=datetime.datetime(2016, 2, 5, 10, 16, 26)))
db.session.add(
    Post(uid=29, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=64, c2_number=22, league="Standard",
         name="Sandbox", time=datetime.datetime(2016, 4, 1, 4, 37, 9)))
db.session.add(
    Post(uid=30, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=136, c2_number=152, league="Standard",
         name="Breadmaker", time=datetime.datetime(2016, 11, 14, 1, 26, 28)))
db.session.add(
    Post(uid=31, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=172, c2_number=251, league="Standard",
         name="Kill Switch", time=datetime.datetime(2016, 11, 19, 11, 19, 23)))
db.session.add(
    Post(uid=32, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=153, c2_number=195, league="Standard",
         name="Scrapper", time=datetime.datetime(2016, 4, 19, 15, 45, 43)))
db.session.add(
    Post(uid=33, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=100, c2_number=34, league="Standard",
         name="Broomspun", time=datetime.datetime(2016, 7, 8, 2, 28, 45)))
db.session.add(
    Post(uid=34, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=212, c2_number=115, league="Standard",
         name="Kingfisher", time=datetime.datetime(2016, 5, 20, 0, 26, 32)))
db.session.add(
    Post(uid=35, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=258, c2_number=178, league="Standard",
         name="Screwtape", time=datetime.datetime(2016, 9, 27, 19, 10, 11)))
db.session.add(
    Post(uid=36, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=38, c2_number=197, league="Standard",
         name="Buckshot", time=datetime.datetime(2016, 2, 6, 1, 33, 50)))
db.session.add(
    Post(uid=37, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=117, c2_number=227, league="Standard",
         name="Kitchen", time=datetime.datetime(2016, 7, 2, 18, 9, 41)))
db.session.add(
    Post(uid=38, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=261, c2_number=146, league="Standard",
         name="Sexual Chocolate", time=datetime.datetime(2016, 1, 16, 7, 25, 21)))
db.session.add(
    Post(uid=39, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=211, c2_number=264, league="Standard",
         name="Bugger", time=datetime.datetime(2016, 7, 6, 15, 44, 3)))
db.session.add(
    Post(uid=40, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=26, c2_number=159, league="Standard",
         name="Knuckles", time=datetime.datetime(2016, 3, 25, 2, 30, 38)))
db.session.add(
    Post(uid=41, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=57, c2_number=156, league="Standard",
         name="Shadow Chaser", time=datetime.datetime(2016, 10, 13, 6, 38, 11)))
db.session.add(
    Post(uid=42, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=184, c2_number=291, league="Standard",
         name="Cabbie", time=datetime.datetime(2016, 11, 17, 6, 26, 31)))
db.session.add(Post(uid=43, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=197, c2_number=58,
                    league="Standard", name="Lady Killer", time=datetime.datetime(2016, 2, 7, 14, 55, 26)))
db.session.add(
    Post(uid=44, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=290, c2_number=248, league="Standard",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 11, 27, 14, 48, 7)))
db.session.add(
    Post(uid=45, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=258, c2_number=263, league="Standard",
         name="Candy Butcher", time=datetime.datetime(2016, 2, 26, 20, 10, 27)))
db.session.add(
    Post(uid=46, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=25, c2_number=35, league="Standard",
         name="Liquid Science", time=datetime.datetime(2016, 10, 19, 13, 52, 53)))
db.session.add(
    Post(uid=47, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=35, c2_number=174, league="Standard",
         name="Shooter", time=datetime.datetime(2016, 3, 2, 19, 47, 26)))
db.session.add(
    Post(uid=48, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=264, c2_number=40, league="Standard",
         name="Capital F", time=datetime.datetime(2016, 3, 9, 21, 47, 19)))
db.session.add(
    Post(uid=49, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=174, c2_number=43, league="Standard",
         name="Little Cobra", time=datetime.datetime(2016, 2, 1, 7, 15, 37)))
db.session.add(
    Post(uid=50, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=159, c2_number=153, league="Standard",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 6, 1, 14, 43, 57)))
db.session.add(
    Post(uid=51, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=78, c2_number=247, league="Standard",
         name="Captain Peroxide", time=datetime.datetime(2016, 3, 21, 13, 53, 11)))
db.session.add(
    Post(uid=52, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=128, c2_number=273, league="Standard",
         name="Little General", time=datetime.datetime(2016, 10, 14, 13, 26, 34)))
db.session.add(
    Post(uid=53, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=124, c2_number=138, league="Standard",
         name="Skull Crusher", time=datetime.datetime(2016, 5, 6, 13, 16, 56)))
db.session.add(
    Post(uid=54, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=299, c2_number=188, league="Standard",
         name="Celtic Charger", time=datetime.datetime(2016, 4, 7, 3, 57, 41)))
db.session.add(
    Post(uid=55, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=272, c2_number=103, league="Standard",
         name="Lord Nikon", time=datetime.datetime(2016, 4, 26, 11, 17, 33)))
db.session.add(
    Post(uid=56, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=253, c2_number=179, league="Standard",
         name="Sky Bully", time=datetime.datetime(2016, 10, 23, 10, 51, 13)))
db.session.add(
    Post(uid=57, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=266, c2_number=179, league="Standard",
         name="Cereal Killer", time=datetime.datetime(2016, 11, 9, 6, 30, 7)))
db.session.add(
    Post(uid=58, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=283, c2_number=252, league="Standard",
         name="Lord Pistachio", time=datetime.datetime(2016, 1, 14, 9, 21, 52)))
db.session.add(
    Post(uid=59, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=163, c2_number=117, league="Standard",
         name="Slow Trot", time=datetime.datetime(2016, 4, 21, 18, 44, 43)))
db.session.add(Post(uid=60, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=69, c2_number=283, league="Standard",
                    name="Chicago Blackout", time=datetime.datetime(2016, 12, 6, 21, 4, 0)))
db.session.add(
    Post(uid=61, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=130, c2_number=100, league="Standard",
         name="Mad Irishman", time=datetime.datetime(2016, 2, 4, 20, 14, 1)))
db.session.add(Post(uid=62, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=210, c2_number=203, league="Standard",
                    name="Snake Eyes", time=datetime.datetime(2016, 12, 25, 20, 4, 45)))
db.session.add(
    Post(uid=63, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=244, c2_number=313, league="Standard",
         name="Chocolate Thunder", time=datetime.datetime(2016, 1, 14, 15, 26, 19)))
db.session.add(Post(uid=64, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=255, c2_number=68, league="Standard",
                    name="Mad Jack", time=datetime.datetime(2016, 12, 23, 18, 42, 47)))
db.session.add(Post(uid=65, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=160, c2_number=109, league="Standard",
                    name="Snow Hound", time=datetime.datetime(2016, 1, 16, 1, 46, 20)))
db.session.add(
    Post(uid=66, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=59, c2_number=188, league="Standard",
         name="Chuckles", time=datetime.datetime(2016, 3, 26, 9, 27, 14)))
db.session.add(
    Post(uid=67, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=160, c2_number=38, league="Standard",
         name="Mad Rascal", time=datetime.datetime(2016, 7, 11, 11, 9, 1)))
db.session.add(
    Post(uid=68, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=257, c2_number=118, league="Standard",
         name="Sofa King", time=datetime.datetime(2016, 7, 26, 22, 53, 23)))
db.session.add(
    Post(uid=69, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=234, c2_number=25, league="Standard",
         name="Commando", time=datetime.datetime(2016, 3, 23, 19, 19, 13)))
db.session.add(
    Post(uid=70, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=236, c2_number=199, league="Standard",
         name="Manimal", time=datetime.datetime(2016, 5, 12, 5, 7, 25)))
db.session.add(
    Post(uid=71, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=136, c2_number=220, league="Standard",
         name="Speedwell", time=datetime.datetime(2016, 5, 28, 9, 54, 16)))
db.session.add(
    Post(uid=72, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=119, c2_number=224, league="Standard",
         name="Cool Whip", time=datetime.datetime(2016, 7, 25, 7, 19, 19)))
db.session.add(
    Post(uid=73, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=259, c2_number=68, league="Standard",
         name="Marbles", time=datetime.datetime(2016, 1, 20, 5, 10, 13)))
db.session.add(Post(uid=74, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=301, c2_number=284, league="Standard",
                    name="Spider Fuji", time=datetime.datetime(2016, 12, 26, 8, 28, 7)))
db.session.add(
    Post(uid=75, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=200, c2_number=287, league="Standard", name="Cosmo",
         time=datetime.datetime(2016, 6, 7, 17, 16, 44)))
db.session.add(
    Post(uid=76, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=230, c2_number=57, league="Standard",
         name="Married Man", time=datetime.datetime(2016, 3, 17, 4, 3, 24)))
db.session.add(Post(uid=77, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=212, c2_number=64, league="Standard",
                    name="Springheel Jack", time=datetime.datetime(2016, 11, 8, 0, 38, 11)))
db.session.add(Post(uid=78, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=272, c2_number=25, league="Standard",
                    name="Crash Override", time=datetime.datetime(2016, 1, 20, 5, 35, 13)))
db.session.add(
    Post(uid=79, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=169, c2_number=130, league="Standard",
         name="Marshmallow", time=datetime.datetime(2016, 4, 1, 15, 12, 18)))
db.session.add(Post(uid=80, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=124, c2_number=156, league="Standard",
                    name="Squatch", time=datetime.datetime(2016, 4, 26, 5, 5, 1)))
db.session.add(Post(uid=81, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=212, c2_number=39, league="Standard",
                    name="Crash Test", time=datetime.datetime(2016, 1, 1, 4, 42, 52)))
db.session.add(Post(uid=82, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=36, c2_number=142, league="Standard",
                    name="Mental", time=datetime.datetime(2016, 8, 24, 4, 11, 15)))
db.session.add(Post(uid=83, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=305, c2_number=230, league="Standard",
                    name="Stacker of Wheat", time=datetime.datetime(2016, 2, 25, 15, 31, 29)))
db.session.add(
    Post(uid=84, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=199, c2_number=172, league="Standard",
         name="Crazy Eights", time=datetime.datetime(2016, 9, 7, 4, 5, 0)))
db.session.add(
    Post(uid=85, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=76, c2_number=154, league="Standard",
         name="Mercury Reborn", time=datetime.datetime(2016, 8, 15, 22, 41, 43)))
db.session.add(
    Post(uid=86, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=281, c2_number=47, league="Standard",
         name="Sugar Man", time=datetime.datetime(2016, 2, 26, 9, 17, 29)))
db.session.add(
    Post(uid=87, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=76, c2_number=57, league="Standard",
         name="Criss Cross", time=datetime.datetime(2016, 3, 3, 9, 26, 25)))
db.session.add(
    Post(uid=88, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=191, c2_number=152, league="Standard",
         name="Midas", time=datetime.datetime(2016, 7, 2, 12, 48, 51)))
db.session.add(Post(uid=89, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=86, c2_number=205, league="Standard",
                    name="Suicide Jockey", time=datetime.datetime(2016, 11, 28, 13, 57, 28)))
db.session.add(
    Post(uid=90, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=208, c2_number=202, league="Standard",
         name="Cross Thread", time=datetime.datetime(2016, 6, 16, 14, 38, 24)))
db.session.add(
    Post(uid=91, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=203, c2_number=254, league="Standard",
         name="Midnight Rambler", time=datetime.datetime(2016, 9, 18, 17, 32, 41)))
db.session.add(Post(uid=92, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=121, c2_number=206, league="Standard",
                    name="Swampmasher", time=datetime.datetime(2016, 5, 20, 1, 50, 10)))
db.session.add(
    Post(uid=93, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=267, c2_number=314, league="Standard", name="Cujo",
         time=datetime.datetime(2016, 3, 16, 0, 27, 3)))
db.session.add(Post(uid=94, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=129, c2_number=72, league="Standard",
                    name="Midnight Rider", time=datetime.datetime(2016, 6, 10, 14, 16, 53)))
db.session.add(Post(uid=95, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=187, c2_number=229, league="Standard",
                    name="Swerve", time=datetime.datetime(2016, 1, 11, 6, 47, 25)))
db.session.add(
    Post(uid=96, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=87, c2_number=318, league="Standard",
         name="Dancing Madman", time=datetime.datetime(2016, 1, 6, 16, 26, 43)))
db.session.add(Post(uid=97, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=106, c2_number=230,
                    league="Standard", name="Mindless Bobcat", time=datetime.datetime(2016, 7, 2, 17, 32, 23)))
db.session.add(
    Post(uid=98, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=308, c2_number=187, league="Standard",
         name="Tacklebox", time=datetime.datetime(2016, 11, 23, 9, 23, 42)))
db.session.add(
    Post(uid=99, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=218, c2_number=301, league="Standard",
         name="Dangle", time=datetime.datetime(2016, 10, 4, 10, 43, 0)))
db.session.add(
    Post(uid=100, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=131, c2_number=38, league="Standard",
         name="Mr. 44", time=datetime.datetime(2016, 7, 25, 15, 16, 3)))
db.session.add(
    Post(uid=101, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=121, c2_number=97, league="Standard",
         name="Take Away", time=datetime.datetime(2016, 7, 11, 16, 13, 47)))
db.session.add(
    Post(uid=102, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=73, c2_number=231, league="Standard",
         name="Dark Horse", time=datetime.datetime(2016, 3, 24, 9, 29, 36)))
db.session.add(
    Post(uid=103, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=80, c2_number=196, league="Standard",
         name="Mr. Fabulous", time=datetime.datetime(2016, 11, 18, 14, 14, 1)))
db.session.add(
    Post(uid=104, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=297, c2_number=245, league="Standard",
         name="Tan Stallion", time=datetime.datetime(2016, 8, 10, 13, 34, 11)))
db.session.add(
    Post(uid=105, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=187, c2_number=286, league="Standard",
         name="Day Hawk", time=datetime.datetime(2016, 1, 8, 19, 57, 58)))
db.session.add(
    Post(uid=106, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=254, c2_number=96, league="Standard",
         name="Mr. Gadget", time=datetime.datetime(2016, 10, 26, 2, 4, 37)))
db.session.add(
    Post(uid=107, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=144, c2_number=57, league="Standard",
         name="The China Wall", time=datetime.datetime(2016, 4, 13, 14, 15, 10)))
db.session.add(
    Post(uid=108, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=230, c2_number=256, league="Standard",
         name="Desert Haze", time=datetime.datetime(2016, 12, 14, 20, 0, 42)))
db.session.add(
    Post(uid=109, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=77, c2_number=137, league="Standard",
         name="Mr. Lucky", time=datetime.datetime(2016, 12, 6, 7, 2, 10)))
db.session.add(
    Post(uid=110, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=145, c2_number=212, league="Standard",
         name="The Dude", time=datetime.datetime(2016, 12, 10, 14, 8, 9)))
db.session.add(
    Post(uid=111, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=145, c2_number=91, league="Standard",
         name="Digger", time=datetime.datetime(2016, 3, 24, 10, 10, 9)))
db.session.add(
    Post(uid=112, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=49, c2_number=89, league="Standard",
         name="Mr. Peppermint", time=datetime.datetime(2016, 7, 9, 9, 15, 40)))
db.session.add(
    Post(uid=113, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=283, c2_number=221, league="Standard",
         name="The Flying Mouse", time=datetime.datetime(2016, 7, 2, 2, 2, 52)))
db.session.add(
    Post(uid=114, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=92, c2_number=175, league="Standard",
         name="Disco Thunder", time=datetime.datetime(2016, 7, 24, 5, 0, 40)))
db.session.add(Post(uid=115, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=282, c2_number=184,
                    league="Standard", name="Mr. Spy", time=datetime.datetime(2016, 11, 10, 2, 14, 31)))
db.session.add(Post(uid=116, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=265, c2_number=46, league="Standard",
                    name="The Happy Jock", time=datetime.datetime(2016, 12, 22, 10, 47, 16)))
db.session.add(
    Post(uid=117, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=281, c2_number=148, league="Standard",
         name="Disco Potato", time=datetime.datetime(2016, 12, 11, 11, 45, 20)))
db.session.add(
    Post(uid=118, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=60, c2_number=229, league="Standard",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 7, 28, 16, 38, 8)))
db.session.add(
    Post(uid=119, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=84, c2_number=207, league="Standard",
         name="The Howling Swede", time=datetime.datetime(2016, 4, 5, 20, 10, 58)))
db.session.add(
    Post(uid=120, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=109, c2_number=296, league="Standard",
         name="Dr. Cocktail", time=datetime.datetime(2016, 12, 13, 16, 39, 36)))
db.session.add(
    Post(uid=121, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=225, c2_number=216, league="Standard",
         name="Mr. Wholesome", time=datetime.datetime(2016, 10, 18, 20, 16, 23)))
db.session.add(
    Post(uid=122, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=78, c2_number=289, league="Standard",
         name="Thrasher", time=datetime.datetime(2016, 4, 1, 19, 13, 3)))
db.session.add(
    Post(uid=123, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=194, c2_number=186, league="Standard",
         name="Dredd", time=datetime.datetime(2016, 1, 18, 18, 14, 45)))
db.session.add(
    Post(uid=124, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=52, c2_number=183, league="Standard",
         name="Mud Pie Man", time=datetime.datetime(2016, 5, 16, 20, 3, 17)))
db.session.add(
    Post(uid=125, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=306, c2_number=39, league="Standard",
         name="Toe", time=datetime.datetime(2016, 8, 28, 7, 50, 38)))
db.session.add(
    Post(uid=126, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=135, c2_number=264, league="Standard",
         name="Dropkick", time=datetime.datetime(2016, 3, 4, 22, 54, 18)))
db.session.add(
    Post(uid=127, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=124, c2_number=198, league="Standard",
         name="Mule Skinner", time=datetime.datetime(2016, 10, 26, 10, 56, 7)))
db.session.add(Post(uid=128, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=74, c2_number=288, league="Standard",
                    name="Toolmaker", time=datetime.datetime(2016, 2, 15, 13, 49, 32)))
db.session.add(Post(uid=129, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=227, c2_number=99, league="Standard",
                    name="Drop Stone", time=datetime.datetime(2016, 9, 21, 22, 21, 28)))
db.session.add(
    Post(uid=130, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=181, c2_number=74, league="Standard",
         name="Murmur", time=datetime.datetime(2016, 12, 9, 0, 31, 13)))
db.session.add(
    Post(uid=131, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=104, c2_number=274, league="Standard",
         name="Tough Nut", time=datetime.datetime(2016, 11, 25, 17, 38, 28)))
db.session.add(
    Post(uid=132, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=213, c2_number=67, league="Hardcore",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 10, 9, 15, 4, 33)))
db.session.add(Post(uid=133, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=294, c2_number=159,
                    league="Hardcore", name="Nacho", time=datetime.datetime(2016, 9, 24, 13, 17, 30)))
db.session.add(
    Post(uid=134, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=198, c2_number=216, league="Hardcore",
         name="Trip", time=datetime.datetime(2016, 11, 2, 17, 11, 38)))
db.session.add(
    Post(uid=135, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=35, c2_number=204, league="Hardcore",
         name="Easy Sweep", time=datetime.datetime(2016, 1, 18, 13, 11, 6)))
db.session.add(
    Post(uid=136, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=49, c2_number=113, league="Hardcore",
         name="Natural Mess", time=datetime.datetime(2016, 11, 25, 17, 13, 44)))
db.session.add(
    Post(uid=137, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=279, c2_number=193, league="Hardcore",
         name="Troubadour", time=datetime.datetime(2016, 4, 18, 3, 44, 37)))
db.session.add(
    Post(uid=138, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=207, c2_number=125, league="Hardcore",
         name="Electric Player", time=datetime.datetime(2016, 5, 27, 0, 58, 37)))
db.session.add(
    Post(uid=139, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=50, c2_number=249, league="Hardcore",
         name="Necromancer", time=datetime.datetime(2016, 6, 27, 13, 24, 54)))
db.session.add(
    Post(uid=140, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=134, c2_number=44, league="Hardcore",
         name="Turnip King", time=datetime.datetime(2016, 8, 18, 16, 42, 43)))
db.session.add(
    Post(uid=141, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=283, c2_number=294, league="Hardcore",
         name="Esquire", time=datetime.datetime(2016, 12, 14, 15, 40, 7)))
db.session.add(
    Post(uid=142, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=127, c2_number=46, league="Hardcore",
         name="Neophyte Believer", time=datetime.datetime(2016, 6, 6, 2, 39, 26)))
db.session.add(
    Post(uid=143, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=66, c2_number=277, league="Hardcore",
         name="Twitch", time=datetime.datetime(2016, 10, 23, 21, 55, 2)))
db.session.add(
    Post(uid=144, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=176, c2_number=115, league="Hardcore",
         name="Fast Draw", time=datetime.datetime(2016, 3, 14, 4, 57, 29)))
db.session.add(
    Post(uid=145, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=44, c2_number=123, league="Hardcore",
         name="Nessie", time=datetime.datetime(2016, 10, 3, 15, 22, 19)))
db.session.add(Post(uid=146, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=32, c2_number=74, league="Hardcore",
                    name="Vagabond Warrior", time=datetime.datetime(2016, 8, 26, 12, 12, 23)))
db.session.add(Post(uid=147, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=76, c2_number=224, league="Hardcore",
                    name="Flakes", time=datetime.datetime(2016, 1, 7, 15, 6, 35)))
db.session.add(
    Post(uid=148, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=66, c2_number=217, league="Hardcore",
         name="New Cycle", time=datetime.datetime(2016, 2, 9, 15, 50, 20)))
db.session.add(
    Post(uid=149, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=276, c2_number=157, league="Hardcore",
         name="Voluntary", time=datetime.datetime(2016, 8, 13, 3, 56, 0)))
db.session.add(Post(uid=150, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=38, c2_number=306,
                    league="Hardcore", name="Flint", time=datetime.datetime(2016, 9, 1, 9, 38, 45)))
db.session.add(
    Post(uid=151, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=242, c2_number=245,
         league="Hardcore", name="Nickname Master", time=datetime.datetime(2016, 2, 20, 16, 40, 1)))
db.session.add(
    Post(uid=152, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=244, c2_number=75, league="Hardcore",
         name="Vortex", time=datetime.datetime(2016, 4, 14, 21, 12, 5)))
db.session.add(Post(uid=153, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=56, c2_number=125,
                    league="Hardcore", name="Freak", time=datetime.datetime(2016, 12, 20, 9, 44, 1)))
db.session.add(Post(uid=154, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=100, c2_number=247,
                    league="Hardcore", name="Nightmare King", time=datetime.datetime(2016, 5, 11, 8, 32, 32)))
db.session.add(Post(uid=155, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=301, c2_number=259,
                    league="Hardcore", name="Washer", time=datetime.datetime(2016, 10, 22, 5, 31, 54)))
db.session.add(Post(uid=156, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=34, c2_number=220,
                    league="Hardcore", name="Gas Man", time=datetime.datetime(2016, 6, 28, 3, 20, 19)))
db.session.add(Post(uid=157, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=71, c2_number=282,
                    league="Hardcore", name="Night Train", time=datetime.datetime(2016, 1, 19, 17, 31, 19)))
db.session.add(Post(uid=158, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=29, c2_number=180,
                    league="Hardcore", name="Waylay Dave", time=datetime.datetime(2016, 5, 7, 3, 3, 17)))
db.session.add(Post(uid=159, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=203, c2_number=134,
                    league="Hardcore", name="Glyph", time=datetime.datetime(2016, 1, 1, 17, 20, 37)))
db.session.add(Post(uid=160, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=209, c2_number=234,
                    league="Hardcore", name="Old Man Winter", time=datetime.datetime(2016, 11, 7, 11, 32, 32)))
db.session.add(Post(uid=161, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=262, c2_number=201,
                    league="Hardcore", name="Wheels", time=datetime.datetime(2016, 3, 17, 7, 28, 51)))
db.session.add(Post(uid=162, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=20, c2_number=204,
                    league="Hardcore", name="Grave Digger", time=datetime.datetime(2016, 9, 9, 16, 31, 6)))
db.session.add(Post(uid=163, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=116, c2_number=276,
                    league="Hardcore", name="Old Orange Eyes", time=datetime.datetime(2016, 4, 8, 10, 12, 50)))
db.session.add(
    Post(uid=164, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=308, c2_number=313, league="Hardcore",
         name="Wooden Man", time=datetime.datetime(2016, 2, 8, 13, 42, 53)))
db.session.add(
    Post(uid=165, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=61, c2_number=172, league="Hardcore",
         name="Guillotine", time=datetime.datetime(2016, 4, 7, 1, 44, 33)))
db.session.add(Post(uid=166, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=34, c2_number=181,
                    league="Hardcore", name="Old Regret", time=datetime.datetime(2016, 8, 19, 8, 27, 56)))
db.session.add(Post(uid=167, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=49, c2_number=152,
                    league="Hardcore", name="Woo Woo", time=datetime.datetime(2016, 10, 18, 9, 34, 50)))
db.session.add(Post(uid=168, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=100, c2_number=96, league="Hardcore",
                    name="Gunhawk", time=datetime.datetime(2016, 3, 15, 15, 50, 11)))
db.session.add(
    Post(uid=169, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=161, c2_number=39, league="Hardcore",
         name="Onion King", time=datetime.datetime(2016, 8, 25, 11, 6, 31)))
db.session.add(Post(uid=170, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=76, c2_number=115, league="Hardcore",
                    name="Yellow Menace", time=datetime.datetime(2016, 1, 25, 22, 35, 18)))
db.session.add(
    Post(uid=171, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=295, c2_number=181, league="Hardcore",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 11, 17, 15, 20, 22)))
db.session.add(Post(uid=172, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=165, c2_number=36, league="Hardcore",
                    name="Osprey", time=datetime.datetime(2016, 8, 5, 4, 56, 24)))
db.session.add(Post(uid=173, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=56, c2_number=282, league="Hardcore",
                    name="Zero Charisma", time=datetime.datetime(2016, 1, 6, 0, 50, 31)))
db.session.add(
    Post(uid=174, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=147, c2_number=194, league="Hardcore",
         name="Highlander Monk", time=datetime.datetime(2016, 6, 3, 15, 48, 32)))
db.session.add(
    Post(uid=175, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=46, c2_number=203, league="Hardcore",
         name="Overrun", time=datetime.datetime(2016, 5, 19, 5, 24, 52)))
db.session.add(
    Post(uid=176, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=285, c2_number=278, league="Hardcore",
         name="Zesty Dragon", time=datetime.datetime(2016, 5, 14, 0, 44, 37)))
db.session.add(
    Post(uid=177, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=36, c2_number=283, league="Hardcore",
         name="Zod", time=datetime.datetime(2016, 2, 22, 3, 45, 55)))
db.session.add(
    Post(uid=0, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=315, c2_number=209, league="Hardcore",
         name="101", time=datetime.datetime(2016, 7, 17, 22, 51, 24)))
db.session.add(
    Post(uid=1, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=219, c2_number=198, league="Hardcore",
         name="Houston", time=datetime.datetime(2016, 4, 3, 21, 14, 21)))
db.session.add(
    Post(uid=2, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=139, c2_number=313, league="Hardcore",
         name="Pinball Wizard", time=datetime.datetime(2016, 9, 23, 11, 39, 51)))
db.session.add(
    Post(uid=3, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=204, c2_number=47, league="Hardcore",
         name="Accidental Genius", time=datetime.datetime(2016, 11, 28, 19, 7, 16)))
db.session.add(
    Post(uid=4, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=34, c2_number=133, league="Hardcore", name="Hyper",
         time=datetime.datetime(2016, 7, 28, 10, 51, 18)))
db.session.add(
    Post(uid=5, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=99, c2_number=169, league="Hardcore", name="Pluto",
         time=datetime.datetime(2016, 2, 23, 17, 6, 57)))
db.session.add(
    Post(uid=6, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=132, c2_number=145, league="Hardcore",
         name="Alpha", time=datetime.datetime(2016, 6, 8, 3, 28, 12)))
db.session.add(Post(uid=7, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=185, c2_number=118, league="Hardcore",
                    name="Jester", time=datetime.datetime(2016, 10, 13, 13, 8, 34)))
db.session.add(
    Post(uid=8, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=95, c2_number=211, league="Hardcore",
         name="Pogue", time=datetime.datetime(2016, 2, 19, 6, 16, 8)))
db.session.add(Post(uid=9, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=148, c2_number=308,
                    league="Hardcore", name="Airport Hobo", time=datetime.datetime(2016, 7, 22, 3, 27, 41)))
db.session.add(
    Post(uid=10, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=149, c2_number=299, league="Hardcore",
         name="Jigsaw", time=datetime.datetime(2016, 5, 4, 12, 37, 46)))
db.session.add(
    Post(uid=11, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=310, c2_number=159, league="Hardcore",
         name="Prometheus", time=datetime.datetime(2016, 3, 23, 21, 30, 18)))
db.session.add(
    Post(uid=12, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=315, c2_number=77, league="Hardcore",
         name="Bearded Angler", time=datetime.datetime(2016, 8, 14, 8, 40, 15)))
db.session.add(
    Post(uid=13, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=286, c2_number=191, league="Hardcore",
         name="Joker's Grin", time=datetime.datetime(2016, 6, 26, 22, 29, 9)))
db.session.add(
    Post(uid=14, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=78, c2_number=251, league="Hardcore",
         name="Psycho Thinker", time=datetime.datetime(2016, 2, 3, 13, 16, 23)))
db.session.add(
    Post(uid=15, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=184, c2_number=311, league="Hardcore",
         name="Beetle King", time=datetime.datetime(2016, 9, 8, 8, 41, 7)))
db.session.add(
    Post(uid=16, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=115, c2_number=147, league="Hardcore",
         name="Judge", time=datetime.datetime(2016, 11, 3, 2, 38, 43)))
db.session.add(
    Post(uid=17, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=286, c2_number=146, league="Hardcore",
         name="Pusher", time=datetime.datetime(2016, 3, 19, 7, 45, 15)))
db.session.add(
    Post(uid=18, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=35, c2_number=115, league="Hardcore",
         name="Bitmap", time=datetime.datetime(2016, 7, 23, 1, 54, 46)))
db.session.add(
    Post(uid=19, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=272, c2_number=273, league="Hardcore",
         name="Junkyard Dog", time=datetime.datetime(2016, 2, 17, 8, 15, 52)))
db.session.add(
    Post(uid=20, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=207, c2_number=90, league="Hardcore",
         name="Riff Raff", time=datetime.datetime(2016, 6, 25, 4, 55, 25)))
db.session.add(
    Post(uid=21, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=231, c2_number=239, league="Hardcore",
         name="Blister", time=datetime.datetime(2016, 10, 27, 18, 19, 23)))
db.session.add(
    Post(uid=22, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=205, c2_number=80, league="Hardcore",
         name="K-9", time=datetime.datetime(2016, 10, 4, 20, 4, 4)))
db.session.add(Post(uid=23, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=54, c2_number=225, league="Hardcore",
                    name="Roadblock", time=datetime.datetime(2016, 12, 24, 11, 3, 54)))
db.session.add(
    Post(uid=24, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=23, c2_number=86, league="Hardcore",
         name="Bowie", time=datetime.datetime(2016, 7, 11, 14, 18, 55)))
db.session.add(
    Post(uid=25, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=143, c2_number=188, league="Hardcore",
         name="Keystone", time=datetime.datetime(2016, 2, 7, 4, 47, 57)))
db.session.add(
    Post(uid=26, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=155, c2_number=308, league="Hardcore",
         name="Rooster", time=datetime.datetime(2016, 4, 13, 21, 25, 4)))
db.session.add(
    Post(uid=27, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=187, c2_number=198, league="Hardcore",
         name="Bowler", time=datetime.datetime(2016, 12, 14, 13, 7, 28)))
db.session.add(Post(uid=28, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=166, c2_number=36, league="Hardcore",
                    name="Kickstart", time=datetime.datetime(2016, 7, 16, 3, 38, 49)))
db.session.add(
    Post(uid=29, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=243, c2_number=140, league="Hardcore",
         name="Sandbox", time=datetime.datetime(2016, 10, 1, 10, 34, 44)))
db.session.add(Post(uid=30, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=168, c2_number=251, league="Hardcore",
                    name="Breadmaker", time=datetime.datetime(2016, 7, 25, 7, 16, 36)))
db.session.add(
    Post(uid=31, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=109, c2_number=184, league="Hardcore",
         name="Kill Switch", time=datetime.datetime(2016, 5, 1, 16, 6, 3)))
db.session.add(
    Post(uid=32, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=112, c2_number=47, league="Hardcore",
         name="Scrapper", time=datetime.datetime(2016, 6, 13, 0, 23, 31)))
db.session.add(
    Post(uid=33, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=262, c2_number=33, league="Hardcore",
         name="Broomspun", time=datetime.datetime(2016, 8, 4, 2, 26, 40)))
db.session.add(
    Post(uid=34, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=317, c2_number=39, league="Hardcore",
         name="Kingfisher", time=datetime.datetime(2016, 1, 8, 18, 2, 46)))
db.session.add(
    Post(uid=35, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=300, c2_number=87, league="Hardcore",
         name="Screwtape", time=datetime.datetime(2016, 4, 3, 3, 17, 53)))
db.session.add(
    Post(uid=36, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=35, c2_number=65, league="Hardcore",
         name="Buckshot", time=datetime.datetime(2016, 4, 21, 16, 43, 20)))
db.session.add(
    Post(uid=37, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=52, c2_number=122, league="Hardcore",
         name="Kitchen", time=datetime.datetime(2016, 3, 2, 22, 25, 18)))
db.session.add(
    Post(uid=38, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=39, c2_number=131, league="Hardcore",
         name="Sexual Chocolate", time=datetime.datetime(2016, 6, 5, 3, 12, 57)))
db.session.add(
    Post(uid=39, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=294, c2_number=269, league="Hardcore",
         name="Bugger", time=datetime.datetime(2016, 2, 12, 7, 12, 2)))
db.session.add(Post(uid=40, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=37, c2_number=191, league="Hardcore",
                    name="Knuckles", time=datetime.datetime(2016, 3, 28, 19, 55, 20)))
db.session.add(Post(uid=41, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=83, c2_number=180, league="Hardcore",
                    name="Shadow Chaser", time=datetime.datetime(2016, 11, 12, 13, 36, 4)))
db.session.add(
    Post(uid=42, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=254, c2_number=277, league="Hardcore",
         name="Cabbie", time=datetime.datetime(2016, 4, 14, 9, 32, 49)))
db.session.add(Post(uid=43, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=92, c2_number=42, league="Hardcore",
                    name="Lady Killer", time=datetime.datetime(2016, 1, 2, 15, 5, 15)))
db.session.add(
    Post(uid=44, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=122, c2_number=103, league="Hardcore",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 11, 7, 6, 39, 57)))
db.session.add(
    Post(uid=45, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=28, c2_number=172, league="Hardcore",
         name="Candy Butcher", time=datetime.datetime(2016, 10, 16, 0, 27, 16)))
db.session.add(Post(uid=46, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=162, c2_number=178, league="Hardcore",
                    name="Liquid Science", time=datetime.datetime(2016, 4, 18, 6, 6, 32)))
db.session.add(
    Post(uid=47, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=167, c2_number=176, league="Hardcore",
         name="Shooter", time=datetime.datetime(2016, 9, 26, 9, 38, 52)))
db.session.add(
    Post(uid=48, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=206, c2_number=278, league="Hardcore",
         name="Capital F", time=datetime.datetime(2016, 1, 21, 14, 22, 42)))
db.session.add(
    Post(uid=49, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=158, c2_number=230, league="Hardcore",
         name="Little Cobra", time=datetime.datetime(2016, 8, 8, 22, 27, 33)))
db.session.add(
    Post(uid=50, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=60, c2_number=59, league="Hardcore",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 6, 25, 16, 0, 21)))
db.session.add(
    Post(uid=51, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=136, c2_number=202, league="Hardcore",
         name="Captain Peroxide", time=datetime.datetime(2016, 6, 6, 3, 2, 56)))
db.session.add(
    Post(uid=52, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=47, c2_number=87, league="Hardcore",
         name="Little General", time=datetime.datetime(2016, 12, 5, 8, 39, 21)))
db.session.add(
    Post(uid=53, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=249, c2_number=228, league="Hardcore",
         name="Skull Crusher", time=datetime.datetime(2016, 5, 20, 20, 32, 11)))
db.session.add(
    Post(uid=54, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=319, c2_number=95, league="Hardcore",
         name="Celtic Charger", time=datetime.datetime(2016, 3, 6, 8, 49, 23)))
db.session.add(
    Post(uid=55, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=157, c2_number=47, league="Hardcore",
         name="Lord Nikon", time=datetime.datetime(2016, 10, 18, 7, 51, 42)))
db.session.add(
    Post(uid=56, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=133, c2_number=151, league="Hardcore",
         name="Sky Bully", time=datetime.datetime(2016, 1, 13, 13, 7, 40)))
db.session.add(
    Post(uid=57, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=234, c2_number=75, league="Hardcore",
         name="Cereal Killer", time=datetime.datetime(2016, 3, 19, 20, 4, 2)))
db.session.add(Post(uid=58, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=48, c2_number=36, league="Hardcore",
                    name="Lord Pistachio", time=datetime.datetime(2016, 10, 5, 4, 16, 33)))
db.session.add(Post(uid=59, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=171, c2_number=71, league="Hardcore",
                    name="Slow Trot", time=datetime.datetime(2016, 6, 3, 14, 56, 30)))
db.session.add(
    Post(uid=60, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=230, c2_number=40, league="Hardcore",
         name="Chicago Blackout", time=datetime.datetime(2016, 5, 12, 0, 39, 12)))
db.session.add(
    Post(uid=61, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=66, c2_number=262, league="Hardcore",
         name="Mad Irishman", time=datetime.datetime(2016, 8, 16, 3, 4, 24)))
db.session.add(
    Post(uid=62, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=63, c2_number=178, league="Hardcore",
         name="Snake Eyes", time=datetime.datetime(2016, 2, 14, 17, 53, 46)))
db.session.add(Post(uid=63, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=318, c2_number=173,
                    league="Hardcore", name="Chocolate Thunder", time=datetime.datetime(2016, 12, 28, 12, 36, 40)))
db.session.add(
    Post(uid=64, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=154, c2_number=87, league="Hardcore",
         name="Mad Jack", time=datetime.datetime(2016, 2, 24, 17, 13, 43)))
db.session.add(
    Post(uid=65, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=81, c2_number=161, league="Hardcore",
         name="Snow Hound", time=datetime.datetime(2016, 10, 10, 10, 0, 43)))
db.session.add(
    Post(uid=66, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=102, c2_number=29, league="Hardcore",
         name="Chuckles", time=datetime.datetime(2016, 8, 25, 18, 45, 10)))
db.session.add(
    Post(uid=67, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=148, c2_number=106, league="Hardcore",
         name="Mad Rascal", time=datetime.datetime(2016, 3, 27, 17, 53, 41)))
db.session.add(Post(uid=68, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=125, c2_number=48,
                    league="Hardcore", name="Sofa King", time=datetime.datetime(2016, 12, 22, 20, 47, 9)))
db.session.add(
    Post(uid=69, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=278, c2_number=298, league="Hardcore",
         name="Commando", time=datetime.datetime(2016, 12, 14, 8, 39, 8)))
db.session.add(
    Post(uid=70, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=69, c2_number=87, league="Hardcore",
         name="Manimal", time=datetime.datetime(2016, 11, 14, 9, 16, 35)))
db.session.add(Post(uid=71, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=61, c2_number=228,
                    league="Hardcore", name="Speedwell", time=datetime.datetime(2016, 6, 27, 1, 44, 5)))
db.session.add(
    Post(uid=72, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=60, c2_number=224, league="Hardcore",
         name="Cool Whip", time=datetime.datetime(2016, 5, 10, 16, 27, 44)))
db.session.add(
    Post(uid=73, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=112, c2_number=25, league="Hardcore",
         name="Marbles", time=datetime.datetime(2016, 5, 16, 14, 32, 38)))
db.session.add(
    Post(uid=74, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=223, c2_number=147, league="Hardcore",
         name="Spider Fuji", time=datetime.datetime(2016, 3, 1, 8, 56, 37)))
db.session.add(Post(uid=75, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=288, c2_number=282,
                    league="Hardcore", name="Cosmo", time=datetime.datetime(2016, 2, 14, 17, 33, 22)))
db.session.add(
    Post(uid=76, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=301, c2_number=304, league="Hardcore",
         name="Married Man", time=datetime.datetime(2016, 6, 27, 20, 1, 22)))
db.session.add(
    Post(uid=77, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=216, c2_number=196, league="Hardcore",
         name="Springheel Jack", time=datetime.datetime(2016, 6, 9, 3, 38, 38)))
db.session.add(
    Post(uid=78, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=210, c2_number=167, league="Hardcore",
         name="Crash Override", time=datetime.datetime(2016, 2, 7, 22, 4, 56)))
db.session.add(
    Post(uid=79, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=319, c2_number=268, league="Hardcore",
         name="Marshmallow", time=datetime.datetime(2016, 5, 13, 2, 16, 3)))
db.session.add(
    Post(uid=80, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=269, c2_number=147, league="Hardcore",
         name="Squatch", time=datetime.datetime(2016, 8, 1, 12, 6, 16)))
db.session.add(Post(uid=81, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=141, c2_number=44,
                    league="Hardcore", name="Crash Test", time=datetime.datetime(2016, 7, 23, 22, 17, 35)))
db.session.add(
    Post(uid=82, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=105, c2_number=156, league="Hardcore",
         name="Mental", time=datetime.datetime(2016, 11, 28, 12, 39, 6)))
db.session.add(
    Post(uid=83, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=123, c2_number=286, league="Hardcore",
         name="Stacker of Wheat", time=datetime.datetime(2016, 7, 22, 6, 5, 0)))
db.session.add(
    Post(uid=84, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=242, c2_number=235, league="Hardcore",
         name="Crazy Eights", time=datetime.datetime(2016, 11, 2, 11, 29, 37)))
db.session.add(
    Post(uid=85, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=90, c2_number=290, league="Hardcore",
         name="Mercury Reborn", time=datetime.datetime(2016, 8, 19, 17, 46, 43)))
db.session.add(
    Post(uid=86, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=39, c2_number=303, league="Hardcore",
         name="Sugar Man", time=datetime.datetime(2016, 8, 21, 18, 10, 40)))
db.session.add(
    Post(uid=87, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=98, c2_number=123, league="Hardcore",
         name="Criss Cross", time=datetime.datetime(2016, 5, 7, 20, 6, 45)))
db.session.add(
    Post(uid=88, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=161, c2_number=101, league="Hardcore",
         name="Midas", time=datetime.datetime(2016, 3, 14, 3, 26, 33)))
db.session.add(
    Post(uid=89, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=66, c2_number=52, league="Hardcore",
         name="Suicide Jockey", time=datetime.datetime(2016, 7, 9, 6, 25, 17)))
db.session.add(
    Post(uid=90, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=176, c2_number=193, league="Hardcore",
         name="Cross Thread", time=datetime.datetime(2016, 6, 22, 15, 46, 49)))
db.session.add(
    Post(uid=91, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=220, c2_number=120, league="Hardcore",
         name="Midnight Rambler", time=datetime.datetime(2016, 9, 11, 10, 28, 46)))
db.session.add(
    Post(uid=92, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=309, c2_number=304, league="Hardcore",
         name="Swampmasher", time=datetime.datetime(2016, 6, 17, 3, 17, 47)))
db.session.add(
    Post(uid=93, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=159, c2_number=151, league="Hardcore",
         name="Cujo", time=datetime.datetime(2016, 1, 5, 6, 1, 11)))
db.session.add(
    Post(uid=94, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=267, c2_number=87, league="Hardcore",
         name="Midnight Rider", time=datetime.datetime(2016, 4, 13, 0, 23, 7)))
db.session.add(
    Post(uid=95, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=103, c2_number=160, league="Hardcore",
         name="Swerve", time=datetime.datetime(2016, 7, 17, 7, 25, 38)))
db.session.add(
    Post(uid=96, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=249, c2_number=266, league="Hardcore",
         name="Dancing Madman", time=datetime.datetime(2016, 7, 20, 2, 46, 40)))
db.session.add(
    Post(uid=97, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=75, c2_number=216, league="Hardcore",
         name="Mindless Bobcat", time=datetime.datetime(2016, 11, 4, 6, 52, 19)))
db.session.add(
    Post(uid=98, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=309, c2_number=64, league="Hardcore",
         name="Tacklebox", time=datetime.datetime(2016, 4, 16, 14, 24, 16)))
db.session.add(Post(uid=99, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=120, c2_number=221,
                    league="Hardcore", name="Dangle", time=datetime.datetime(2016, 12, 10, 17, 8, 48)))
db.session.add(
    Post(uid=100, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=182, c2_number=283, league="Hardcore",
         name="Mr. 44", time=datetime.datetime(2016, 2, 6, 4, 2, 5)))
db.session.add(
    Post(uid=101, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=33, c2_number=24, league="Hardcore",
         name="Take Away", time=datetime.datetime(2016, 3, 25, 14, 16, 5)))
db.session.add(
    Post(uid=102, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=245, c2_number=230, league="Hardcore",
         name="Dark Horse", time=datetime.datetime(2016, 10, 20, 13, 37, 52)))
db.session.add(
    Post(uid=103, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=149, c2_number=185, league="Hardcore",
         name="Mr. Fabulous", time=datetime.datetime(2016, 4, 27, 10, 39, 32)))
db.session.add(Post(uid=104, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=247, c2_number=296,
                    league="Hardcore", name="Tan Stallion", time=datetime.datetime(2016, 9, 14, 0, 18, 4)))
db.session.add(
    Post(uid=105, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=110, c2_number=63, league="Hardcore",
         name="Day Hawk", time=datetime.datetime(2016, 11, 4, 19, 30, 3)))
db.session.add(
    Post(uid=106, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=263, c2_number=82, league="Hardcore",
         name="Mr. Gadget", time=datetime.datetime(2016, 11, 28, 8, 47, 5)))
db.session.add(Post(uid=107, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=226, c2_number=303,
                    league="Hardcore", name="The China Wall", time=datetime.datetime(2016, 4, 18, 22, 11, 37)))
db.session.add(
    Post(uid=108, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=291, c2_number=113, league="Hardcore",
         name="Desert Haze", time=datetime.datetime(2016, 7, 12, 8, 27, 19)))
db.session.add(
    Post(uid=109, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=289, c2_number=259, league="Hardcore",
         name="Mr. Lucky", time=datetime.datetime(2016, 2, 17, 10, 40, 58)))
db.session.add(
    Post(uid=110, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=89, c2_number=143, league="Hardcore",
         name="The Dude", time=datetime.datetime(2016, 8, 6, 16, 10, 54)))
db.session.add(
    Post(uid=111, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=197, c2_number=224, league="Hardcore",
         name="Digger", time=datetime.datetime(2016, 5, 20, 19, 35, 58)))
db.session.add(
    Post(uid=112, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=167, c2_number=221, league="Hardcore",
         name="Mr. Peppermint", time=datetime.datetime(2016, 5, 13, 10, 16, 58)))
db.session.add(
    Post(uid=113, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=241, c2_number=309, league="Hardcore",
         name="The Flying Mouse", time=datetime.datetime(2016, 1, 24, 8, 20, 32)))
db.session.add(
    Post(uid=114, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=36, c2_number=208, league="Hardcore",
         name="Disco Thunder", time=datetime.datetime(2016, 8, 22, 10, 50, 6)))
db.session.add(
    Post(uid=115, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=130, c2_number=106, league="Hardcore",
         name="Mr. Spy", time=datetime.datetime(2016, 9, 9, 1, 41, 14)))
db.session.add(
    Post(uid=116, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=184, c2_number=308, league="Hardcore",
         name="The Happy Jock", time=datetime.datetime(2016, 4, 7, 1, 32, 11)))
db.session.add(Post(uid=117, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=296, c2_number=125,
                    league="Hardcore", name="Disco Potato", time=datetime.datetime(2016, 11, 2, 17, 33, 31)))
db.session.add(
    Post(uid=118, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=227, c2_number=174, league="Hardcore",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 3, 13, 17, 13, 37)))
db.session.add(
    Post(uid=119, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=269, c2_number=98, league="Hardcore",
         name="The Howling Swede", time=datetime.datetime(2016, 8, 17, 16, 54, 10)))
db.session.add(
    Post(uid=120, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=260, c2_number=268, league="Hardcore",
         name="Dr. Cocktail", time=datetime.datetime(2016, 4, 6, 4, 16, 39)))
db.session.add(
    Post(uid=121, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=39, c2_number=236, league="Hardcore",
         name="Mr. Wholesome", time=datetime.datetime(2016, 6, 20, 2, 2, 10)))
db.session.add(Post(uid=122, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=119, c2_number=30,
                    league="Hardcore", name="Thrasher", time=datetime.datetime(2016, 6, 13, 19, 25, 39)))
db.session.add(
    Post(uid=123, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=56, c2_number=195, league="Hardcore",
         name="Dredd", time=datetime.datetime(2016, 9, 18, 12, 37, 31)))
db.session.add(
    Post(uid=124, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=201, c2_number=81, league="Hardcore",
         name="Mud Pie Man", time=datetime.datetime(2016, 3, 13, 5, 25, 2)))
db.session.add(Post(uid=125, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=259, c2_number=195,
                    league="Hardcore", name="Toe", time=datetime.datetime(2016, 4, 15, 21, 6, 56)))
db.session.add(
    Post(uid=126, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=227, c2_number=277, league="Hardcore",
         name="Dropkick", time=datetime.datetime(2016, 11, 16, 17, 58, 18)))
db.session.add(
    Post(uid=127, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=234, c2_number=182, league="Hardcore",
         name="Mule Skinner", time=datetime.datetime(2016, 7, 18, 22, 25, 3)))
db.session.add(
    Post(uid=128, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=174, c2_number=238, league="Hardcore",
         name="Toolmaker", time=datetime.datetime(2016, 9, 26, 5, 30, 34)))
db.session.add(Post(uid=129, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=232, c2_number=209,
                    league="Hardcore", name="Drop Stone", time=datetime.datetime(2016, 3, 28, 17, 9, 30)))
db.session.add(
    Post(uid=130, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=292, c2_number=76, league="Hardcore",
         name="Murmur", time=datetime.datetime(2016, 2, 25, 22, 19, 47)))
db.session.add(
    Post(uid=131, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=177, c2_number=140, league="Hardcore",
         name="Tough Nut", time=datetime.datetime(2016, 11, 13, 14, 35, 14)))
db.session.add(
    Post(uid=132, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=265, c2_number=165, league="Hardcore",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 5, 24, 2, 42, 8)))
db.session.add(
    Post(uid=133, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=26, c2_number=223, league="Hardcore",
         name="Nacho", time=datetime.datetime(2016, 2, 13, 11, 48, 23)))
db.session.add(
    Post(uid=134, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=63, c2_number=143, league="Hardcore",
         name="Trip", time=datetime.datetime(2016, 1, 21, 16, 19, 47)))
db.session.add(Post(uid=135, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=279, c2_number=105,
                    league="Hardcore", name="Easy Sweep", time=datetime.datetime(2016, 5, 2, 1, 28, 43)))
db.session.add(
    Post(uid=136, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=190, c2_number=43, league="Hardcore",
         name="Natural Mess", time=datetime.datetime(2016, 9, 5, 3, 31, 39)))
db.session.add(
    Post(uid=137, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=105, c2_number=126, league="Hardcore",
         name="Troubadour", time=datetime.datetime(2016, 9, 16, 18, 21, 34)))
db.session.add(
    Post(uid=138, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=105, c2_number=252, league="Hardcore",
         name="Electric Player", time=datetime.datetime(2016, 2, 20, 22, 20, 35)))
db.session.add(
    Post(uid=139, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=116, c2_number=179, league="Hardcore",
         name="Necromancer", time=datetime.datetime(2016, 2, 23, 12, 26, 22)))
db.session.add(
    Post(uid=140, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=171, c2_number=301, league="Hardcore",
         name="Turnip King", time=datetime.datetime(2016, 11, 23, 13, 2, 52)))
db.session.add(
    Post(uid=141, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=137, c2_number=155, league="Hardcore",
         name="Esquire", time=datetime.datetime(2016, 11, 8, 13, 41, 11)))
db.session.add(
    Post(uid=142, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=115, c2_number=222, league="Hardcore",
         name="Neophyte Believer", time=datetime.datetime(2016, 1, 3, 5, 26, 16)))
db.session.add(
    Post(uid=143, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=193, c2_number=44, league="Hardcore",
         name="Twitch", time=datetime.datetime(2016, 7, 8, 18, 39, 11)))
db.session.add(
    Post(uid=144, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=280, c2_number=104, league="Hardcore",
         name="Fast Draw", time=datetime.datetime(2016, 8, 13, 16, 30, 38)))
db.session.add(
    Post(uid=145, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=63, c2_number=263, league="Hardcore",
         name="Nessie", time=datetime.datetime(2016, 4, 24, 8, 14, 46)))
db.session.add(
    Post(uid=146, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=120, c2_number=244, league="Hardcore",
         name="Vagabond Warrior", time=datetime.datetime(2016, 11, 26, 4, 52, 24)))
db.session.add(
    Post(uid=147, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=131, c2_number=242, league="Hardcore",
         name="Flakes", time=datetime.datetime(2016, 2, 26, 7, 15, 34)))
db.session.add(
    Post(uid=148, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=180, c2_number=279, league="Hardcore",
         name="New Cycle", time=datetime.datetime(2016, 6, 23, 14, 6, 44)))
db.session.add(
    Post(uid=149, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=183, c2_number=259, league="Hardcore",
         name="Voluntary", time=datetime.datetime(2016, 8, 27, 7, 10, 25)))
db.session.add(
    Post(uid=150, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=199, c2_number=129, league="Hardcore",
         name="Flint", time=datetime.datetime(2016, 1, 11, 11, 17, 41)))
db.session.add(
    Post(uid=151, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=229, c2_number=313, league="Hardcore",
         name="Nickname Master", time=datetime.datetime(2016, 10, 17, 15, 37, 56)))
db.session.add(
    Post(uid=152, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=273, c2_number=61, league="Hardcore",
         name="Vortex", time=datetime.datetime(2016, 10, 2, 5, 24, 41)))
db.session.add(Post(uid=153, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=275, c2_number=231,
                    league="Hardcore", name="Freak", time=datetime.datetime(2016, 11, 22, 2, 2, 47)))
db.session.add(
    Post(uid=154, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=26, c2_number=233, league="Hardcore",
         name="Nightmare King", time=datetime.datetime(2016, 1, 28, 5, 1, 37)))
db.session.add(
    Post(uid=155, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=177, c2_number=180, league="Hardcore",
         name="Washer", time=datetime.datetime(2016, 7, 12, 21, 30, 38)))
db.session.add(
    Post(uid=156, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=120, c2_number=72, league="Hardcore",
         name="Gas Man", time=datetime.datetime(2016, 4, 28, 20, 19, 54)))
db.session.add(
    Post(uid=157, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=123, c2_number=49, league="Hardcore",
         name="Night Train", time=datetime.datetime(2016, 1, 20, 3, 2, 29)))
db.session.add(
    Post(uid=158, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=99, c2_number=286, league="Hardcore",
         name="Waylay Dave", time=datetime.datetime(2016, 2, 20, 16, 36, 57)))
db.session.add(
    Post(uid=159, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=39, c2_number=149, league="Hardcore",
         name="Glyph", time=datetime.datetime(2016, 4, 25, 12, 23, 56)))
db.session.add(
    Post(uid=160, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=40, c2_number=30, league="Hardcore",
         name="Old Man Winter", time=datetime.datetime(2016, 11, 13, 3, 25, 8)))
db.session.add(
    Post(uid=161, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=171, c2_number=276, league="Hardcore",
         name="Wheels", time=datetime.datetime(2016, 2, 18, 16, 29, 25)))
db.session.add(
    Post(uid=162, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=41, c2_number=317, league="Hardcore",
         name="Grave Digger", time=datetime.datetime(2016, 5, 2, 1, 56, 32)))
db.session.add(
    Post(uid=163, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=262, c2_number=41, league="Hardcore",
         name="Old Orange Eyes", time=datetime.datetime(2016, 12, 25, 20, 13, 29)))
db.session.add(
    Post(uid=164, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=154, c2_number=304, league="Hardcore",
         name="Wooden Man", time=datetime.datetime(2016, 4, 23, 2, 9, 43)))
db.session.add(
    Post(uid=165, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=75, c2_number=243, league="Hardcore",
         name="Guillotine", time=datetime.datetime(2016, 5, 13, 19, 50, 21)))
db.session.add(
    Post(uid=166, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=230, c2_number=162, league="Hardcore",
         name="Old Regret", time=datetime.datetime(2016, 7, 18, 3, 49, 16)))
db.session.add(
    Post(uid=167, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=70, c2_number=243, league="Hardcore",
         name="Woo Woo", time=datetime.datetime(2016, 1, 27, 8, 0, 16)))
db.session.add(
    Post(uid=168, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=131, c2_number=25, league="Hardcore",
         name="Gunhawk", time=datetime.datetime(2016, 5, 21, 3, 22, 1)))
db.session.add(
    Post(uid=169, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=42, c2_number=180, league="Hardcore",
         name="Onion King", time=datetime.datetime(2016, 5, 7, 5, 46, 6)))
db.session.add(
    Post(uid=170, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=69, c2_number=116, league="Hardcore",
         name="Yellow Menace", time=datetime.datetime(2016, 9, 20, 20, 23, 16)))
db.session.add(Post(uid=171, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=251, c2_number=179,
                    league="Hardcore", name="High Kingdom Warrior", time=datetime.datetime(2016, 6, 24, 13, 23, 8)))
db.session.add(
    Post(uid=172, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=77, c2_number=218, league="Hardcore",
         name="Osprey", time=datetime.datetime(2016, 8, 12, 11, 16, 35)))
db.session.add(
    Post(uid=173, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=167, c2_number=84, league="Hardcore",
         name="Zero Charisma", time=datetime.datetime(2016, 12, 26, 13, 48, 48)))
db.session.add(
    Post(uid=174, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=247, c2_number=20, league="Hardcore",
         name="Highlander Monk", time=datetime.datetime(2016, 11, 17, 8, 20, 49)))
db.session.add(
    Post(uid=175, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=294, c2_number=177, league="Hardcore",
         name="Overrun", time=datetime.datetime(2016, 8, 8, 18, 50, 4)))
db.session.add(
    Post(uid=176, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=114, c2_number=131, league="Hardcore",
         name="Zesty Dragon", time=datetime.datetime(2016, 10, 4, 9, 18, 30)))
db.session.add(
    Post(uid=177, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=92, c2_number=147, league="Hardcore",
         name="Zod", time=datetime.datetime(2016, 6, 8, 10, 58, 43)))
db.session.add(
    Post(uid=0, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=161, c2_number=126, league="Hardcore",
         name="101", time=datetime.datetime(2016, 7, 13, 6, 58, 44)))
db.session.add(
    Post(uid=1, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=300, c2_number=185, league="Hardcore",
         name="Houston", time=datetime.datetime(2016, 1, 2, 11, 15, 26)))
db.session.add(
    Post(uid=2, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=145, c2_number=264, league="Hardcore",
         name="Pinball Wizard", time=datetime.datetime(2016, 11, 28, 13, 37, 45)))
db.session.add(
    Post(uid=3, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=27, c2_number=114, league="Hardcore",
         name="Accidental Genius", time=datetime.datetime(2016, 2, 10, 1, 45, 4)))
db.session.add(
    Post(uid=4, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=101, c2_number=258, league="Hardcore",
         name="Hyper", time=datetime.datetime(2016, 11, 13, 16, 24, 6)))
db.session.add(
    Post(uid=5, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=190, c2_number=259, league="Hardcore",
         name="Pluto", time=datetime.datetime(2016, 10, 20, 6, 28, 51)))
db.session.add(
    Post(uid=6, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=313, c2_number=179, league="Hardcore",
         name="Alpha", time=datetime.datetime(2016, 1, 25, 20, 12, 39)))
db.session.add(Post(uid=7, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=124, c2_number=285, league="Hardcore",
                    name="Jester", time=datetime.datetime(2016, 6, 16, 4, 46, 51)))
db.session.add(
    Post(uid=8, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=222, c2_number=153, league="Hardcore",
         name="Pogue", time=datetime.datetime(2016, 10, 2, 5, 16, 26)))
db.session.add(
    Post(uid=9, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=194, c2_number=182, league="Hardcore",
         name="Airport Hobo", time=datetime.datetime(2016, 7, 12, 0, 53, 44)))
db.session.add(
    Post(uid=10, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=149, c2_number=303, league="Hardcore",
         name="Jigsaw", time=datetime.datetime(2016, 2, 17, 12, 46, 28)))
db.session.add(Post(uid=11, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=245, c2_number=172,
                    league="Hardcore", name="Prometheus", time=datetime.datetime(2016, 8, 11, 2, 1, 4)))
db.session.add(
    Post(uid=12, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=291, c2_number=23, league="Hardcore",
         name="Bearded Angler", time=datetime.datetime(2016, 9, 21, 4, 23, 14)))
db.session.add(
    Post(uid=13, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=102, c2_number=264, league="Hardcore",
         name="Joker's Grin", time=datetime.datetime(2016, 2, 25, 12, 23, 22)))
db.session.add(
    Post(uid=14, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=140, c2_number=174, league="Hardcore",
         name="Psycho Thinker", time=datetime.datetime(2016, 11, 10, 19, 39, 57)))
db.session.add(
    Post(uid=15, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=156, c2_number=203, league="Hardcore",
         name="Beetle King", time=datetime.datetime(2016, 2, 7, 17, 12, 22)))
db.session.add(Post(uid=16, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=253, c2_number=109,
                    league="Hardcore", name="Judge", time=datetime.datetime(2016, 7, 6, 22, 26, 13)))
db.session.add(
    Post(uid=17, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=150, c2_number=25, league="Hardcore",
         name="Pusher", time=datetime.datetime(2016, 8, 27, 21, 22, 39)))
db.session.add(
    Post(uid=18, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=186, c2_number=109, league="Hardcore",
         name="Bitmap", time=datetime.datetime(2016, 3, 2, 4, 0, 53)))
db.session.add(Post(uid=19, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=129, c2_number=164,
                    league="Hardcore", name="Junkyard Dog", time=datetime.datetime(2016, 3, 10, 18, 8, 52)))
db.session.add(
    Post(uid=20, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=263, c2_number=132, league="Hardcore",
         name="Riff Raff", time=datetime.datetime(2016, 11, 5, 11, 40, 24)))
db.session.add(
    Post(uid=21, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=262, c2_number=234, league="Hardcore",
         name="Blister", time=datetime.datetime(2016, 5, 22, 4, 11, 10)))
db.session.add(
    Post(uid=22, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=67, c2_number=78, league="Hardcore",
         name="K-9", time=datetime.datetime(2016, 12, 21, 1, 56, 38)))
db.session.add(
    Post(uid=23, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=216, c2_number=312, league="Hardcore",
         name="Roadblock", time=datetime.datetime(2016, 9, 12, 0, 43, 14)))
db.session.add(
    Post(uid=24, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=107, c2_number=188, league="Hardcore",
         name="Bowie", time=datetime.datetime(2016, 4, 4, 16, 56, 17)))
db.session.add(
    Post(uid=25, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=289, c2_number=87, league="Hardcore",
         name="Keystone", time=datetime.datetime(2016, 5, 21, 22, 29, 36)))
db.session.add(
    Post(uid=26, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=299, c2_number=202, league="Hardcore",
         name="Rooster", time=datetime.datetime(2016, 9, 6, 20, 18, 11)))
db.session.add(
    Post(uid=27, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=249, c2_number=121, league="Hardcore",
         name="Bowler", time=datetime.datetime(2016, 12, 9, 2, 48, 46)))
db.session.add(Post(uid=28, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=265, c2_number=122, league="Hardcore",
                    name="Kickstart", time=datetime.datetime(2016, 10, 7, 12, 23, 1)))
db.session.add(
    Post(uid=29, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=125, c2_number=179, league="Hardcore",
         name="Sandbox", time=datetime.datetime(2016, 5, 16, 18, 16, 1)))
db.session.add(Post(uid=30, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=278, c2_number=34, league="Hardcore",
                    name="Breadmaker", time=datetime.datetime(2016, 11, 24, 4, 41, 38)))
db.session.add(
    Post(uid=31, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=47, c2_number=168, league="Hardcore",
         name="Kill Switch", time=datetime.datetime(2016, 9, 1, 12, 55, 9)))
db.session.add(Post(uid=32, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=211, c2_number=141, league="Hardcore",
                    name="Scrapper", time=datetime.datetime(2016, 12, 4, 13, 51, 30)))
db.session.add(Post(uid=33, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=301, c2_number=228, league="Hardcore",
                    name="Broomspun", time=datetime.datetime(2016, 10, 23, 1, 33, 51)))
db.session.add(
    Post(uid=34, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=162, c2_number=256, league="Hardcore",
         name="Kingfisher", time=datetime.datetime(2016, 6, 24, 16, 6, 39)))
db.session.add(
    Post(uid=35, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=26, c2_number=52, league="Hardcore",
         name="Screwtape", time=datetime.datetime(2016, 7, 8, 19, 32, 35)))
db.session.add(
    Post(uid=36, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=45, c2_number=317, league="Hardcore",
         name="Buckshot", time=datetime.datetime(2016, 11, 15, 17, 2, 6)))
db.session.add(
    Post(uid=37, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=165, c2_number=102, league="Hardcore",
         name="Kitchen", time=datetime.datetime(2016, 8, 18, 22, 44, 39)))
db.session.add(
    Post(uid=38, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=210, c2_number=99, league="Hardcore",
         name="Sexual Chocolate", time=datetime.datetime(2016, 7, 20, 10, 14, 52)))
db.session.add(
    Post(uid=39, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=130, c2_number=117, league="Hardcore",
         name="Bugger", time=datetime.datetime(2016, 8, 10, 16, 27, 0)))
db.session.add(
    Post(uid=40, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=290, c2_number=203, league="Hardcore",
         name="Knuckles", time=datetime.datetime(2016, 1, 17, 16, 27, 25)))
db.session.add(
    Post(uid=41, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=250, c2_number=191, league="Hardcore",
         name="Shadow Chaser", time=datetime.datetime(2016, 7, 10, 9, 5, 13)))
db.session.add(Post(uid=42, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=75, c2_number=167, league="Hardcore",
                    name="Cabbie", time=datetime.datetime(2016, 10, 24, 5, 26, 37)))
db.session.add(Post(uid=43, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=228, c2_number=147, league="Hardcore",
                    name="Lady Killer", time=datetime.datetime(2016, 9, 20, 3, 39, 11)))
db.session.add(
    Post(uid=44, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=169, c2_number=89, league="Hardcore",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 1, 11, 16, 30, 33)))
db.session.add(Post(uid=45, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=238, c2_number=317, league="Hardcore",
                    name="Candy Butcher", time=datetime.datetime(2016, 11, 9, 7, 20, 27)))
db.session.add(Post(uid=46, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=264, c2_number=116, league="Hardcore",
                    name="Liquid Science", time=datetime.datetime(2016, 8, 11, 9, 24, 5)))
db.session.add(
    Post(uid=47, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=92, c2_number=227, league="Hardcore",
         name="Shooter", time=datetime.datetime(2016, 7, 23, 15, 14, 10)))
db.session.add(Post(uid=48, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=80, c2_number=265, league="Hardcore",
                    name="Capital F", time=datetime.datetime(2016, 9, 3, 19, 18, 26)))
db.session.add(
    Post(uid=49, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=291, c2_number=248, league="Hardcore",
         name="Little Cobra", time=datetime.datetime(2016, 10, 8, 16, 18, 34)))
db.session.add(Post(uid=50, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=55, c2_number=255, league="Hardcore",
                    name="Sidewalk Enforcer", time=datetime.datetime(2016, 3, 15, 2, 42, 32)))
db.session.add(Post(uid=51, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=173, c2_number=187, league="Hardcore",
                    name="Captain Peroxide", time=datetime.datetime(2016, 8, 4, 22, 0, 25)))
db.session.add(
    Post(uid=52, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=79, c2_number=39, league="Hardcore",
         name="Little General", time=datetime.datetime(2016, 2, 10, 19, 12, 44)))
db.session.add(
    Post(uid=53, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=104, c2_number=49, league="Hardcore",
         name="Skull Crusher", time=datetime.datetime(2016, 11, 4, 2, 26, 1)))
db.session.add(
    Post(uid=54, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=139, c2_number=136, league="Hardcore",
         name="Celtic Charger", time=datetime.datetime(2016, 11, 27, 20, 9, 14)))
db.session.add(
    Post(uid=55, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=283, c2_number=201, league="Hardcore",
         name="Lord Nikon", time=datetime.datetime(2016, 10, 8, 17, 6, 42)))
db.session.add(
    Post(uid=56, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=117, c2_number=281, league="Hardcore",
         name="Sky Bully", time=datetime.datetime(2016, 4, 9, 22, 4, 30)))
db.session.add(
    Post(uid=57, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=106, c2_number=104, league="Hardcore",
         name="Cereal Killer", time=datetime.datetime(2016, 2, 26, 7, 28, 58)))
db.session.add(
    Post(uid=58, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=249, c2_number=156, league="Hardcore",
         name="Lord Pistachio", time=datetime.datetime(2016, 2, 26, 14, 25, 29)))
db.session.add(
    Post(uid=59, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=238, c2_number=76, league="Hardcore",
         name="Slow Trot", time=datetime.datetime(2016, 11, 14, 0, 10, 12)))
db.session.add(Post(uid=60, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=23, c2_number=38, league="Hardcore",
                    name="Chicago Blackout", time=datetime.datetime(2016, 4, 16, 13, 6, 46)))
db.session.add(Post(uid=61, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=255, c2_number=142, league="Hardcore",
                    name="Mad Irishman", time=datetime.datetime(2016, 10, 28, 10, 36, 47)))
db.session.add(Post(uid=62, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=39, c2_number=89, league="Hardcore",
                    name="Snake Eyes", time=datetime.datetime(2016, 3, 11, 19, 19, 42)))
db.session.add(Post(uid=63, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=310, c2_number=133, league="Hardcore",
                    name="Chocolate Thunder", time=datetime.datetime(2016, 5, 4, 6, 1, 34)))
db.session.add(
    Post(uid=64, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=152, c2_number=156, league="Hardcore",
         name="Mad Jack", time=datetime.datetime(2016, 2, 2, 13, 41, 55)))
db.session.add(Post(uid=65, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=169, c2_number=136,
                    league="Hardcore", name="Snow Hound", time=datetime.datetime(2016, 4, 21, 20, 55, 50)))
db.session.add(
    Post(uid=66, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=228, c2_number=225, league="Hardcore",
         name="Chuckles", time=datetime.datetime(2016, 12, 10, 17, 33, 13)))
db.session.add(
    Post(uid=67, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=243, c2_number=201, league="Hardcore",
         name="Mad Rascal", time=datetime.datetime(2016, 3, 9, 13, 23, 44)))
db.session.add(
    Post(uid=68, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=238, c2_number=99, league="Hardcore",
         name="Sofa King", time=datetime.datetime(2016, 6, 17, 18, 55, 27)))
db.session.add(
    Post(uid=69, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=107, c2_number=184, league="Hardcore",
         name="Commando", time=datetime.datetime(2016, 11, 3, 18, 0, 25)))
db.session.add(
    Post(uid=70, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=234, c2_number=138, league="Hardcore",
         name="Manimal", time=datetime.datetime(2016, 11, 25, 17, 32, 15)))
db.session.add(
    Post(uid=71, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=181, c2_number=228, league="Hardcore",
         name="Speedwell", time=datetime.datetime(2016, 12, 17, 18, 54, 13)))
db.session.add(
    Post(uid=72, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=317, c2_number=147, league="Hardcore",
         name="Cool Whip", time=datetime.datetime(2016, 9, 22, 8, 27, 12)))
db.session.add(
    Post(uid=73, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=108, c2_number=110, league="Hardcore",
         name="Marbles", time=datetime.datetime(2016, 11, 4, 2, 5, 41)))
db.session.add(
    Post(uid=74, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=201, c2_number=46, league="Hardcore",
         name="Spider Fuji", time=datetime.datetime(2016, 12, 23, 21, 26, 8)))
db.session.add(
    Post(uid=75, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=251, c2_number=67, league="Hardcore",
         name="Cosmo", time=datetime.datetime(2016, 2, 9, 17, 7, 41)))
db.session.add(
    Post(uid=76, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=153, c2_number=60, league="Hardcore",
         name="Married Man", time=datetime.datetime(2016, 11, 18, 19, 4, 40)))
db.session.add(
    Post(uid=77, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=245, c2_number=253, league="Hardcore",
         name="Springheel Jack", time=datetime.datetime(2016, 12, 14, 19, 51, 56)))
db.session.add(
    Post(uid=78, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=289, c2_number=288, league="Hardcore",
         name="Crash Override", time=datetime.datetime(2016, 10, 11, 8, 5, 42)))
db.session.add(Post(uid=79, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=90, c2_number=104, league="Hardcore",
                    name="Marshmallow", time=datetime.datetime(2016, 6, 6, 19, 39, 44)))
db.session.add(
    Post(uid=80, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=49, c2_number=191, league="Hardcore",
         name="Squatch", time=datetime.datetime(2016, 10, 21, 19, 37, 8)))
db.session.add(
    Post(uid=81, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=313, c2_number=217, league="Hardcore",
         name="Crash Test", time=datetime.datetime(2016, 10, 14, 8, 43, 21)))
db.session.add(
    Post(uid=82, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=85, c2_number=125, league="Hardcore",
         name="Mental", time=datetime.datetime(2016, 2, 2, 5, 7, 3)))
db.session.add(
    Post(uid=83, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=201, c2_number=88, league="Hardcore",
         name="Stacker of Wheat", time=datetime.datetime(2016, 11, 24, 8, 2, 1)))
db.session.add(Post(uid=84, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=143, c2_number=117, league="Hardcore",
                    name="Crazy Eights", time=datetime.datetime(2016, 3, 8, 6, 41, 53)))
db.session.add(
    Post(uid=85, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=226, c2_number=144, league="Hardcore",
         name="Mercury Reborn", time=datetime.datetime(2016, 12, 3, 3, 55, 29)))
db.session.add(
    Post(uid=86, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=197, c2_number=232, league="Hardcore",
         name="Sugar Man", time=datetime.datetime(2016, 4, 19, 10, 56, 1)))
db.session.add(
    Post(uid=87, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=145, c2_number=162, league="Hardcore",
         name="Criss Cross", time=datetime.datetime(2016, 10, 10, 6, 41, 6)))
db.session.add(
    Post(uid=88, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=36, c2_number=222, league="Hardcore",
         name="Midas", time=datetime.datetime(2016, 6, 18, 10, 2, 23)))
db.session.add(
    Post(uid=89, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=118, c2_number=319, league="Hardcore",
         name="Suicide Jockey", time=datetime.datetime(2016, 6, 16, 10, 36, 29)))
db.session.add(
    Post(uid=90, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=214, c2_number=315, league="Hardcore",
         name="Cross Thread", time=datetime.datetime(2016, 6, 13, 17, 49, 33)))
db.session.add(
    Post(uid=91, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=268, c2_number=317, league="Hardcore",
         name="Midnight Rambler", time=datetime.datetime(2016, 6, 20, 22, 15, 43)))
db.session.add(
    Post(uid=92, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=69, c2_number=129, league="Hardcore",
         name="Swampmasher", time=datetime.datetime(2016, 6, 17, 17, 5, 45)))
db.session.add(
    Post(uid=93, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=289, c2_number=101, league="Hardcore",
         name="Cujo", time=datetime.datetime(2016, 6, 6, 1, 1, 3)))
db.session.add(
    Post(uid=94, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=54, c2_number=228, league="Hardcore",
         name="Midnight Rider", time=datetime.datetime(2016, 11, 5, 15, 42, 46)))
db.session.add(
    Post(uid=95, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=131, c2_number=62, league="Hardcore",
         name="Swerve", time=datetime.datetime(2016, 6, 12, 3, 19, 2)))
db.session.add(Post(uid=96, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=258, c2_number=56, league="Hardcore",
                    name="Dancing Madman", time=datetime.datetime(2016, 4, 21, 13, 12, 30)))
db.session.add(Post(uid=97, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=48, c2_number=285, league="Hardcore",
                    name="Mindless Bobcat", time=datetime.datetime(2016, 7, 17, 14, 48, 1)))
db.session.add(
    Post(uid=98, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=61, c2_number=296, league="Hardcore",
         name="Tacklebox", time=datetime.datetime(2016, 12, 21, 5, 53, 22)))
db.session.add(
    Post(uid=99, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=317, c2_number=243, league="Hardcore",
         name="Dangle", time=datetime.datetime(2016, 3, 3, 16, 35, 2)))
db.session.add(
    Post(uid=100, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=267, c2_number=177, league="Legacy",
         name="Mr. 44", time=datetime.datetime(2016, 10, 8, 17, 26, 6)))
db.session.add(
    Post(uid=101, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=110, c2_number=296, league="Legacy",
         name="Take Away", time=datetime.datetime(2016, 11, 9, 11, 40, 10)))
db.session.add(Post(uid=102, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=94, c2_number=288, league="Legacy",
                    name="Dark Horse", time=datetime.datetime(2016, 7, 13, 9, 52, 41)))
db.session.add(
    Post(uid=103, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=135, c2_number=273, league="Legacy",
         name="Mr. Fabulous", time=datetime.datetime(2016, 6, 19, 10, 42, 48)))
db.session.add(Post(uid=104, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=131, c2_number=149, league="Legacy",
                    name="Tan Stallion", time=datetime.datetime(2016, 5, 23, 2, 58, 50)))
db.session.add(
    Post(uid=105, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=116, c2_number=173, league="Legacy",
         name="Day Hawk", time=datetime.datetime(2016, 1, 15, 0, 47, 42)))
db.session.add(
    Post(uid=106, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=124, c2_number=310, league="Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 2, 6, 14, 16, 55)))
db.session.add(
    Post(uid=107, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=194, c2_number=199, league="Legacy",
         name="The China Wall", time=datetime.datetime(2016, 10, 15, 1, 20, 6)))
db.session.add(
    Post(uid=108, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=272, c2_number=155, league="Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 1, 8, 15, 30, 58)))
db.session.add(
    Post(uid=109, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=124, c2_number=219, league="Legacy",
         name="Mr. Lucky", time=datetime.datetime(2016, 9, 1, 13, 30, 50)))
db.session.add(
    Post(uid=110, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=252, c2_number=76, league="Legacy",
         name="The Dude", time=datetime.datetime(2016, 3, 17, 12, 42, 21)))
db.session.add(
    Post(uid=111, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=208, c2_number=64, league="Legacy",
         name="Digger", time=datetime.datetime(2016, 8, 1, 10, 14, 57)))
db.session.add(
    Post(uid=112, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=264, c2_number=154, league="Legacy",
         name="Mr. Peppermint", time=datetime.datetime(2016, 5, 17, 22, 12, 4)))
db.session.add(
    Post(uid=113, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=309, c2_number=278, league="Legacy",
         name="The Flying Mouse", time=datetime.datetime(2016, 6, 10, 9, 48, 4)))
db.session.add(Post(uid=114, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=188, c2_number=126, league="Legacy",
                    name="Disco Thunder", time=datetime.datetime(2016, 10, 7, 11, 28, 7)))
db.session.add(Post(uid=115, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=267, c2_number=252, league="Legacy",
                    name="Mr. Spy", time=datetime.datetime(2016, 9, 10, 22, 0, 44)))
db.session.add(
    Post(uid=116, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=208, c2_number=133, league="Legacy",
         name="The Happy Jock", time=datetime.datetime(2016, 1, 5, 12, 37, 23)))
db.session.add(
    Post(uid=117, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=182, c2_number=161, league="Legacy",
         name="Disco Potato", time=datetime.datetime(2016, 9, 15, 2, 18, 11)))
db.session.add(
    Post(uid=118, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=28, c2_number=270, league="Legacy",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 1, 1, 14, 47, 18)))
db.session.add(
    Post(uid=119, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=314, c2_number=157,
         league="Legacy", name="The Howling Swede", time=datetime.datetime(2016, 1, 27, 14, 24, 38)))
db.session.add(
    Post(uid=120, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=306, c2_number=43, league="Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 9, 21, 14, 33, 6)))
db.session.add(Post(uid=121, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=190, c2_number=252,
                    league="Legacy", name="Mr. Wholesome", time=datetime.datetime(2016, 2, 2, 16, 8, 12)))
db.session.add(
    Post(uid=122, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=168, c2_number=277, league="Legacy",
         name="Thrasher", time=datetime.datetime(2016, 3, 3, 2, 37, 4)))
db.session.add(
    Post(uid=123, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=219, c2_number=272, league="Legacy",
         name="Dredd", time=datetime.datetime(2016, 5, 27, 9, 47, 51)))
db.session.add(Post(uid=124, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=251, c2_number=306,
                    league="Legacy", name="Mud Pie Man", time=datetime.datetime(2016, 6, 15, 3, 24, 41)))
db.session.add(Post(uid=125, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=26, c2_number=117,
                    league="Legacy", name="Toe", time=datetime.datetime(2016, 10, 12, 8, 27, 10)))
db.session.add(Post(uid=126, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=74, c2_number=142,
                    league="Legacy", name="Dropkick", time=datetime.datetime(2016, 2, 28, 10, 49, 36)))
db.session.add(Post(uid=127, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=105, c2_number=275,
                    league="Legacy", name="Mule Skinner", time=datetime.datetime(2016, 8, 1, 4, 44, 1)))
db.session.add(Post(uid=128, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=31, c2_number=255,
                    league="Legacy", name="Toolmaker", time=datetime.datetime(2016, 7, 5, 8, 13, 41)))
db.session.add(Post(uid=129, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=317, c2_number=175,
                    league="Legacy", name="Drop Stone", time=datetime.datetime(2016, 7, 18, 6, 20, 26)))
db.session.add(Post(uid=130, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=195, c2_number=103,
                    league="Legacy", name="Murmur", time=datetime.datetime(2016, 6, 6, 13, 58, 7)))
db.session.add(Post(uid=131, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=153, c2_number=192,
                    league="Legacy", name="Tough Nut", time=datetime.datetime(2016, 9, 15, 9, 53, 15)))
db.session.add(
    Post(uid=132, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=272, c2_number=24, league="Legacy",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 12, 12, 18, 54, 9)))
db.session.add(
    Post(uid=133, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=91, c2_number=232, league="Legacy",
         name="Nacho", time=datetime.datetime(2016, 8, 6, 6, 53, 45)))
db.session.add(Post(uid=134, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=113, c2_number=30,
                    league="Legacy", name="Trip", time=datetime.datetime(2016, 8, 20, 2, 21, 57)))
db.session.add(
    Post(uid=135, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=215, c2_number=224, league="Legacy",
         name="Easy Sweep", time=datetime.datetime(2016, 12, 11, 10, 26, 17)))
db.session.add(Post(uid=136, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=99, c2_number=103, league="Legacy",
                    name="Natural Mess", time=datetime.datetime(2016, 9, 8, 15, 58, 56)))
db.session.add(
    Post(uid=137, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=149, c2_number=222, league="Legacy",
         name="Troubadour", time=datetime.datetime(2016, 2, 18, 13, 42, 37)))
db.session.add(Post(uid=138, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=295, c2_number=87, league="Legacy",
                    name="Electric Player", time=datetime.datetime(2016, 7, 6, 8, 55, 34)))
db.session.add(Post(uid=139, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=52, c2_number=126, league="Legacy",
                    name="Necromancer", time=datetime.datetime(2016, 5, 23, 0, 45, 6)))
db.session.add(Post(uid=140, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=310, c2_number=273, league="Legacy",
                    name="Turnip King", time=datetime.datetime(2016, 10, 16, 20, 1, 0)))
db.session.add(Post(uid=141, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=82, c2_number=79, league="Legacy",
                    name="Esquire", time=datetime.datetime(2016, 3, 28, 19, 57, 26)))
db.session.add(
    Post(uid=142, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=189, c2_number=39, league="Legacy",
         name="Neophyte Believer", time=datetime.datetime(2016, 2, 12, 20, 37, 6)))
db.session.add(
    Post(uid=143, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=269, c2_number=31, league="Legacy",
         name="Twitch", time=datetime.datetime(2016, 1, 23, 5, 19, 46)))
db.session.add(
    Post(uid=144, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=177, c2_number=37, league="Legacy",
         name="Fast Draw", time=datetime.datetime(2016, 2, 23, 7, 14, 37)))
db.session.add(
    Post(uid=145, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=93, c2_number=162, league="Legacy",
         name="Nessie", time=datetime.datetime(2016, 6, 26, 17, 15, 46)))
db.session.add(Post(uid=146, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=85, c2_number=176, league="Legacy",
                    name="Vagabond Warrior", time=datetime.datetime(2016, 11, 21, 14, 32, 49)))
db.session.add(Post(uid=147, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=316, c2_number=82, league="Legacy",
                    name="Flakes", time=datetime.datetime(2016, 10, 12, 3, 58, 19)))
db.session.add(
    Post(uid=148, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=215, c2_number=242, league="Legacy",
         name="New Cycle", time=datetime.datetime(2016, 4, 25, 4, 22, 45)))
db.session.add(
    Post(uid=149, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=268, c2_number=125, league="Legacy",
         name="Voluntary", time=datetime.datetime(2016, 2, 17, 10, 39, 34)))
db.session.add(
    Post(uid=150, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=279, c2_number=182, league="Legacy", name="Flint",
         time=datetime.datetime(2016, 10, 27, 0, 25, 28)))
db.session.add(Post(uid=151, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=244, c2_number=98, league="Legacy",
                    name="Nickname Master", time=datetime.datetime(2016, 8, 4, 8, 39, 25)))
db.session.add(
    Post(uid=152, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=313, c2_number=250, league="Legacy",
         name="Vortex", time=datetime.datetime(2016, 9, 23, 8, 33, 53)))
db.session.add(Post(uid=153, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=111, c2_number=284, league="Legacy",
                    name="Freak", time=datetime.datetime(2016, 3, 3, 2, 58, 6)))
db.session.add(
    Post(uid=154, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=174, c2_number=212, league="Legacy",
         name="Nightmare King", time=datetime.datetime(2016, 8, 16, 1, 2, 55)))
db.session.add(Post(uid=155, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=168, c2_number=306,
                    league="Legacy", name="Washer", time=datetime.datetime(2016, 6, 12, 15, 38, 42)))
db.session.add(
    Post(uid=156, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=189, c2_number=308, league="Legacy",
         name="Gas Man", time=datetime.datetime(2016, 6, 15, 2, 19, 7)))
db.session.add(
    Post(uid=157, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=99, c2_number=132, league="Legacy",
         name="Night Train", time=datetime.datetime(2016, 6, 13, 6, 5, 20)))
db.session.add(Post(uid=158, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=24, c2_number=42, league="Legacy",
                    name="Waylay Dave", time=datetime.datetime(2016, 2, 15, 7, 47, 1)))
db.session.add(
    Post(uid=159, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=231, c2_number=49, league="Legacy",
         name="Glyph", time=datetime.datetime(2016, 11, 13, 7, 8, 43)))
db.session.add(
    Post(uid=160, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=107, c2_number=180, league="Legacy",
         name="Old Man Winter", time=datetime.datetime(2016, 10, 8, 21, 12, 52)))
db.session.add(
    Post(uid=161, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=286, c2_number=26, league="Legacy",
         name="Wheels", time=datetime.datetime(2016, 11, 28, 22, 37, 42)))
db.session.add(
    Post(uid=162, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=142, c2_number=315, league="Legacy",
         name="Grave Digger", time=datetime.datetime(2016, 8, 15, 7, 53, 43)))
db.session.add(
    Post(uid=163, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=82, c2_number=38, league="Legacy",
         name="Old Orange Eyes", time=datetime.datetime(2016, 12, 18, 18, 49, 15)))
db.session.add(
    Post(uid=164, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=94, c2_number=110, league="Legacy",
         name="Wooden Man", time=datetime.datetime(2016, 1, 7, 18, 23, 11)))
db.session.add(
    Post(uid=165, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=148, c2_number=113, league="Legacy",
         name="Guillotine", time=datetime.datetime(2016, 8, 4, 14, 30, 5)))
db.session.add(
    Post(uid=166, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=78, c2_number=23, league="Legacy",
         name="Old Regret", time=datetime.datetime(2016, 8, 4, 3, 16, 31)))
db.session.add(
    Post(uid=167, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=284, c2_number=95, league="Legacy",
         name="Woo Woo", time=datetime.datetime(2016, 4, 28, 13, 19, 40)))
db.session.add(
    Post(uid=168, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=206, c2_number=236, league="Legacy",
         name="Gunhawk", time=datetime.datetime(2016, 7, 20, 11, 30, 20)))
db.session.add(Post(uid=169, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=124, c2_number=272, league="Legacy",
                    name="Onion King", time=datetime.datetime(2016, 3, 5, 15, 41, 49)))
db.session.add(
    Post(uid=170, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=56, c2_number=309, league="Legacy",
         name="Yellow Menace", time=datetime.datetime(2016, 7, 8, 22, 18, 7)))
db.session.add(
    Post(uid=171, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=110, c2_number=60, league="Legacy",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 6, 17, 17, 6, 25)))
db.session.add(Post(uid=172, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=312, c2_number=304, league="Legacy",
                    name="Osprey", time=datetime.datetime(2016, 10, 11, 15, 19, 12)))
db.session.add(
    Post(uid=173, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=306, c2_number=213, league="Legacy",
         name="Zero Charisma", time=datetime.datetime(2016, 6, 27, 1, 49, 24)))
db.session.add(Post(uid=174, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=54, c2_number=25, league="Legacy",
                    name="Highlander Monk", time=datetime.datetime(2016, 8, 5, 15, 17, 9)))
db.session.add(
    Post(uid=175, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=53, c2_number=123, league="Legacy",
         name="Overrun", time=datetime.datetime(2016, 8, 21, 1, 57, 27)))
db.session.add(Post(uid=176, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=231, c2_number=253, league="Legacy",
                    name="Zesty Dragon", time=datetime.datetime(2016, 8, 25, 14, 58, 0)))
db.session.add(
    Post(uid=177, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=39, c2_number=319, league="Legacy", name="Zod",
         time=datetime.datetime(2016, 6, 8, 9, 40, 44)))
db.session.add(
    Post(uid=0, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=215, c2_number=72, league="Legacy",
         name="101", time=datetime.datetime(2016, 7, 15, 12, 8, 2)))
db.session.add(Post(uid=1, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=81, c2_number=83, league="Legacy",
                    name="Houston", time=datetime.datetime(2016, 7, 2, 21, 47, 0)))
db.session.add(Post(uid=2, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=81, c2_number=120, league="Legacy",
                    name="Pinball Wizard", time=datetime.datetime(2016, 3, 8, 15, 55, 55)))
db.session.add(
    Post(uid=3, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=113, c2_number=202, league="Legacy",
         name="Accidental Genius", time=datetime.datetime(2016, 9, 19, 4, 37, 15)))
db.session.add(Post(uid=4, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=131, c2_number=143, league="Legacy",
                    name="Hyper", time=datetime.datetime(2016, 1, 1, 13, 40, 58)))
db.session.add(Post(uid=5, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=43, c2_number=204, league="Legacy",
                    name="Pluto", time=datetime.datetime(2016, 1, 19, 17, 9, 47)))
db.session.add(Post(uid=6, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=207, c2_number=65, league="Legacy",
                    name="Alpha", time=datetime.datetime(2016, 6, 7, 5, 55, 45)))
db.session.add(
    Post(uid=7, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=149, c2_number=147, league="Legacy",
         name="Jester", time=datetime.datetime(2016, 5, 16, 1, 43, 16)))
db.session.add(
    Post(uid=8, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=251, c2_number=46, league="Legacy", name="Pogue",
         time=datetime.datetime(2016, 3, 27, 13, 58, 17)))
db.session.add(Post(uid=9, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=302, c2_number=76, league="Legacy",
                    name="Airport Hobo", time=datetime.datetime(2016, 9, 13, 14, 39, 50)))
db.session.add(Post(uid=10, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=127, c2_number=51, league="Legacy",
                    name="Jigsaw", time=datetime.datetime(2016, 4, 26, 1, 5, 12)))
db.session.add(Post(uid=11, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=288, c2_number=205, league="Legacy",
                    name="Prometheus", time=datetime.datetime(2016, 12, 12, 2, 4, 52)))
db.session.add(Post(uid=12, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=260, c2_number=303, league="Legacy",
                    name="Bearded Angler", time=datetime.datetime(2016, 8, 17, 7, 1, 33)))
db.session.add(
    Post(uid=13, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=138, c2_number=263, league="Legacy",
         name="Joker's Grin", time=datetime.datetime(2016, 12, 10, 15, 25, 28)))
db.session.add(Post(uid=14, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=43, c2_number=136, league="Legacy",
                    name="Psycho Thinker", time=datetime.datetime(2016, 5, 21, 18, 17, 34)))
db.session.add(
    Post(uid=15, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=268, c2_number=43, league="Legacy",
         name="Beetle King", time=datetime.datetime(2016, 10, 7, 6, 15, 22)))
db.session.add(Post(uid=16, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=234, c2_number=41, league="Legacy",
                    name="Judge", time=datetime.datetime(2016, 9, 8, 1, 34, 13)))
db.session.add(Post(uid=17, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=207, c2_number=63, league="Legacy",
                    name="Pusher", time=datetime.datetime(2016, 5, 6, 8, 12, 53)))
db.session.add(
    Post(uid=18, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=288, c2_number=170, league="Legacy",
         name="Bitmap", time=datetime.datetime(2016, 2, 12, 11, 35, 36)))
db.session.add(
    Post(uid=19, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=87, c2_number=186, league="Legacy",
         name="Junkyard Dog", time=datetime.datetime(2016, 12, 28, 16, 20, 24)))
db.session.add(
    Post(uid=20, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=261, c2_number=264, league="Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 12, 13, 14, 9, 55)))
db.session.add(
    Post(uid=21, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=92, c2_number=49, league="Legacy",
         name="Blister", time=datetime.datetime(2016, 9, 13, 7, 56, 6)))
db.session.add(
    Post(uid=22, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=110, c2_number=293, league="Legacy",
         name="K-9", time=datetime.datetime(2016, 5, 3, 22, 33, 37)))
db.session.add(
    Post(uid=23, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=289, c2_number=242, league="Legacy",
         name="Roadblock", time=datetime.datetime(2016, 10, 11, 21, 6, 5)))
db.session.add(
    Post(uid=24, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=243, c2_number=235, league="Legacy",
         name="Bowie", time=datetime.datetime(2016, 11, 12, 4, 43, 1)))
db.session.add(
    Post(uid=25, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=309, c2_number=133, league="Legacy",
         name="Keystone", time=datetime.datetime(2016, 11, 6, 5, 30, 49)))
db.session.add(Post(uid=26, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=277, c2_number=225, league="Legacy",
                    name="Rooster", time=datetime.datetime(2016, 9, 11, 13, 43, 4)))
db.session.add(Post(uid=27, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=214, c2_number=282, league="Legacy",
                    name="Bowler", time=datetime.datetime(2016, 2, 22, 18, 22, 22)))
db.session.add(
    Post(uid=28, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=310, c2_number=44, league="Legacy",
         name="Kickstart", time=datetime.datetime(2016, 6, 13, 0, 33, 40)))
db.session.add(Post(uid=29, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=165, c2_number=28, league="Legacy",
                    name="Sandbox", time=datetime.datetime(2016, 11, 8, 11, 24, 19)))
db.session.add(
    Post(uid=30, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=288, c2_number=53, league="Legacy",
         name="Breadmaker", time=datetime.datetime(2016, 9, 8, 17, 56, 21)))
db.session.add(Post(uid=31, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=185, c2_number=317,
                    league="Legacy", name="Kill Switch", time=datetime.datetime(2016, 4, 3, 0, 20, 54)))
db.session.add(
    Post(uid=32, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=306, c2_number=228, league="Legacy",
         name="Scrapper", time=datetime.datetime(2016, 12, 23, 6, 43, 51)))
db.session.add(
    Post(uid=33, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=259, c2_number=117, league="Legacy",
         name="Broomspun", time=datetime.datetime(2016, 10, 28, 12, 41, 35)))
db.session.add(
    Post(uid=34, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=149, c2_number=272, league="Legacy",
         name="Kingfisher", time=datetime.datetime(2016, 9, 7, 21, 1, 46)))
db.session.add(
    Post(uid=35, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=54, c2_number=241, league="Legacy",
         name="Screwtape", time=datetime.datetime(2016, 4, 10, 10, 55, 33)))
db.session.add(Post(uid=36, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=171, c2_number=278,
                    league="Legacy", name="Buckshot", time=datetime.datetime(2016, 11, 19, 13, 54, 47)))
db.session.add(
    Post(uid=37, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=158, c2_number=253, league="Legacy",
         name="Kitchen", time=datetime.datetime(2016, 1, 15, 14, 43, 4)))
db.session.add(
    Post(uid=38, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=88, c2_number=241, league="Legacy",
         name="Sexual Chocolate", time=datetime.datetime(2016, 3, 16, 11, 37, 16)))
db.session.add(Post(uid=39, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=174, c2_number=202,
                    league="Legacy", name="Bugger", time=datetime.datetime(2016, 11, 1, 19, 49, 35)))
db.session.add(
    Post(uid=40, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=23, c2_number=218, league="Legacy",
         name="Knuckles", time=datetime.datetime(2016, 8, 25, 14, 43, 31)))
db.session.add(
    Post(uid=41, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=20, c2_number=253, league="Legacy",
         name="Shadow Chaser", time=datetime.datetime(2016, 3, 20, 3, 6, 37)))
db.session.add(
    Post(uid=42, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=59, c2_number=60, league="Legacy",
         name="Cabbie", time=datetime.datetime(2016, 12, 19, 15, 6, 1)))
db.session.add(
    Post(uid=43, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=304, c2_number=213, league="Legacy",
         name="Lady Killer", time=datetime.datetime(2016, 7, 2, 16, 35, 51)))
db.session.add(
    Post(uid=44, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=97, c2_number=287, league="Legacy",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 11, 11, 19, 21, 28)))
db.session.add(
    Post(uid=45, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=290, c2_number=100, league="Legacy",
         name="Candy Butcher", time=datetime.datetime(2016, 9, 15, 15, 11, 27)))
db.session.add(
    Post(uid=46, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=81, c2_number=235, league="Legacy",
         name="Liquid Science", time=datetime.datetime(2016, 8, 20, 1, 20, 49)))
db.session.add(
    Post(uid=47, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=124, c2_number=54, league="Legacy",
         name="Shooter", time=datetime.datetime(2016, 3, 15, 9, 5, 29)))
db.session.add(
    Post(uid=48, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=234, c2_number=307, league="Legacy",
         name="Capital F", time=datetime.datetime(2016, 4, 2, 20, 32, 5)))
db.session.add(Post(uid=49, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=111, c2_number=45,
                    league="Legacy", name="Little Cobra", time=datetime.datetime(2016, 3, 12, 22, 53, 23)))
db.session.add(
    Post(uid=50, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=219, c2_number=251, league="Legacy",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 3, 20, 3, 4, 28)))
db.session.add(
    Post(uid=51, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=232, c2_number=102, league="Legacy",
         name="Captain Peroxide", time=datetime.datetime(2016, 8, 5, 9, 51, 0)))
db.session.add(
    Post(uid=52, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=118, c2_number=122, league="Legacy",
         name="Little General", time=datetime.datetime(2016, 7, 26, 4, 11, 12)))
db.session.add(
    Post(uid=53, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=199, c2_number=280, league="Legacy",
         name="Skull Crusher", time=datetime.datetime(2016, 2, 23, 12, 27, 28)))
db.session.add(
    Post(uid=54, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=173, c2_number=284, league="Legacy",
         name="Celtic Charger", time=datetime.datetime(2016, 7, 4, 14, 26, 24)))
db.session.add(
    Post(uid=55, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=90, c2_number=71, league="Legacy",
         name="Lord Nikon", time=datetime.datetime(2016, 3, 20, 22, 4, 15)))
db.session.add(
    Post(uid=56, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=171, c2_number=47, league="Legacy",
         name="Sky Bully", time=datetime.datetime(2016, 1, 8, 3, 55, 29)))
db.session.add(
    Post(uid=57, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=273, c2_number=60, league="Legacy",
         name="Cereal Killer", time=datetime.datetime(2016, 6, 4, 21, 52, 32)))
db.session.add(
    Post(uid=58, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=217, c2_number=255, league="Legacy",
         name="Lord Pistachio", time=datetime.datetime(2016, 6, 19, 15, 21, 17)))
db.session.add(
    Post(uid=59, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=178, c2_number=175, league="Legacy",
         name="Slow Trot", time=datetime.datetime(2016, 9, 4, 10, 39, 31)))
db.session.add(
    Post(uid=60, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=200, c2_number=30, league="Legacy",
         name="Chicago Blackout", time=datetime.datetime(2016, 6, 13, 12, 57, 47)))
db.session.add(
    Post(uid=61, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=272, c2_number=249, league="Legacy",
         name="Mad Irishman", time=datetime.datetime(2016, 1, 7, 14, 31, 26)))
db.session.add(Post(uid=62, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=223, c2_number=91, league="Legacy",
                    name="Snake Eyes", time=datetime.datetime(2016, 2, 19, 20, 3, 31)))
db.session.add(Post(uid=63, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=21, c2_number=23, league="Legacy",
                    name="Chocolate Thunder", time=datetime.datetime(2016, 8, 25, 2, 56, 40)))
db.session.add(
    Post(uid=64, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=128, c2_number=94, league="Legacy",
         name="Mad Jack", time=datetime.datetime(2016, 1, 23, 15, 26, 36)))
db.session.add(
    Post(uid=65, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=166, c2_number=140, league="Legacy",
         name="Snow Hound", time=datetime.datetime(2016, 12, 17, 11, 13, 58)))
db.session.add(
    Post(uid=66, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=225, c2_number=115, league="Legacy",
         name="Chuckles", time=datetime.datetime(2016, 12, 18, 0, 23, 0)))
db.session.add(Post(uid=67, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=172, c2_number=281,
                    league="Legacy", name="Mad Rascal", time=datetime.datetime(2016, 3, 22, 12, 56, 13)))
db.session.add(
    Post(uid=68, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=222, c2_number=135, league="Legacy",
         name="Sofa King", time=datetime.datetime(2016, 1, 21, 1, 17, 57)))
db.session.add(
    Post(uid=69, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=237, c2_number=91, league="Legacy",
         name="Commando", time=datetime.datetime(2016, 11, 10, 3, 34, 19)))
db.session.add(
    Post(uid=70, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=176, c2_number=255, league="Legacy",
         name="Manimal", time=datetime.datetime(2016, 6, 13, 16, 8, 46)))
db.session.add(
    Post(uid=71, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=68, c2_number=83, league="Legacy",
         name="Speedwell", time=datetime.datetime(2016, 11, 6, 5, 2, 26)))
db.session.add(
    Post(uid=72, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=239, c2_number=120, league="Legacy",
         name="Cool Whip", time=datetime.datetime(2016, 2, 2, 11, 57, 48)))
db.session.add(
    Post(uid=73, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=98, c2_number=131, league="Legacy",
         name="Marbles", time=datetime.datetime(2016, 2, 10, 5, 53, 28)))
db.session.add(
    Post(uid=74, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=126, c2_number=162, league="Legacy",
         name="Spider Fuji", time=datetime.datetime(2016, 9, 27, 1, 21, 49)))
db.session.add(
    Post(uid=75, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=53, c2_number=235, league="Legacy",
         name="Cosmo", time=datetime.datetime(2016, 3, 19, 7, 58, 51)))
db.session.add(
    Post(uid=76, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=314, c2_number=232, league="Legacy",
         name="Married Man", time=datetime.datetime(2016, 11, 1, 10, 43, 51)))
db.session.add(
    Post(uid=77, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=265, c2_number=140, league="Legacy",
         name="Springheel Jack", time=datetime.datetime(2016, 3, 26, 13, 24, 44)))
db.session.add(
    Post(uid=78, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=273, c2_number=312, league="Legacy",
         name="Crash Override", time=datetime.datetime(2016, 10, 5, 6, 30, 55)))
db.session.add(
    Post(uid=79, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=286, c2_number=129, league="Legacy",
         name="Marshmallow", time=datetime.datetime(2016, 5, 14, 1, 15, 28)))
db.session.add(
    Post(uid=80, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=129, c2_number=107, league="Legacy",
         name="Squatch", time=datetime.datetime(2016, 12, 7, 18, 0, 13)))
db.session.add(Post(uid=81, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=146, c2_number=20, league="Legacy",
                    name="Crash Test", time=datetime.datetime(2016, 4, 21, 11, 55, 39)))
db.session.add(
    Post(uid=82, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=135, c2_number=28, league="Legacy",
         name="Mental", time=datetime.datetime(2016, 2, 10, 9, 42, 24)))
db.session.add(
    Post(uid=83, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=204, c2_number=64, league="Legacy",
         name="Stacker of Wheat", time=datetime.datetime(2016, 9, 7, 8, 52, 4)))
db.session.add(
    Post(uid=84, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=68, c2_number=259, league="Legacy",
         name="Crazy Eights", time=datetime.datetime(2016, 3, 5, 17, 46, 40)))
db.session.add(Post(uid=85, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=274, c2_number=64,
                    league="Legacy", name="Mercury Reborn", time=datetime.datetime(2016, 6, 1, 14, 46, 35)))
db.session.add(
    Post(uid=86, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=160, c2_number=120, league="Legacy",
         name="Sugar Man", time=datetime.datetime(2016, 5, 12, 22, 9, 22)))
db.session.add(
    Post(uid=87, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=111, c2_number=194, league="Legacy",
         name="Criss Cross", time=datetime.datetime(2016, 6, 12, 7, 9, 14)))
db.session.add(
    Post(uid=88, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=95, c2_number=220, league="Legacy",
         name="Midas", time=datetime.datetime(2016, 7, 4, 1, 8, 1)))
db.session.add(
    Post(uid=89, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=315, c2_number=77, league="Legacy",
         name="Suicide Jockey", time=datetime.datetime(2016, 5, 13, 19, 26, 41)))
db.session.add(Post(uid=90, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=299, c2_number=201,
                    league="Legacy", name="Cross Thread", time=datetime.datetime(2016, 8, 13, 22, 41, 26)))
db.session.add(
    Post(uid=91, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=22, c2_number=128, league="Legacy",
         name="Midnight Rambler", time=datetime.datetime(2016, 8, 16, 11, 0, 36)))
db.session.add(
    Post(uid=92, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=287, c2_number=270, league="Legacy",
         name="Swampmasher", time=datetime.datetime(2016, 7, 18, 5, 30, 56)))
db.session.add(Post(uid=93, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=128, c2_number=132,
                    league="Legacy", name="Cujo", time=datetime.datetime(2016, 9, 2, 2, 51, 52)))
db.session.add(
    Post(uid=94, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=299, c2_number=278, league="Legacy",
         name="Midnight Rider", time=datetime.datetime(2016, 7, 7, 13, 14, 47)))
db.session.add(
    Post(uid=95, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=144, c2_number=260, league="Legacy",
         name="Swerve", time=datetime.datetime(2016, 9, 4, 1, 53, 47)))
db.session.add(
    Post(uid=96, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=25, c2_number=242, league="Legacy",
         name="Dancing Madman", time=datetime.datetime(2016, 8, 5, 18, 10, 48)))
db.session.add(
    Post(uid=97, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=258, c2_number=111, league="Legacy",
         name="Mindless Bobcat", time=datetime.datetime(2016, 8, 21, 13, 24, 39)))
db.session.add(
    Post(uid=98, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=183, c2_number=36, league="Legacy",
         name="Tacklebox", time=datetime.datetime(2016, 10, 24, 5, 29, 13)))
db.session.add(
    Post(uid=99, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=315, c2_number=247, league="Legacy",
         name="Dangle", time=datetime.datetime(2016, 4, 9, 8, 41, 25)))
db.session.add(
    Post(uid=100, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=255, c2_number=31, league="Legacy",
         name="Mr. 44", time=datetime.datetime(2016, 6, 5, 2, 35, 32)))
db.session.add(
    Post(uid=101, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=164, c2_number=233, league="Legacy",
         name="Take Away", time=datetime.datetime(2016, 10, 8, 4, 45, 38)))
db.session.add(
    Post(uid=102, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=152, c2_number=75, league="Legacy",
         name="Dark Horse", time=datetime.datetime(2016, 10, 5, 13, 55, 43)))
db.session.add(Post(uid=103, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=194, c2_number=119,
                    league="Legacy", name="Mr. Fabulous", time=datetime.datetime(2016, 3, 28, 4, 6, 43)))
db.session.add(
    Post(uid=104, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=166, c2_number=201, league="Legacy",
         name="Tan Stallion", time=datetime.datetime(2016, 6, 6, 15, 2, 37)))
db.session.add(
    Post(uid=105, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=136, c2_number=96, league="Legacy",
         name="Day Hawk", time=datetime.datetime(2016, 5, 25, 6, 32, 40)))
db.session.add(
    Post(uid=106, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=196, c2_number=69, league="Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 1, 1, 10, 57, 53)))
db.session.add(
    Post(uid=107, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=274, c2_number=111, league="Legacy",
         name="The China Wall", time=datetime.datetime(2016, 12, 12, 4, 22, 5)))
db.session.add(
    Post(uid=108, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=37, c2_number=222, league="Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 11, 9, 22, 52, 8)))
db.session.add(
    Post(uid=109, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=111, c2_number=118, league="Legacy",
         name="Mr. Lucky", time=datetime.datetime(2016, 3, 1, 3, 28, 23)))
db.session.add(
    Post(uid=110, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=300, c2_number=208, league="Legacy",
         name="The Dude", time=datetime.datetime(2016, 1, 9, 19, 46, 22)))
db.session.add(
    Post(uid=111, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=153, c2_number=71, league="Legacy",
         name="Digger", time=datetime.datetime(2016, 8, 23, 0, 28, 17)))
db.session.add(
    Post(uid=112, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=91, c2_number=33, league="Legacy",
         name="Mr. Peppermint", time=datetime.datetime(2016, 9, 16, 20, 10, 6)))
db.session.add(
    Post(uid=113, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=99, c2_number=237, league="Legacy",
         name="The Flying Mouse", time=datetime.datetime(2016, 1, 6, 12, 41, 12)))
db.session.add(
    Post(uid=114, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=307, c2_number=306, league="Legacy",
         name="Disco Thunder", time=datetime.datetime(2016, 12, 12, 12, 25, 51)))
db.session.add(
    Post(uid=115, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=176, c2_number=256, league="Legacy",
         name="Mr. Spy", time=datetime.datetime(2016, 8, 13, 10, 38, 51)))
db.session.add(Post(uid=116, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=33, c2_number=107, league="Legacy",
                    name="The Happy Jock", time=datetime.datetime(2016, 3, 21, 20, 20, 50)))
db.session.add(Post(uid=117, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=169, c2_number=193, league="Legacy",
                    name="Disco Potato", time=datetime.datetime(2016, 1, 21, 13, 13, 25)))
db.session.add(
    Post(uid=118, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=119, c2_number=212, league="Legacy",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 2, 23, 8, 11, 52)))
db.session.add(
    Post(uid=119, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=187, c2_number=310, league="Legacy",
         name="The Howling Swede", time=datetime.datetime(2016, 1, 20, 4, 6, 6)))
db.session.add(
    Post(uid=120, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=138, c2_number=73, league="Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 3, 15, 0, 22, 6)))
db.session.add(Post(uid=121, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=127, c2_number=160,
                    league="Legacy", name="Mr. Wholesome", time=datetime.datetime(2016, 1, 21, 3, 38, 10)))
db.session.add(Post(uid=122, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=154, c2_number=68, league="Legacy",
                    name="Thrasher", time=datetime.datetime(2016, 4, 6, 5, 18, 38)))
db.session.add(
    Post(uid=123, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=302, c2_number=316, league="Legacy",
         name="Dredd", time=datetime.datetime(2016, 7, 24, 3, 26, 9)))
db.session.add(
    Post(uid=124, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=272, c2_number=106, league="Legacy",
         name="Mud Pie Man", time=datetime.datetime(2016, 4, 19, 20, 25, 23)))
db.session.add(
    Post(uid=125, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=57, c2_number=161, league="Legacy",
         name="Toe", time=datetime.datetime(2016, 4, 8, 16, 44, 53)))
db.session.add(
    Post(uid=126, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=110, c2_number=102, league="Legacy",
         name="Dropkick", time=datetime.datetime(2016, 3, 4, 7, 17, 54)))
db.session.add(
    Post(uid=127, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=97, c2_number=228, league="Legacy",
         name="Mule Skinner", time=datetime.datetime(2016, 2, 24, 0, 34, 41)))
db.session.add(
    Post(uid=128, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=311, c2_number=35, league="Legacy",
         name="Toolmaker", time=datetime.datetime(2016, 11, 2, 11, 4, 35)))
db.session.add(
    Post(uid=129, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=238, c2_number=268, league="Legacy",
         name="Drop Stone", time=datetime.datetime(2016, 1, 10, 9, 11, 37)))
db.session.add(
    Post(uid=130, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=47, c2_number=222, league="Legacy",
         name="Murmur", time=datetime.datetime(2016, 9, 2, 7, 10, 19)))
db.session.add(
    Post(uid=131, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=190, c2_number=305, league="Legacy",
         name="Tough Nut", time=datetime.datetime(2016, 9, 3, 16, 0, 4)))
db.session.add(
    Post(uid=132, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=180, c2_number=82, league="Legacy",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 9, 2, 17, 12, 36)))
db.session.add(
    Post(uid=133, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=269, c2_number=123, league="Legacy",
         name="Nacho", time=datetime.datetime(2016, 10, 3, 10, 48, 28)))
db.session.add(Post(uid=134, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=71, c2_number=203, league="Legacy",
                    name="Trip", time=datetime.datetime(2016, 1, 5, 19, 28, 19)))
db.session.add(Post(uid=135, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=158, c2_number=136, league="Legacy",
                    name="Easy Sweep", time=datetime.datetime(2016, 6, 10, 21, 50, 17)))
db.session.add(
    Post(uid=136, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=162, c2_number=251, league="Legacy",
         name="Natural Mess", time=datetime.datetime(2016, 7, 23, 21, 22, 44)))
db.session.add(
    Post(uid=137, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=278, c2_number=283, league="Legacy",
         name="Troubadour", time=datetime.datetime(2016, 5, 24, 5, 58, 15)))
db.session.add(
    Post(uid=138, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=112, c2_number=27, league="Legacy",
         name="Electric Player", time=datetime.datetime(2016, 6, 15, 16, 13, 16)))
db.session.add(Post(uid=139, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=251, c2_number=271,
                    league="Legacy", name="Necromancer", time=datetime.datetime(2016, 11, 16, 19, 16, 41)))
db.session.add(
    Post(uid=140, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=290, c2_number=132, league="Legacy",
         name="Turnip King", time=datetime.datetime(2016, 12, 23, 18, 23, 37)))
db.session.add(
    Post(uid=141, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=273, c2_number=64, league="Legacy",
         name="Esquire", time=datetime.datetime(2016, 12, 19, 17, 25, 2)))
db.session.add(
    Post(uid=142, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=254, c2_number=132, league="Legacy",
         name="Neophyte Believer", time=datetime.datetime(2016, 2, 7, 17, 56, 2)))
db.session.add(
    Post(uid=143, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=162, c2_number=181, league="Legacy",
         name="Twitch", time=datetime.datetime(2016, 12, 25, 10, 29, 39)))
db.session.add(
    Post(uid=144, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=221, c2_number=280, league="Legacy",
         name="Fast Draw", time=datetime.datetime(2016, 6, 12, 22, 49, 22)))
db.session.add(
    Post(uid=145, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=32, c2_number=269, league="Legacy",
         name="Nessie", time=datetime.datetime(2016, 10, 19, 11, 34, 5)))
db.session.add(
    Post(uid=146, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=250, c2_number=83, league="Legacy",
         name="Vagabond Warrior", time=datetime.datetime(2016, 4, 24, 12, 3, 33)))
db.session.add(
    Post(uid=147, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=105, c2_number=38, league="Legacy",
         name="Flakes", time=datetime.datetime(2016, 11, 22, 10, 11, 4)))
db.session.add(
    Post(uid=148, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=173, c2_number=239, league="Legacy",
         name="New Cycle", time=datetime.datetime(2016, 1, 14, 18, 26, 46)))
db.session.add(
    Post(uid=149, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=163, c2_number=77, league="Legacy",
         name="Voluntary", time=datetime.datetime(2016, 7, 21, 21, 18, 35)))
db.session.add(
    Post(uid=150, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=136, c2_number=55, league="Legacy",
         name="Flint", time=datetime.datetime(2016, 1, 9, 3, 26, 41)))
db.session.add(
    Post(uid=151, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=300, c2_number=312, league="Legacy",
         name="Nickname Master", time=datetime.datetime(2016, 1, 23, 15, 0, 30)))
db.session.add(
    Post(uid=152, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=206, c2_number=286, league="Legacy",
         name="Vortex", time=datetime.datetime(2016, 8, 15, 7, 14, 16)))
db.session.add(Post(uid=153, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=229, c2_number=212, league="Legacy",
                    name="Freak", time=datetime.datetime(2016, 6, 24, 11, 15, 42)))
db.session.add(
    Post(uid=154, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=68, c2_number=148, league="Legacy",
         name="Nightmare King", time=datetime.datetime(2016, 6, 23, 16, 52, 39)))
db.session.add(
    Post(uid=155, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=51, c2_number=225, league="Legacy",
         name="Washer", time=datetime.datetime(2016, 7, 11, 19, 45, 49)))
db.session.add(
    Post(uid=156, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=186, c2_number=22, league="Legacy",
         name="Gas Man", time=datetime.datetime(2016, 2, 18, 3, 28, 3)))
db.session.add(Post(uid=157, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=27, c2_number=137,
                    league="Legacy", name="Night Train", time=datetime.datetime(2016, 8, 11, 16, 34, 36)))
db.session.add(
    Post(uid=158, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=308, c2_number=225, league="Legacy",
         name="Waylay Dave", time=datetime.datetime(2016, 12, 9, 3, 50, 29)))
db.session.add(
    Post(uid=159, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=174, c2_number=113, league="Legacy",
         name="Glyph", time=datetime.datetime(2016, 7, 14, 22, 4, 54)))
db.session.add(
    Post(uid=160, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=149, c2_number=165, league="Legacy",
         name="Old Man Winter", time=datetime.datetime(2016, 1, 10, 20, 13, 12)))
db.session.add(
    Post(uid=161, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=228, c2_number=297, league="Legacy",
         name="Wheels", time=datetime.datetime(2016, 2, 22, 18, 2, 29)))
db.session.add(
    Post(uid=162, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=144, c2_number=168, league="Legacy",
         name="Grave Digger", time=datetime.datetime(2016, 12, 14, 18, 51, 4)))
db.session.add(
    Post(uid=163, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=134, c2_number=105, league="Legacy",
         name="Old Orange Eyes", time=datetime.datetime(2016, 6, 13, 6, 55, 17)))
db.session.add(
    Post(uid=164, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=301, c2_number=199, league="Legacy",
         name="Wooden Man", time=datetime.datetime(2016, 4, 21, 22, 15, 45)))
db.session.add(
    Post(uid=165, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=114, c2_number=85, league="Legacy",
         name="Guillotine", time=datetime.datetime(2016, 1, 17, 11, 44, 19)))
db.session.add(
    Post(uid=166, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=157, c2_number=288, league="Legacy",
         name="Old Regret", time=datetime.datetime(2016, 9, 1, 16, 13, 24)))
db.session.add(
    Post(uid=167, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=32, c2_number=123, league="Legacy",
         name="Woo Woo", time=datetime.datetime(2016, 9, 24, 7, 12, 17)))
db.session.add(
    Post(uid=168, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=124, c2_number=164, league="Legacy",
         name="Gunhawk", time=datetime.datetime(2016, 9, 17, 16, 22, 18)))
db.session.add(
    Post(uid=169, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=305, c2_number=204, league="Legacy",
         name="Onion King", time=datetime.datetime(2016, 10, 1, 12, 52, 14)))
db.session.add(
    Post(uid=170, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=319, c2_number=40, league="Legacy",
         name="Yellow Menace", time=datetime.datetime(2016, 9, 22, 17, 33, 58)))
db.session.add(
    Post(uid=171, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=97, c2_number=242, league="Legacy",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 5, 2, 4, 39, 22)))
db.session.add(
    Post(uid=172, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=130, c2_number=243, league="Legacy",
         name="Osprey", time=datetime.datetime(2016, 3, 5, 10, 58, 35)))
db.session.add(
    Post(uid=173, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=102, c2_number=308, league="Legacy",
         name="Zero Charisma", time=datetime.datetime(2016, 2, 22, 7, 29, 31)))
db.session.add(Post(uid=174, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=297, c2_number=195, league="Legacy",
                    name="Highlander Monk", time=datetime.datetime(2016, 10, 24, 4, 47, 38)))
db.session.add(
    Post(uid=175, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=35, c2_number=301, league="Legacy",
         name="Overrun", time=datetime.datetime(2016, 1, 20, 5, 57, 52)))
db.session.add(Post(uid=176, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=60, c2_number=216, league="Legacy",
                    name="Zesty Dragon", time=datetime.datetime(2016, 6, 2, 12, 6, 24)))
db.session.add(
    Post(uid=177, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=291, c2_number=317, league="Legacy",
         name="Zod", time=datetime.datetime(2016, 3, 17, 15, 38, 5)))
db.session.add(
    Post(uid=0, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=115, c2_number=298, league="Legacy", name="101",
         time=datetime.datetime(2016, 5, 23, 1, 39, 15)))
db.session.add(Post(uid=1, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=241, c2_number=227, league="Legacy",
                    name="Houston", time=datetime.datetime(2016, 12, 2, 19, 46, 27)))
db.session.add(
    Post(uid=2, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=173, c2_number=300, league="Legacy",
         name="Pinball Wizard", time=datetime.datetime(2016, 4, 21, 11, 11, 27)))
db.session.add(Post(uid=3, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=90, c2_number=29, league="Legacy",
                    name="Accidental Genius", time=datetime.datetime(2016, 3, 3, 3, 48, 11)))
db.session.add(Post(uid=4, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=164, c2_number=177, league="Legacy",
                    name="Hyper", time=datetime.datetime(2016, 2, 2, 21, 31, 1)))
db.session.add(
    Post(uid=5, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=35, c2_number=98, league="Legacy",
         name="Pluto", time=datetime.datetime(2016, 10, 12, 6, 34, 24)))
db.session.add(Post(uid=6, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=266, c2_number=97, league="Legacy",
                    name="Alpha", time=datetime.datetime(2016, 12, 4, 17, 38, 25)))
db.session.add(Post(uid=7, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=208, c2_number=27, league="Legacy",
                    name="Jester", time=datetime.datetime(2016, 11, 10, 19, 39, 10)))
db.session.add(Post(uid=8, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=144, c2_number=284, league="Legacy",
                    name="Pogue", time=datetime.datetime(2016, 9, 3, 9, 30, 11)))
db.session.add(
    Post(uid=9, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=305, c2_number=195, league="Legacy",
         name="Airport Hobo", time=datetime.datetime(2016, 9, 27, 10, 28, 16)))
db.session.add(
    Post(uid=10, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=162, c2_number=198, league="Legacy", name="Jigsaw",
         time=datetime.datetime(2016, 11, 10, 13, 12, 33)))
db.session.add(Post(uid=11, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=288, c2_number=120, league="Legacy",
                    name="Prometheus", time=datetime.datetime(2016, 8, 23, 22, 32, 51)))
db.session.add(Post(uid=12, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=199, c2_number=261, league="Legacy",
                    name="Bearded Angler", time=datetime.datetime(2016, 12, 20, 18, 39, 31)))
db.session.add(Post(uid=13, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=307, c2_number=164, league="Legacy",
                    name="Joker's Grin", time=datetime.datetime(2016, 8, 25, 13, 4, 50)))
db.session.add(Post(uid=14, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=105, c2_number=170, league="Legacy",
                    name="Psycho Thinker", time=datetime.datetime(2016, 12, 3, 9, 35, 54)))
db.session.add(
    Post(uid=15, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=222, c2_number=56, league="Legacy",
         name="Beetle King", time=datetime.datetime(2016, 6, 17, 21, 54, 55)))
db.session.add(
    Post(uid=16, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=144, c2_number=63, league="Legacy", name="Judge",
         time=datetime.datetime(2016, 10, 2, 0, 49, 55)))
db.session.add(Post(uid=17, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=151, c2_number=193, league="Legacy",
                    name="Pusher", time=datetime.datetime(2016, 11, 28, 11, 27, 14)))
db.session.add(
    Post(uid=18, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=58, c2_number=166, league="Legacy", name="Bitmap",
         time=datetime.datetime(2016, 3, 14, 19, 9, 36)))
db.session.add(Post(uid=19, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=54, c2_number=31, league="Legacy",
                    name="Junkyard Dog", time=datetime.datetime(2016, 11, 1, 8, 12, 37)))
db.session.add(
    Post(uid=20, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=67, c2_number=222, league="Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 8, 13, 5, 2, 34)))
db.session.add(Post(uid=21, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=155, c2_number=84, league="Legacy",
                    name="Blister", time=datetime.datetime(2016, 6, 5, 9, 49, 10)))
db.session.add(Post(uid=22, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=104, c2_number=168, league="Legacy",
                    name="K-9", time=datetime.datetime(2016, 2, 27, 7, 17, 17)))
db.session.add(
    Post(uid=23, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=311, c2_number=245, league="Legacy",
         name="Roadblock", time=datetime.datetime(2016, 1, 24, 1, 2, 58)))
db.session.add(Post(uid=24, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=163, c2_number=77, league="Legacy",
                    name="Bowie", time=datetime.datetime(2016, 6, 12, 15, 3, 30)))
db.session.add(Post(uid=25, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=121, c2_number=231, league="Legacy",
                    name="Keystone", time=datetime.datetime(2016, 9, 17, 9, 13, 9)))
db.session.add(Post(uid=26, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=49, c2_number=140, league="Legacy",
                    name="Rooster", time=datetime.datetime(2016, 6, 17, 10, 1, 21)))
db.session.add(Post(uid=27, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=27, c2_number=74, league="Legacy",
                    name="Bowler", time=datetime.datetime(2016, 2, 16, 7, 47, 54)))
db.session.add(
    Post(uid=28, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=94, c2_number=23, league="Legacy", name="Kickstart",
         time=datetime.datetime(2016, 7, 3, 18, 28, 26)))
db.session.add(
    Post(uid=29, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=102, c2_number=126, league="Legacy", name="Sandbox",
         time=datetime.datetime(2016, 12, 26, 14, 23, 27)))
db.session.add(Post(uid=30, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=279, c2_number=143, league="Legacy",
                    name="Breadmaker", time=datetime.datetime(2016, 10, 6, 14, 35, 20)))
db.session.add(Post(uid=31, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=100, c2_number=177, league="Legacy",
                    name="Kill Switch", time=datetime.datetime(2016, 5, 2, 2, 45, 19)))
db.session.add(
    Post(uid=32, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=63, c2_number=152, league="Legacy",
         name="Scrapper", time=datetime.datetime(2016, 8, 17, 0, 53, 40)))
db.session.add(
    Post(uid=33, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=203, c2_number=45, league="Legacy",
         name="Broomspun", time=datetime.datetime(2016, 7, 16, 4, 48, 47)))
db.session.add(Post(uid=34, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=128, c2_number=22, league="Legacy",
                    name="Kingfisher", time=datetime.datetime(2016, 2, 1, 1, 42, 37)))
db.session.add(
    Post(uid=35, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=37, c2_number=313, league="Legacy",
         name="Screwtape", time=datetime.datetime(2016, 7, 8, 20, 8, 46)))
db.session.add(
    Post(uid=36, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=224, c2_number=276, league="Legacy",
         name="Buckshot", time=datetime.datetime(2016, 1, 14, 9, 14, 41)))
db.session.add(
    Post(uid=37, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=232, c2_number=59, league="Legacy",
         name="Kitchen", time=datetime.datetime(2016, 8, 19, 10, 48, 54)))
db.session.add(
    Post(uid=38, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=105, c2_number=276, league="Legacy",
         name="Sexual Chocolate", time=datetime.datetime(2016, 4, 23, 7, 58, 16)))
db.session.add(
    Post(uid=39, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=21, c2_number=230, league="Legacy",
         name="Bugger", time=datetime.datetime(2016, 9, 23, 15, 33, 7)))
db.session.add(
    Post(uid=40, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=139, c2_number=111, league="Legacy",
         name="Knuckles", time=datetime.datetime(2016, 6, 23, 14, 8, 22)))
db.session.add(
    Post(uid=41, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=204, c2_number=39, league="Legacy",
         name="Shadow Chaser", time=datetime.datetime(2016, 7, 25, 4, 15, 55)))
db.session.add(
    Post(uid=42, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=270, c2_number=39, league="Legacy",
         name="Cabbie", time=datetime.datetime(2016, 9, 5, 9, 44, 32)))
db.session.add(
    Post(uid=43, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=290, c2_number=260, league="Legacy",
         name="Lady Killer", time=datetime.datetime(2016, 3, 4, 18, 30, 15)))
db.session.add(
    Post(uid=44, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=213, c2_number=219, league="Legacy",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 7, 11, 13, 13, 14)))
db.session.add(
    Post(uid=45, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=222, c2_number=150, league="Legacy",
         name="Candy Butcher", time=datetime.datetime(2016, 5, 13, 15, 57, 43)))
db.session.add(Post(uid=46, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=273, c2_number=221, league="Legacy",
                    name="Liquid Science", time=datetime.datetime(2016, 7, 5, 5, 12, 4)))
db.session.add(Post(uid=47, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=212, c2_number=90, league="Legacy",
                    name="Shooter", time=datetime.datetime(2016, 12, 23, 7, 25, 9)))
db.session.add(
    Post(uid=48, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=260, c2_number=143, league="Legacy",
         name="Capital F", time=datetime.datetime(2016, 6, 6, 20, 46, 14)))
db.session.add(
    Post(uid=49, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=237, c2_number=198, league="Legacy",
         name="Little Cobra", time=datetime.datetime(2016, 4, 4, 22, 25, 3)))
db.session.add(Post(uid=50, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=135, c2_number=87, league="Legacy",
                    name="Sidewalk Enforcer", time=datetime.datetime(2016, 12, 1, 6, 14, 44)))
db.session.add(
    Post(uid=51, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=173, c2_number=63, league="Legacy",
         name="Captain Peroxide", time=datetime.datetime(2016, 7, 2, 21, 55, 54)))
db.session.add(Post(uid=52, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=32, c2_number=105, league="Legacy",
                    name="Little General", time=datetime.datetime(2016, 9, 22, 4, 46, 36)))
db.session.add(
    Post(uid=53, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=115, c2_number=258, league="Legacy",
         name="Skull Crusher", time=datetime.datetime(2016, 10, 27, 2, 42, 35)))
db.session.add(Post(uid=54, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=109, c2_number=236, league="Legacy",
                    name="Celtic Charger", time=datetime.datetime(2016, 8, 19, 2, 30, 6)))
db.session.add(Post(uid=55, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=239, c2_number=249, league="Legacy",
                    name="Lord Nikon", time=datetime.datetime(2016, 6, 23, 6, 12, 54)))
db.session.add(
    Post(uid=56, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=165, c2_number=40, league="Legacy",
         name="Sky Bully", time=datetime.datetime(2016, 5, 12, 6, 1, 22)))
db.session.add(
    Post(uid=57, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=262, c2_number=82, league="Legacy",
         name="Cereal Killer", time=datetime.datetime(2016, 4, 16, 13, 47, 29)))
db.session.add(
    Post(uid=58, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=54, c2_number=75, league="Legacy",
         name="Lord Pistachio", time=datetime.datetime(2016, 8, 23, 7, 19, 45)))
db.session.add(
    Post(uid=59, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=216, c2_number=36, league="Legacy",
         name="Slow Trot", time=datetime.datetime(2016, 8, 25, 21, 25, 42)))
db.session.add(
    Post(uid=60, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=129, c2_number=240, league="Legacy",
         name="Chicago Blackout", time=datetime.datetime(2016, 6, 10, 19, 15, 7)))
db.session.add(
    Post(uid=61, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=297, c2_number=201, league="Legacy",
         name="Mad Irishman", time=datetime.datetime(2016, 11, 13, 1, 24, 23)))
db.session.add(
    Post(uid=62, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=245, c2_number=123, league="Legacy",
         name="Snake Eyes", time=datetime.datetime(2016, 4, 24, 11, 34, 18)))
db.session.add(
    Post(uid=63, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=118, c2_number=85, league="Legacy",
         name="Chocolate Thunder", time=datetime.datetime(2016, 4, 22, 21, 52, 55)))
db.session.add(Post(uid=64, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=304, c2_number=101, league="Legacy",
                    name="Mad Jack", time=datetime.datetime(2016, 5, 16, 18, 44, 47)))
db.session.add(Post(uid=65, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=235, c2_number=144, league="Legacy",
                    name="Snow Hound", time=datetime.datetime(2016, 11, 14, 7, 50, 54)))
db.session.add(
    Post(uid=66, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=284, c2_number=312, league="Legacy",
         name="Chuckles", time=datetime.datetime(2016, 8, 23, 11, 5, 42)))
db.session.add(Post(uid=67, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=212, c2_number=281, league="Legacy",
                    name="Mad Rascal", time=datetime.datetime(2016, 9, 20, 7, 46, 42)))
db.session.add(
    Post(uid=68, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=86, c2_number=115, league="Hardcore Legacy",
         name="Sofa King", time=datetime.datetime(2016, 10, 27, 3, 14, 48)))
db.session.add(Post(uid=69, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=191, c2_number=133,
                    league="Hardcore Legacy", name="Commando", time=datetime.datetime(2016, 4, 22, 15, 41, 33)))
db.session.add(
    Post(uid=70, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=66, c2_number=172, league="Hardcore Legacy",
         name="Manimal", time=datetime.datetime(2016, 3, 14, 1, 31, 8)))
db.session.add(
    Post(uid=71, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=181, c2_number=292, league="Hardcore Legacy",
         name="Speedwell", time=datetime.datetime(2016, 4, 20, 6, 43, 37)))
db.session.add(
    Post(uid=72, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=279, c2_number=267, league="Hardcore Legacy",
         name="Cool Whip", time=datetime.datetime(2016, 4, 11, 9, 25, 37)))
db.session.add(
    Post(uid=73, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=65, c2_number=139, league="Hardcore Legacy",
         name="Marbles", time=datetime.datetime(2016, 5, 1, 9, 34, 21)))
db.session.add(Post(uid=74, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=143, c2_number=181,
                    league="Hardcore Legacy", name="Spider Fuji", time=datetime.datetime(2016, 3, 21, 19, 37, 11)))
db.session.add(
    Post(uid=75, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=76, c2_number=91, league="Hardcore Legacy",
         name="Cosmo", time=datetime.datetime(2016, 5, 21, 12, 3, 31)))
db.session.add(Post(uid=76, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=255, c2_number=229,
                    league="Hardcore Legacy", name="Married Man", time=datetime.datetime(2016, 6, 6, 4, 29, 7)))
db.session.add(Post(uid=77, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=277, c2_number=80,
                    league="Hardcore Legacy", name="Springheel Jack", time=datetime.datetime(2016, 10, 27, 7, 18, 51)))
db.session.add(
    Post(uid=78, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=277, c2_number=294, league="Hardcore Legacy",
         name="Crash Override", time=datetime.datetime(2016, 12, 6, 9, 32, 23)))
db.session.add(
    Post(uid=79, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=90, c2_number=108, league="Hardcore Legacy",
         name="Marshmallow", time=datetime.datetime(2016, 4, 28, 6, 12, 56)))
db.session.add(
    Post(uid=80, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=129, c2_number=128, league="Hardcore Legacy",
         name="Squatch", time=datetime.datetime(2016, 9, 25, 3, 43, 25)))
db.session.add(Post(uid=81, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=172, c2_number=96,
                    league="Hardcore Legacy", name="Crash Test", time=datetime.datetime(2016, 5, 5, 22, 38, 9)))
db.session.add(
    Post(uid=82, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=147, c2_number=309, league="Hardcore Legacy",
         name="Mental", time=datetime.datetime(2016, 9, 19, 8, 48, 45)))
db.session.add(
    Post(uid=83, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=193, c2_number=233, league="Hardcore Legacy",
         name="Stacker of Wheat", time=datetime.datetime(2016, 7, 23, 4, 27, 14)))
db.session.add(
    Post(uid=84, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=272, c2_number=289, league="Hardcore Legacy",
         name="Crazy Eights", time=datetime.datetime(2016, 5, 15, 21, 11, 1)))
db.session.add(
    Post(uid=85, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=199, c2_number=218, league="Hardcore Legacy",
         name="Mercury Reborn", time=datetime.datetime(2016, 7, 27, 11, 10, 43)))
db.session.add(Post(uid=86, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=269, c2_number=171,
                    league="Hardcore Legacy", name="Sugar Man", time=datetime.datetime(2016, 6, 1, 5, 4, 31)))
db.session.add(
    Post(uid=87, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=108, c2_number=264,
         league="Hardcore Legacy", name="Criss Cross", time=datetime.datetime(2016, 5, 16, 13, 56, 32)))
db.session.add(Post(uid=88, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=176, c2_number=124,
                    league="Hardcore Legacy", name="Midas", time=datetime.datetime(2016, 1, 2, 19, 55, 7)))
db.session.add(Post(uid=89, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=203, c2_number=105,
                    league="Hardcore Legacy", name="Suicide Jockey", time=datetime.datetime(2016, 2, 15, 20, 10, 36)))
db.session.add(Post(uid=90, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=222, c2_number=315,
                    league="Hardcore Legacy", name="Cross Thread", time=datetime.datetime(2016, 4, 23, 21, 10, 46)))
db.session.add(Post(uid=91, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=202, c2_number=157,
                    league="Hardcore Legacy", name="Midnight Rambler", time=datetime.datetime(2016, 1, 28, 9, 36, 17)))
db.session.add(Post(uid=92, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=83, c2_number=132,
                    league="Hardcore Legacy", name="Swampmasher", time=datetime.datetime(2016, 8, 4, 0, 19, 4)))
db.session.add(Post(uid=93, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=127, c2_number=281,
                    league="Hardcore Legacy", name="Cujo", time=datetime.datetime(2016, 11, 1, 7, 21, 25)))
db.session.add(Post(uid=94, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=159, c2_number=76,
                    league="Hardcore Legacy", name="Midnight Rider", time=datetime.datetime(2016, 2, 11, 21, 40, 49)))
db.session.add(Post(uid=95, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=288, c2_number=142,
                    league="Hardcore Legacy", name="Swerve", time=datetime.datetime(2016, 10, 17, 18, 28, 5)))
db.session.add(Post(uid=96, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=21, c2_number=128,
                    league="Hardcore Legacy", name="Dancing Madman", time=datetime.datetime(2016, 12, 8, 17, 27, 14)))
db.session.add(Post(uid=97, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=142, c2_number=309,
                    league="Hardcore Legacy", name="Mindless Bobcat", time=datetime.datetime(2016, 6, 3, 22, 52, 12)))
db.session.add(Post(uid=98, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=266, c2_number=211,
                    league="Hardcore Legacy", name="Tacklebox", time=datetime.datetime(2016, 11, 22, 7, 24, 7)))
db.session.add(Post(uid=99, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=298, c2_number=275,
                    league="Hardcore Legacy", name="Dangle", time=datetime.datetime(2016, 9, 6, 11, 18, 38)))
db.session.add(Post(uid=100, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=220, c2_number=210,
                    league="Hardcore Legacy", name="Mr. 44", time=datetime.datetime(2016, 2, 11, 17, 3, 21)))
db.session.add(Post(uid=101, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=67, c2_number=144,
                    league="Hardcore Legacy", name="Take Away", time=datetime.datetime(2016, 1, 16, 15, 26, 36)))
db.session.add(Post(uid=102, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=53, c2_number=231,
                    league="Hardcore Legacy", name="Dark Horse", time=datetime.datetime(2016, 5, 16, 9, 1, 1)))
db.session.add(Post(uid=103, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=212, c2_number=220,
                    league="Hardcore Legacy", name="Mr. Fabulous", time=datetime.datetime(2016, 9, 12, 5, 7, 20)))
db.session.add(
    Post(uid=104, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=46, c2_number=81, league="Hardcore Legacy",
         name="Tan Stallion", time=datetime.datetime(2016, 4, 12, 13, 41, 37)))
db.session.add(Post(uid=105, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=32, c2_number=210,
                    league="Hardcore Legacy", name="Day Hawk", time=datetime.datetime(2016, 2, 17, 0, 30, 35)))
db.session.add(
    Post(uid=106, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=163, c2_number=77, league="Hardcore Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 6, 12, 8, 55, 3)))
db.session.add(
    Post(uid=107, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=245, c2_number=308, league="Hardcore Legacy",
         name="The China Wall", time=datetime.datetime(2016, 4, 12, 0, 58, 8)))
db.session.add(
    Post(uid=108, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=224, c2_number=40, league="Hardcore Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 9, 18, 5, 1, 17)))
db.session.add(
    Post(uid=109, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=267, c2_number=117, league="Hardcore Legacy",
         name="Mr. Lucky", time=datetime.datetime(2016, 3, 2, 2, 23, 6)))
db.session.add(Post(uid=110, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=250, c2_number=302,
                    league="Hardcore Legacy", name="The Dude", time=datetime.datetime(2016, 2, 26, 22, 17, 39)))
db.session.add(
    Post(uid=111, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=222, c2_number=248, league="Hardcore Legacy",
         name="Digger", time=datetime.datetime(2016, 11, 27, 12, 34, 41)))
db.session.add(
    Post(uid=112, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=175, c2_number=224, league="Hardcore Legacy",
         name="Mr. Peppermint", time=datetime.datetime(2016, 3, 5, 0, 57, 45)))
db.session.add(Post(uid=113, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=286, c2_number=47,
                    league="Hardcore Legacy", name="The Flying Mouse", time=datetime.datetime(2016, 12, 2, 1, 26, 44)))
db.session.add(
    Post(uid=114, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=303, c2_number=227, league="Hardcore Legacy",
         name="Disco Thunder", time=datetime.datetime(2016, 6, 13, 21, 22, 43)))
db.session.add(
    Post(uid=115, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=62, c2_number=92, league="Hardcore Legacy",
         name="Mr. Spy", time=datetime.datetime(2016, 7, 5, 1, 4, 46)))
db.session.add(
    Post(uid=116, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=191, c2_number=291, league="Hardcore Legacy",
         name="The Happy Jock", time=datetime.datetime(2016, 12, 8, 22, 55, 1)))
db.session.add(Post(uid=117, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=224, c2_number=143,
                    league="Hardcore Legacy", name="Disco Potato", time=datetime.datetime(2016, 7, 9, 21, 5, 52)))
db.session.add(
    Post(uid=118, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=185, c2_number=63, league="Hardcore Legacy",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 7, 2, 3, 23, 46)))
db.session.add(
    Post(uid=119, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=307, c2_number=171, league="Hardcore Legacy",
         name="The Howling Swede", time=datetime.datetime(2016, 8, 27, 5, 1, 28)))
db.session.add(
    Post(uid=120, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=300, c2_number=37, league="Hardcore Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 1, 17, 8, 31, 25)))
db.session.add(
    Post(uid=121, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=156, c2_number=186, league="Hardcore Legacy",
         name="Mr. Wholesome", time=datetime.datetime(2016, 9, 25, 18, 0, 2)))
db.session.add(Post(uid=122, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=135, c2_number=258,
                    league="Hardcore Legacy", name="Thrasher", time=datetime.datetime(2016, 10, 12, 3, 35, 33)))
db.session.add(Post(uid=123, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=90, c2_number=300,
                    league="Hardcore Legacy", name="Dredd", time=datetime.datetime(2016, 3, 11, 3, 20, 38)))
db.session.add(
    Post(uid=124, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=298, c2_number=178, league="Hardcore Legacy",
         name="Mud Pie Man", time=datetime.datetime(2016, 7, 4, 2, 6, 46)))
db.session.add(Post(uid=125, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=221, c2_number=178,
                    league="Hardcore Legacy", name="Toe", time=datetime.datetime(2016, 6, 3, 21, 0, 42)))
db.session.add(
    Post(uid=126, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=273, c2_number=265, league="Hardcore Legacy",
         name="Dropkick", time=datetime.datetime(2016, 4, 27, 4, 37, 34)))
db.session.add(Post(uid=127, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=140, c2_number=105,
                    league="Hardcore Legacy", name="Mule Skinner", time=datetime.datetime(2016, 6, 5, 17, 29, 13)))
db.session.add(Post(uid=128, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=259, c2_number=186,
                    league="Hardcore Legacy", name="Toolmaker", time=datetime.datetime(2016, 10, 28, 14, 46, 5)))
db.session.add(Post(uid=129, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=92, c2_number=229,
                    league="Hardcore Legacy", name="Drop Stone", time=datetime.datetime(2016, 1, 21, 22, 54, 8)))
db.session.add(Post(uid=130, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=175, c2_number=234,
                    league="Hardcore Legacy", name="Murmur", time=datetime.datetime(2016, 6, 28, 21, 6, 40)))
db.session.add(Post(uid=131, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=72, c2_number=307,
                    league="Hardcore Legacy", name="Tough Nut", time=datetime.datetime(2016, 11, 13, 8, 13, 18)))
db.session.add(Post(uid=132, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=129, c2_number=180,
                    league="Hardcore Legacy", name="Drugstore Cowboy", time=datetime.datetime(2016, 6, 8, 7, 21, 15)))
db.session.add(Post(uid=133, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=38, c2_number=211,
                    league="Hardcore Legacy", name="Nacho", time=datetime.datetime(2016, 3, 19, 13, 41, 49)))
db.session.add(Post(uid=134, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=118, c2_number=95,
                    league="Hardcore Legacy", name="Trip", time=datetime.datetime(2016, 5, 15, 7, 33, 46)))
db.session.add(Post(uid=135, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=183, c2_number=221,
                    league="Hardcore Legacy", name="Easy Sweep", time=datetime.datetime(2016, 10, 8, 8, 19, 45)))
db.session.add(
    Post(uid=136, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=38, c2_number=142, league="Hardcore Legacy",
         name="Natural Mess", time=datetime.datetime(2016, 4, 2, 1, 13, 38)))
db.session.add(
    Post(uid=137, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=302, c2_number=253, league="Hardcore Legacy",
         name="Troubadour", time=datetime.datetime(2016, 4, 17, 16, 52, 52)))
db.session.add(Post(uid=138, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=34, c2_number=144,
                    league="Hardcore Legacy", name="Electric Player", time=datetime.datetime(2016, 2, 12, 11, 46, 6)))
db.session.add(Post(uid=139, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=201, c2_number=111,
                    league="Hardcore Legacy", name="Necromancer", time=datetime.datetime(2016, 7, 17, 12, 51, 5)))
db.session.add(
    Post(uid=140, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=314, c2_number=90, league="Hardcore Legacy",
         name="Turnip King", time=datetime.datetime(2016, 12, 21, 3, 8, 2)))
db.session.add(Post(uid=141, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=110, c2_number=250,
                    league="Hardcore Legacy", name="Esquire", time=datetime.datetime(2016, 11, 16, 15, 11, 36)))
db.session.add(
    Post(uid=142, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=85, c2_number=317, league="Hardcore Legacy",
         name="Neophyte Believer", time=datetime.datetime(2016, 1, 13, 14, 14, 25)))
db.session.add(
    Post(uid=143, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=302, c2_number=305, league="Hardcore Legacy",
         name="Twitch", time=datetime.datetime(2016, 1, 15, 3, 32, 46)))
db.session.add(
    Post(uid=144, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=35, c2_number=112, league="Hardcore Legacy",
         name="Fast Draw", time=datetime.datetime(2016, 8, 15, 17, 32, 7)))
db.session.add(
    Post(uid=145, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=204, c2_number=310, league="Hardcore Legacy",
         name="Nessie", time=datetime.datetime(2016, 2, 28, 9, 14, 35)))
db.session.add(Post(uid=146, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=140, c2_number=156,
                    league="Hardcore Legacy", name="Vagabond Warrior", time=datetime.datetime(2016, 2, 20, 6, 57, 40)))
db.session.add(Post(uid=147, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=312, c2_number=102,
                    league="Hardcore Legacy", name="Flakes", time=datetime.datetime(2016, 12, 14, 4, 55, 48)))
db.session.add(
    Post(uid=148, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=41, c2_number=187, league="Hardcore Legacy",
         name="New Cycle", time=datetime.datetime(2016, 2, 23, 4, 3, 36)))
db.session.add(Post(uid=149, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=236, c2_number=63,
                    league="Hardcore Legacy", name="Voluntary", time=datetime.datetime(2016, 12, 6, 15, 18, 14)))
db.session.add(
    Post(uid=150, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=147, c2_number=224, league="Hardcore Legacy",
         name="Flint", time=datetime.datetime(2016, 10, 28, 19, 17, 3)))
db.session.add(
    Post(uid=151, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=162, c2_number=287, league="Hardcore Legacy",
         name="Nickname Master", time=datetime.datetime(2016, 4, 10, 2, 40, 0)))
db.session.add(
    Post(uid=152, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=93, c2_number=105, league="Hardcore Legacy",
         name="Vortex", time=datetime.datetime(2016, 4, 18, 16, 13, 29)))
db.session.add(Post(uid=153, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=228, c2_number=165,
                    league="Hardcore Legacy", name="Freak", time=datetime.datetime(2016, 6, 19, 0, 8, 29)))
db.session.add(
    Post(uid=154, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=178, c2_number=30, league="Hardcore Legacy",
         name="Nightmare King", time=datetime.datetime(2016, 5, 23, 10, 52, 30)))
db.session.add(
    Post(uid=155, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=33, c2_number=313, league="Hardcore Legacy",
         name="Washer", time=datetime.datetime(2016, 7, 25, 7, 0, 20)))
db.session.add(
    Post(uid=156, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=311, c2_number=165, league="Hardcore Legacy",
         name="Gas Man", time=datetime.datetime(2016, 8, 4, 1, 30, 30)))
db.session.add(
    Post(uid=157, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=52, c2_number=71, league="Hardcore Legacy",
         name="Night Train", time=datetime.datetime(2016, 11, 2, 16, 32, 39)))
db.session.add(
    Post(uid=158, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=177, c2_number=42, league="Hardcore Legacy",
         name="Waylay Dave", time=datetime.datetime(2016, 2, 24, 5, 20, 19)))
db.session.add(Post(uid=159, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=86, c2_number=159,
                    league="Hardcore Legacy", name="Glyph", time=datetime.datetime(2016, 11, 28, 2, 14, 33)))
db.session.add(
    Post(uid=160, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=299, c2_number=120, league="Hardcore Legacy",
         name="Old Man Winter", time=datetime.datetime(2016, 2, 13, 11, 22, 45)))
db.session.add(
    Post(uid=161, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=298, c2_number=52, league="Hardcore Legacy",
         name="Wheels", time=datetime.datetime(2016, 9, 12, 0, 47, 15)))
db.session.add(
    Post(uid=162, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=263, c2_number=82, league="Hardcore Legacy",
         name="Grave Digger", time=datetime.datetime(2016, 3, 19, 18, 35, 23)))
db.session.add(
    Post(uid=163, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=106, c2_number=314, league="Hardcore Legacy",
         name="Old Orange Eyes", time=datetime.datetime(2016, 9, 17, 15, 30, 30)))
db.session.add(Post(uid=164, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=48, c2_number=176,
                    league="Hardcore Legacy", name="Wooden Man", time=datetime.datetime(2016, 12, 1, 2, 26, 39)))
db.session.add(Post(uid=165, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=139, c2_number=34,
                    league="Hardcore Legacy", name="Guillotine", time=datetime.datetime(2016, 8, 16, 0, 11, 19)))
db.session.add(Post(uid=166, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=216, c2_number=73,
                    league="Hardcore Legacy", name="Old Regret", time=datetime.datetime(2016, 7, 10, 6, 43, 44)))
db.session.add(Post(uid=167, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=214, c2_number=141,
                    league="Hardcore Legacy", name="Woo Woo", time=datetime.datetime(2016, 9, 10, 16, 0, 52)))
db.session.add(Post(uid=168, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=315, c2_number=131,
                    league="Hardcore Legacy", name="Gunhawk", time=datetime.datetime(2016, 5, 27, 2, 40, 2)))
db.session.add(
    Post(uid=169, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=224, c2_number=65, league="Hardcore Legacy",
         name="Onion King", time=datetime.datetime(2016, 4, 3, 1, 38, 39)))
db.session.add(Post(uid=170, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=120, c2_number=105,
                    league="Hardcore Legacy", name="Yellow Menace", time=datetime.datetime(2016, 7, 18, 19, 51, 3)))
db.session.add(Post(uid=171, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=62, c2_number=38,
                    league="Hardcore Legacy", name="High Kingdom Warrior",
                    time=datetime.datetime(2016, 5, 12, 18, 54, 5)))
db.session.add(
    Post(uid=172, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=182, c2_number=261, league="Hardcore Legacy",
         name="Osprey", time=datetime.datetime(2016, 7, 16, 12, 34, 36)))
db.session.add(
    Post(uid=173, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=308, c2_number=49, league="Hardcore Legacy",
         name="Zero Charisma", time=datetime.datetime(2016, 7, 15, 5, 29, 48)))
db.session.add(Post(uid=174, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=258, c2_number=256,
                    league="Hardcore Legacy", name="Highlander Monk", time=datetime.datetime(2016, 3, 4, 22, 28, 12)))
db.session.add(
    Post(uid=175, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=76, c2_number=243, league="Hardcore Legacy",
         name="Overrun", time=datetime.datetime(2016, 5, 13, 13, 51, 12)))
db.session.add(Post(uid=176, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=70, c2_number=99,
                    league="Hardcore Legacy", name="Zesty Dragon", time=datetime.datetime(2016, 7, 24, 17, 40, 6)))
db.session.add(Post(uid=177, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=66, c2_number=28,
                    league="Hardcore Legacy", name="Zod", time=datetime.datetime(2016, 7, 22, 17, 29, 1)))
db.session.add(
    Post(uid=0, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=37, c2_number=278, league="Hardcore Legacy",
         name="101", time=datetime.datetime(2016, 12, 21, 22, 2, 36)))
db.session.add(Post(uid=1, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=98, c2_number=134,
                    league="Hardcore Legacy", name="Houston", time=datetime.datetime(2016, 12, 8, 5, 38, 48)))
db.session.add(Post(uid=2, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=261, c2_number=280,
                    league="Hardcore Legacy", name="Pinball Wizard", time=datetime.datetime(2016, 10, 15, 17, 27, 55)))
db.session.add(Post(uid=3, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=89, c2_number=84,
                    league="Hardcore Legacy", name="Accidental Genius",
                    time=datetime.datetime(2016, 8, 21, 16, 23, 54)))
db.session.add(Post(uid=4, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=33, c2_number=296,
                    league="Hardcore Legacy", name="Hyper", time=datetime.datetime(2016, 1, 28, 2, 12, 1)))
db.session.add(Post(uid=5, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=182, c2_number=240,
                    league="Hardcore Legacy", name="Pluto", time=datetime.datetime(2016, 8, 7, 0, 30, 45)))
db.session.add(Post(uid=6, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=241, c2_number=44,
                    league="Hardcore Legacy", name="Alpha", time=datetime.datetime(2016, 3, 6, 4, 42, 48)))
db.session.add(Post(uid=7, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=152, c2_number=298,
                    league="Hardcore Legacy", name="Jester", time=datetime.datetime(2016, 7, 21, 18, 1, 55)))
db.session.add(Post(uid=8, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=224, c2_number=47,
                    league="Hardcore Legacy", name="Pogue", time=datetime.datetime(2016, 9, 3, 6, 27, 42)))
db.session.add(Post(uid=9, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=88, c2_number=192,
                    league="Hardcore Legacy", name="Airport Hobo", time=datetime.datetime(2016, 9, 3, 8, 27, 45)))
db.session.add(Post(uid=10, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=162, c2_number=72,
                    league="Hardcore Legacy", name="Jigsaw", time=datetime.datetime(2016, 7, 23, 10, 47, 20)))
db.session.add(Post(uid=11, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=232, c2_number=304,
                    league="Hardcore Legacy", name="Prometheus", time=datetime.datetime(2016, 5, 16, 16, 58, 0)))
db.session.add(Post(uid=12, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=263, c2_number=281,
                    league="Hardcore Legacy", name="Bearded Angler", time=datetime.datetime(2016, 3, 17, 20, 12, 7)))
db.session.add(
    Post(uid=13, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=84, c2_number=265, league="Hardcore Legacy",
         name="Joker's Grin", time=datetime.datetime(2016, 6, 10, 19, 45, 52)))
db.session.add(Post(uid=14, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=100, c2_number=260,
                    league="Hardcore Legacy", name="Psycho Thinker", time=datetime.datetime(2016, 8, 21, 20, 33, 23)))
db.session.add(Post(uid=15, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=173, c2_number=109,
                    league="Hardcore Legacy", name="Beetle King", time=datetime.datetime(2016, 2, 14, 9, 11, 16)))
db.session.add(
    Post(uid=16, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=82, c2_number=28, league="Hardcore Legacy",
         name="Judge", time=datetime.datetime(2016, 7, 28, 7, 4, 27)))
db.session.add(Post(uid=17, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=138, c2_number=190,
                    league="Hardcore Legacy", name="Pusher", time=datetime.datetime(2016, 12, 9, 5, 1, 30)))
db.session.add(
    Post(uid=18, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=25, c2_number=287, league="Hardcore Legacy",
         name="Bitmap", time=datetime.datetime(2016, 5, 10, 3, 52, 24)))
db.session.add(Post(uid=19, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=182, c2_number=49,
                    league="Hardcore Legacy", name="Junkyard Dog", time=datetime.datetime(2016, 12, 6, 14, 34, 45)))
db.session.add(
    Post(uid=20, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=39, c2_number=288, league="Hardcore Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 6, 13, 20, 57, 28)))
db.session.add(
    Post(uid=21, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=61, c2_number=179, league="Hardcore Legacy",
         name="Blister", time=datetime.datetime(2016, 4, 24, 21, 53, 54)))
db.session.add(Post(uid=22, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=301, c2_number=39,
                    league="Hardcore Legacy", name="K-9", time=datetime.datetime(2016, 10, 2, 0, 4, 6)))
db.session.add(Post(uid=23, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=172, c2_number=41,
                    league="Hardcore Legacy", name="Roadblock", time=datetime.datetime(2016, 8, 9, 21, 28, 43)))
db.session.add(Post(uid=24, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=165, c2_number=83,
                    league="Hardcore Legacy", name="Bowie", time=datetime.datetime(2016, 11, 16, 3, 29, 50)))
db.session.add(Post(uid=25, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=256, c2_number=54,
                    league="Hardcore Legacy", name="Keystone", time=datetime.datetime(2016, 2, 10, 10, 13, 47)))
db.session.add(Post(uid=26, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=299, c2_number=194,
                    league="Hardcore Legacy", name="Rooster", time=datetime.datetime(2016, 4, 18, 14, 17, 24)))
db.session.add(Post(uid=27, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=76, c2_number=294,
                    league="Hardcore Legacy", name="Bowler", time=datetime.datetime(2016, 12, 26, 21, 20, 36)))
db.session.add(Post(uid=28, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=39, c2_number=250,
                    league="Hardcore Legacy", name="Kickstart", time=datetime.datetime(2016, 8, 9, 5, 51, 44)))
db.session.add(Post(uid=29, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=147, c2_number=174,
                    league="Hardcore Legacy", name="Sandbox", time=datetime.datetime(2016, 7, 1, 3, 27, 28)))
db.session.add(
    Post(uid=30, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=241, c2_number=255, league="Hardcore Legacy",
         name="Breadmaker", time=datetime.datetime(2016, 3, 16, 19, 43, 21)))
db.session.add(
    Post(uid=31, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=317, c2_number=293, league="Hardcore Legacy",
         name="Kill Switch", time=datetime.datetime(2016, 11, 19, 6, 57, 13)))
db.session.add(Post(uid=32, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=99, c2_number=272,
                    league="Hardcore Legacy", name="Scrapper", time=datetime.datetime(2016, 1, 22, 14, 19, 28)))
db.session.add(Post(uid=33, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=104, c2_number=132,
                    league="Hardcore Legacy", name="Broomspun", time=datetime.datetime(2016, 6, 9, 3, 47, 52)))
db.session.add(Post(uid=34, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=295, c2_number=242,
                    league="Hardcore Legacy", name="Kingfisher", time=datetime.datetime(2016, 9, 25, 2, 55, 0)))
db.session.add(Post(uid=35, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=299, c2_number=86,
                    league="Hardcore Legacy", name="Screwtape", time=datetime.datetime(2016, 5, 27, 20, 36, 14)))
db.session.add(
    Post(uid=36, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=79, c2_number=239, league="Hardcore Legacy",
         name="Buckshot", time=datetime.datetime(2016, 9, 11, 1, 43, 48)))
db.session.add(Post(uid=37, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=183, c2_number=24,
                    league="Hardcore Legacy", name="Kitchen", time=datetime.datetime(2016, 4, 6, 4, 23, 34)))
db.session.add(
    Post(uid=38, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=108, c2_number=217, league="Hardcore Legacy",
         name="Sexual Chocolate", time=datetime.datetime(2016, 1, 25, 8, 56, 58)))
db.session.add(Post(uid=39, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=307, c2_number=285,
                    league="Hardcore Legacy", name="Bugger", time=datetime.datetime(2016, 11, 2, 13, 31, 50)))
db.session.add(Post(uid=40, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=187, c2_number=64,
                    league="Hardcore Legacy", name="Knuckles", time=datetime.datetime(2016, 6, 17, 0, 43, 42)))
db.session.add(Post(uid=41, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=147, c2_number=319,
                    league="Hardcore Legacy", name="Shadow Chaser", time=datetime.datetime(2016, 6, 2, 7, 17, 32)))
db.session.add(Post(uid=42, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=284, c2_number=130,
                    league="Hardcore Legacy", name="Cabbie", time=datetime.datetime(2016, 5, 2, 1, 20, 13)))
db.session.add(Post(uid=43, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=86, c2_number=46,
                    league="Hardcore Legacy", name="Lady Killer", time=datetime.datetime(2016, 4, 9, 7, 31, 13)))
db.session.add(Post(uid=44, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=268, c2_number=180,
                    league="Hardcore Legacy", name="Sherwood Gladiator",
                    time=datetime.datetime(2016, 8, 24, 13, 39, 47)))
db.session.add(Post(uid=45, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=172, c2_number=179,
                    league="Hardcore Legacy", name="Candy Butcher", time=datetime.datetime(2016, 9, 27, 1, 20, 27)))
db.session.add(Post(uid=46, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=118, c2_number=293,
                    league="Hardcore Legacy", name="Liquid Science", time=datetime.datetime(2016, 4, 18, 2, 11, 5)))
db.session.add(Post(uid=47, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=262, c2_number=112,
                    league="Hardcore Legacy", name="Shooter", time=datetime.datetime(2016, 10, 16, 11, 57, 25)))
db.session.add(
    Post(uid=48, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=106, c2_number=279, league="Hardcore Legacy",
         name="Capital F", time=datetime.datetime(2016, 4, 2, 10, 37, 30)))
db.session.add(
    Post(uid=49, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=222, c2_number=191, league="Hardcore Legacy",
         name="Little Cobra", time=datetime.datetime(2016, 11, 24, 14, 22, 25)))
db.session.add(Post(uid=50, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=275, c2_number=21,
                    league="Hardcore Legacy", name="Sidewalk Enforcer", time=datetime.datetime(2016, 9, 4, 20, 34, 50)))
db.session.add(
    Post(uid=51, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=45, c2_number=271, league="Hardcore Legacy",
         name="Captain Peroxide", time=datetime.datetime(2016, 5, 16, 14, 29, 48)))
db.session.add(Post(uid=52, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=127, c2_number=198,
                    league="Hardcore Legacy", name="Little General", time=datetime.datetime(2016, 7, 28, 5, 12, 43)))
db.session.add(Post(uid=53, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=270, c2_number=178,
                    league="Hardcore Legacy", name="Skull Crusher", time=datetime.datetime(2016, 2, 13, 20, 49, 23)))
db.session.add(Post(uid=54, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=283, c2_number=256,
                    league="Hardcore Legacy", name="Celtic Charger", time=datetime.datetime(2016, 12, 5, 2, 30, 2)))
db.session.add(Post(uid=55, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=198, c2_number=237,
                    league="Hardcore Legacy", name="Lord Nikon", time=datetime.datetime(2016, 1, 7, 7, 39, 41)))
db.session.add(Post(uid=56, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=186, c2_number=294,
                    league="Hardcore Legacy", name="Sky Bully", time=datetime.datetime(2016, 2, 13, 17, 36, 32)))
db.session.add(Post(uid=57, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=289, c2_number=132,
                    league="Hardcore Legacy", name="Cereal Killer", time=datetime.datetime(2016, 10, 28, 14, 0, 29)))
db.session.add(Post(uid=58, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=71, c2_number=294,
                    league="Hardcore Legacy", name="Lord Pistachio", time=datetime.datetime(2016, 3, 24, 19, 22, 7)))
db.session.add(Post(uid=59, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=58, c2_number=179,
                    league="Hardcore Legacy", name="Slow Trot", time=datetime.datetime(2016, 5, 10, 18, 34, 56)))
db.session.add(Post(uid=60, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=261, c2_number=180,
                    league="Hardcore Legacy", name="Chicago Blackout", time=datetime.datetime(2016, 3, 22, 17, 38, 37)))
db.session.add(Post(uid=61, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=145, c2_number=121,
                    league="Hardcore Legacy", name="Mad Irishman", time=datetime.datetime(2016, 12, 9, 15, 11, 43)))
db.session.add(Post(uid=62, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=272, c2_number=220,
                    league="Hardcore Legacy", name="Snake Eyes", time=datetime.datetime(2016, 8, 23, 12, 11, 14)))
db.session.add(Post(uid=63, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=79, c2_number=83,
                    league="Hardcore Legacy", name="Chocolate Thunder", time=datetime.datetime(2016, 10, 18, 1, 1, 41)))
db.session.add(Post(uid=64, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=21, c2_number=210,
                    league="Hardcore Legacy", name="Mad Jack", time=datetime.datetime(2016, 6, 9, 17, 5, 39)))
db.session.add(Post(uid=65, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=133, c2_number=255,
                    league="Hardcore Legacy", name="Snow Hound", time=datetime.datetime(2016, 10, 2, 0, 3, 25)))
db.session.add(Post(uid=66, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=185, c2_number=127,
                    league="Hardcore Legacy", name="Chuckles", time=datetime.datetime(2016, 6, 15, 7, 5, 28)))
db.session.add(
    Post(uid=67, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=273, c2_number=93, league="Hardcore Legacy",
         name="Mad Rascal", time=datetime.datetime(2016, 5, 7, 0, 3, 19)))
db.session.add(Post(uid=68, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=221, c2_number=184,
                    league="Hardcore Legacy", name="Sofa King", time=datetime.datetime(2016, 2, 19, 17, 19, 8)))
db.session.add(Post(uid=69, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=178, c2_number=223,
                    league="Hardcore Legacy", name="Commando", time=datetime.datetime(2016, 11, 28, 16, 40, 44)))
db.session.add(
    Post(uid=70, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=166, c2_number=257, league="Hardcore Legacy",
         name="Manimal", time=datetime.datetime(2016, 7, 6, 3, 11, 53)))
db.session.add(Post(uid=71, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=99, c2_number=175,
                    league="Hardcore Legacy", name="Speedwell", time=datetime.datetime(2016, 11, 15, 19, 52, 53)))
db.session.add(
    Post(uid=72, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=53, c2_number=91, league="Hardcore Legacy",
         name="Cool Whip", time=datetime.datetime(2016, 5, 4, 22, 34, 21)))
db.session.add(Post(uid=73, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=239, c2_number=268,
                    league="Hardcore Legacy", name="Marbles", time=datetime.datetime(2016, 5, 5, 11, 19, 17)))
db.session.add(
    Post(uid=74, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=255, c2_number=58, league="Hardcore Legacy",
         name="Spider Fuji", time=datetime.datetime(2016, 8, 6, 11, 50, 31)))
db.session.add(
    Post(uid=75, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=93, c2_number=235, league="Hardcore Legacy",
         name="Cosmo", time=datetime.datetime(2016, 3, 24, 16, 26, 7)))
db.session.add(Post(uid=76, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=286, c2_number=134,
                    league="Hardcore Legacy", name="Married Man", time=datetime.datetime(2016, 4, 21, 1, 1, 39)))
db.session.add(Post(uid=77, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=188, c2_number=149,
                    league="Hardcore Legacy", name="Springheel Jack", time=datetime.datetime(2016, 9, 15, 16, 19, 20)))
db.session.add(Post(uid=78, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=301, c2_number=305,
                    league="Hardcore Legacy", name="Crash Override", time=datetime.datetime(2016, 12, 26, 22, 57, 51)))
db.session.add(Post(uid=79, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=49, c2_number=234,
                    league="Hardcore Legacy", name="Marshmallow", time=datetime.datetime(2016, 4, 17, 15, 42, 11)))
db.session.add(Post(uid=80, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=134, c2_number=116,
                    league="Hardcore Legacy", name="Squatch", time=datetime.datetime(2016, 6, 17, 2, 32, 2)))
db.session.add(Post(uid=81, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=150, c2_number=211,
                    league="Hardcore Legacy", name="Crash Test", time=datetime.datetime(2016, 12, 21, 19, 1, 8)))
db.session.add(Post(uid=82, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=105, c2_number=253,
                    league="Hardcore Legacy", name="Mental", time=datetime.datetime(2016, 11, 7, 3, 1, 44)))
db.session.add(Post(uid=83, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=35, c2_number=96,
                    league="Hardcore Legacy", name="Stacker of Wheat",
                    time=datetime.datetime(2016, 10, 24, 22, 53, 44)))
db.session.add(
    Post(uid=84, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=45, c2_number=295, league="Hardcore Legacy",
         name="Crazy Eights", time=datetime.datetime(2016, 8, 28, 6, 40, 44)))
db.session.add(
    Post(uid=85, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=114, c2_number=192, league="Hardcore Legacy",
         name="Mercury Reborn", time=datetime.datetime(2016, 3, 8, 8, 5, 29)))
db.session.add(Post(uid=86, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=265, c2_number=231,
                    league="Hardcore Legacy", name="Sugar Man", time=datetime.datetime(2016, 11, 5, 22, 44, 17)))
db.session.add(
    Post(uid=87, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=255, c2_number=118, league="Hardcore Legacy",
         name="Criss Cross", time=datetime.datetime(2016, 3, 8, 3, 11, 41)))
db.session.add(
    Post(uid=88, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=240, c2_number=193, league="Hardcore Legacy",
         name="Midas", time=datetime.datetime(2016, 2, 18, 9, 19, 19)))
db.session.add(Post(uid=89, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=284, c2_number=297,
                    league="Hardcore Legacy", name="Suicide Jockey", time=datetime.datetime(2016, 1, 28, 17, 19, 52)))
db.session.add(
    Post(uid=90, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=236, c2_number=97, league="Hardcore Legacy",
         name="Cross Thread", time=datetime.datetime(2016, 11, 14, 20, 31, 25)))
db.session.add(Post(uid=91, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=304, c2_number=291,
                    league="Hardcore Legacy", name="Midnight Rambler", time=datetime.datetime(2016, 10, 5, 9, 52, 28)))
db.session.add(
    Post(uid=92, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=175, c2_number=199, league="Hardcore Legacy",
         name="Swampmasher", time=datetime.datetime(2016, 4, 1, 0, 25, 7)))
db.session.add(
    Post(uid=93, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=285, c2_number=150, league="Hardcore Legacy",
         name="Cujo", time=datetime.datetime(2016, 1, 4, 6, 37, 5)))
db.session.add(Post(uid=94, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=178, c2_number=284,
                    league="Hardcore Legacy", name="Midnight Rider", time=datetime.datetime(2016, 2, 8, 1, 0, 36)))
db.session.add(Post(uid=95, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=90, c2_number=77,
                    league="Hardcore Legacy", name="Swerve", time=datetime.datetime(2016, 8, 12, 7, 23, 3)))
db.session.add(Post(uid=96, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=222, c2_number=32,
                    league="Hardcore Legacy", name="Dancing Madman", time=datetime.datetime(2016, 2, 14, 2, 34, 30)))
db.session.add(Post(uid=97, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=66, c2_number=201,
                    league="Hardcore Legacy", name="Mindless Bobcat", time=datetime.datetime(2016, 2, 5, 18, 14, 58)))
db.session.add(Post(uid=98, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=134, c2_number=267,
                    league="Hardcore Legacy", name="Tacklebox", time=datetime.datetime(2016, 2, 9, 11, 48, 48)))
db.session.add(Post(uid=99, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=207, c2_number=120,
                    league="Hardcore Legacy", name="Dangle", time=datetime.datetime(2016, 8, 26, 14, 11, 50)))
db.session.add(Post(uid=100, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=122, c2_number=73,
                    league="Hardcore Legacy", name="Mr. 44", time=datetime.datetime(2016, 10, 4, 15, 21, 41)))
db.session.add(Post(uid=101, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=149, c2_number=217,
                    league="Hardcore Legacy", name="Take Away", time=datetime.datetime(2016, 7, 22, 19, 44, 28)))
db.session.add(
    Post(uid=102, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=289, c2_number=165, league="Hardcore Legacy",
         name="Dark Horse", time=datetime.datetime(2016, 2, 8, 0, 23, 10)))
db.session.add(
    Post(uid=103, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=25, c2_number=154, league="Hardcore Legacy",
         name="Mr. Fabulous", time=datetime.datetime(2016, 7, 18, 3, 55, 41)))
db.session.add(Post(uid=104, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=287, c2_number=188,
                    league="Hardcore Legacy", name="Tan Stallion", time=datetime.datetime(2016, 7, 9, 17, 41, 57)))
db.session.add(
    Post(uid=105, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=310, c2_number=96, league="Hardcore Legacy",
         name="Day Hawk", time=datetime.datetime(2016, 5, 7, 17, 18, 34)))
db.session.add(
    Post(uid=106, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=41, c2_number=174, league="Hardcore Legacy",
         name="Mr. Gadget", time=datetime.datetime(2016, 10, 2, 12, 48, 41)))
db.session.add(Post(uid=107, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=216, c2_number=294,
                    league="Hardcore Legacy", name="The China Wall", time=datetime.datetime(2016, 9, 24, 4, 2, 40)))
db.session.add(
    Post(uid=108, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=57, c2_number=195, league="Hardcore Legacy",
         name="Desert Haze", time=datetime.datetime(2016, 6, 16, 14, 30, 27)))
db.session.add(Post(uid=109, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=153, c2_number=184,
                    league="Hardcore Legacy", name="Mr. Lucky", time=datetime.datetime(2016, 4, 20, 16, 6, 53)))
db.session.add(
    Post(uid=110, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=59, c2_number=106, league="Hardcore Legacy",
         name="The Dude", time=datetime.datetime(2016, 10, 6, 12, 47, 30)))
db.session.add(
    Post(uid=111, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=35, c2_number=156, league="Hardcore Legacy",
         name="Digger", time=datetime.datetime(2016, 9, 16, 12, 32, 6)))
db.session.add(Post(uid=112, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=158, c2_number=103,
                    league="Hardcore Legacy", name="Mr. Peppermint", time=datetime.datetime(2016, 2, 4, 6, 57, 13)))
db.session.add(Post(uid=113, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=150, c2_number=45,
                    league="Hardcore Legacy", name="The Flying Mouse", time=datetime.datetime(2016, 8, 9, 10, 34, 11)))
db.session.add(Post(uid=114, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=225, c2_number=164,
                    league="Hardcore Legacy", name="Disco Thunder", time=datetime.datetime(2016, 9, 27, 21, 41, 39)))
db.session.add(Post(uid=115, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=135, c2_number=290,
                    league="Hardcore Legacy", name="Mr. Spy", time=datetime.datetime(2016, 8, 14, 5, 40, 24)))
db.session.add(Post(uid=116, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=251, c2_number=270,
                    league="Hardcore Legacy", name="The Happy Jock", time=datetime.datetime(2016, 2, 8, 8, 10, 49)))
db.session.add(Post(uid=117, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=96, c2_number=218,
                    league="Hardcore Legacy", name="Disco Potato", time=datetime.datetime(2016, 12, 16, 5, 0, 34)))
db.session.add(Post(uid=118, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=112, c2_number=216,
                    league="Hardcore Legacy", name="Mr. Thanksgiving", time=datetime.datetime(2016, 6, 4, 15, 25, 5)))
db.session.add(Post(uid=119, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=194, c2_number=177,
                    league="Hardcore Legacy", name="The Howling Swede", time=datetime.datetime(2016, 1, 10, 18, 8, 21)))
db.session.add(
    Post(uid=120, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=268, c2_number=109, league="Hardcore Legacy",
         name="Dr. Cocktail", time=datetime.datetime(2016, 1, 10, 1, 26, 48)))
db.session.add(
    Post(uid=121, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=199, c2_number=153, league="Hardcore Legacy",
         name="Mr. Wholesome", time=datetime.datetime(2016, 9, 13, 16, 55, 12)))
db.session.add(Post(uid=122, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=237, c2_number=23,
                    league="Hardcore Legacy", name="Thrasher", time=datetime.datetime(2016, 5, 14, 20, 27, 46)))
db.session.add(Post(uid=123, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=134, c2_number=262,
                    league="Hardcore Legacy", name="Dredd", time=datetime.datetime(2016, 2, 18, 12, 46, 29)))
db.session.add(Post(uid=124, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=77, c2_number=112,
                    league="Hardcore Legacy", name="Mud Pie Man", time=datetime.datetime(2016, 5, 27, 22, 23, 14)))
db.session.add(Post(uid=125, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=288, c2_number=274,
                    league="Hardcore Legacy", name="Toe", time=datetime.datetime(2016, 10, 1, 16, 19, 17)))
db.session.add(Post(uid=126, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=273, c2_number=147,
                    league="Hardcore Legacy", name="Dropkick", time=datetime.datetime(2016, 10, 21, 2, 13, 0)))
db.session.add(Post(uid=127, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=30, c2_number=240,
                    league="Hardcore Legacy", name="Mule Skinner", time=datetime.datetime(2016, 5, 8, 13, 6, 5)))
db.session.add(Post(uid=128, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=57, c2_number=298,
                    league="Hardcore Legacy", name="Toolmaker", time=datetime.datetime(2016, 8, 25, 4, 46, 15)))
db.session.add(Post(uid=129, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=297, c2_number=89,
                    league="Hardcore Legacy", name="Drop Stone", time=datetime.datetime(2016, 11, 12, 15, 51, 28)))
db.session.add(Post(uid=130, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=148, c2_number=39,
                    league="Hardcore Legacy", name="Murmur", time=datetime.datetime(2016, 6, 16, 13, 54, 44)))
db.session.add(Post(uid=131, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=69, c2_number=99,
                    league="Hardcore Legacy", name="Tough Nut", time=datetime.datetime(2016, 10, 3, 17, 30, 7)))
db.session.add(Post(uid=132, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=163, c2_number=264,
                    league="Hardcore Legacy", name="Drugstore Cowboy", time=datetime.datetime(2016, 7, 20, 8, 18, 49)))
db.session.add(Post(uid=133, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=192, c2_number=54,
                    league="Hardcore Legacy", name="Nacho", time=datetime.datetime(2016, 1, 27, 0, 38, 29)))
db.session.add(Post(uid=134, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=233, c2_number=294,
                    league="Hardcore Legacy", name="Trip", time=datetime.datetime(2016, 10, 20, 16, 54, 47)))
db.session.add(Post(uid=135, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=213, c2_number=94,
                    league="Hardcore Legacy", name="Easy Sweep", time=datetime.datetime(2016, 9, 21, 14, 37, 53)))
db.session.add(Post(uid=136, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=207, c2_number=33,
                    league="Hardcore Legacy", name="Natural Mess", time=datetime.datetime(2016, 9, 18, 15, 31, 50)))
db.session.add(Post(uid=137, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=80, c2_number=206,
                    league="Hardcore Legacy", name="Troubadour", time=datetime.datetime(2016, 10, 26, 8, 1, 8)))
db.session.add(
    Post(uid=138, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=99, c2_number=180, league="Hardcore Legacy",
         name="Electric Player", time=datetime.datetime(2016, 4, 12, 9, 10, 13)))
db.session.add(
    Post(uid=139, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=92, c2_number=20, league="Hardcore Legacy",
         name="Necromancer", time=datetime.datetime(2016, 8, 11, 11, 55, 9)))
db.session.add(Post(uid=140, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=134, c2_number=95,
                    league="Hardcore Legacy", name="Turnip King", time=datetime.datetime(2016, 4, 14, 10, 34, 33)))
db.session.add(Post(uid=141, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=140, c2_number=300,
                    league="Hardcore Legacy", name="Esquire", time=datetime.datetime(2016, 4, 10, 2, 26, 28)))
db.session.add(
    Post(uid=142, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=106, c2_number=121, league="Hardcore Legacy",
         name="Neophyte Believer", time=datetime.datetime(2016, 11, 26, 7, 31, 47)))
db.session.add(Post(uid=143, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=297, c2_number=294,
                    league="Hardcore Legacy", name="Twitch", time=datetime.datetime(2016, 4, 27, 4, 9, 57)))
db.session.add(
    Post(uid=144, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=118, c2_number=174, league="Hardcore Legacy",
         name="Fast Draw", time=datetime.datetime(2016, 1, 7, 19, 42, 52)))
db.session.add(
    Post(uid=145, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=161, c2_number=310, league="Hardcore Legacy",
         name="Nessie", time=datetime.datetime(2016, 1, 18, 17, 19, 11)))
db.session.add(
    Post(uid=146, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=318, c2_number=235, league="Hardcore Legacy",
         name="Vagabond Warrior", time=datetime.datetime(2016, 12, 13, 10, 49, 19)))
db.session.add(
    Post(uid=147, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=211, c2_number=248, league="Hardcore Legacy",
         name="Flakes", time=datetime.datetime(2016, 9, 22, 7, 25, 22)))
db.session.add(Post(uid=148, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=118, c2_number=270,
                    league="Hardcore Legacy", name="New Cycle", time=datetime.datetime(2016, 9, 1, 7, 14, 4)))
db.session.add(
    Post(uid=149, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=36, c2_number=318, league="Hardcore Legacy",
         name="Voluntary", time=datetime.datetime(2016, 3, 7, 20, 51, 0)))
db.session.add(
    Post(uid=150, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=60, c2_number=75, league="Hardcore Legacy",
         name="Flint", time=datetime.datetime(2016, 9, 3, 16, 3, 10)))
db.session.add(Post(uid=151, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=144, c2_number=28,
                    league="Hardcore Legacy", name="Nickname Master", time=datetime.datetime(2016, 1, 4, 4, 15, 57)))
db.session.add(
    Post(uid=152, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=309, c2_number=253, league="Hardcore Legacy",
         name="Vortex", time=datetime.datetime(2016, 7, 17, 3, 28, 35)))
db.session.add(
    Post(uid=153, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=319, c2_number=283, league="Hardcore Legacy",
         name="Freak", time=datetime.datetime(2016, 9, 11, 4, 25, 32)))
db.session.add(
    Post(uid=154, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=169, c2_number=199, league="Hardcore Legacy",
         name="Nightmare King", time=datetime.datetime(2016, 3, 2, 21, 46, 29)))
db.session.add(
    Post(uid=155, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=170, c2_number=98, league="Hardcore Legacy",
         name="Washer", time=datetime.datetime(2016, 11, 16, 3, 9, 19)))
db.session.add(
    Post(uid=156, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=111, c2_number=53, league="Hardcore Legacy",
         name="Gas Man", time=datetime.datetime(2016, 2, 1, 8, 39, 5)))
db.session.add(
    Post(uid=157, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=184, c2_number=144, league="Hardcore Legacy",
         name="Night Train", time=datetime.datetime(2016, 1, 20, 11, 8, 33)))
db.session.add(
    Post(uid=158, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=53, c2_number=152, league="Hardcore Legacy",
         name="Waylay Dave", time=datetime.datetime(2016, 4, 14, 6, 45, 50)))
db.session.add(
    Post(uid=159, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=106, c2_number=189, league="Hardcore Legacy",
         name="Glyph", time=datetime.datetime(2016, 2, 20, 7, 35, 54)))
db.session.add(
    Post(uid=160, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=306, c2_number=310, league="Hardcore Legacy",
         name="Old Man Winter", time=datetime.datetime(2016, 2, 13, 20, 19, 5)))
db.session.add(Post(uid=161, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=144, c2_number=239,
                    league="Hardcore Legacy", name="Wheels", time=datetime.datetime(2016, 3, 17, 6, 45, 32)))
db.session.add(
    Post(uid=162, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=52, c2_number=302, league="Hardcore Legacy",
         name="Grave Digger", time=datetime.datetime(2016, 12, 24, 9, 52, 46)))
db.session.add(
    Post(uid=163, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=149, c2_number=174, league="Hardcore Legacy",
         name="Old Orange Eyes", time=datetime.datetime(2016, 4, 22, 20, 32, 21)))
db.session.add(
    Post(uid=164, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=116, c2_number=116, league="Hardcore Legacy",
         name="Wooden Man", time=datetime.datetime(2016, 8, 23, 17, 16, 22)))
db.session.add(
    Post(uid=165, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=137, c2_number=304, league="Hardcore Legacy",
         name="Guillotine", time=datetime.datetime(2016, 10, 25, 6, 5, 2)))
db.session.add(Post(uid=166, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=187, c2_number=195,
                    league="Hardcore Legacy", name="Old Regret", time=datetime.datetime(2016, 10, 23, 20, 23, 5)))
db.session.add(
    Post(uid=167, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=229, c2_number=93, league="Hardcore Legacy",
         name="Woo Woo", time=datetime.datetime(2016, 1, 14, 7, 45, 33)))
db.session.add(
    Post(uid=168, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=49, c2_number=63, league="Hardcore Legacy",
         name="Gunhawk", time=datetime.datetime(2016, 1, 12, 22, 11, 51)))
db.session.add(Post(uid=169, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=166, c2_number=77,
                    league="Hardcore Legacy", name="Onion King", time=datetime.datetime(2016, 9, 13, 19, 29, 20)))
db.session.add(
    Post(uid=170, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=67, c2_number=125, league="Hardcore Legacy",
         name="Yellow Menace", time=datetime.datetime(2016, 11, 17, 3, 11, 46)))
db.session.add(
    Post(uid=171, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=204, c2_number=56, league="Hardcore Legacy",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 5, 19, 13, 38, 28)))
db.session.add(
    Post(uid=172, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=121, c2_number=251, league="Hardcore Legacy",
         name="Osprey", time=datetime.datetime(2016, 11, 17, 2, 29, 27)))
db.session.add(
    Post(uid=173, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=208, c2_number=244, league="Hardcore Legacy",
         name="Zero Charisma", time=datetime.datetime(2016, 9, 22, 14, 1, 27)))
db.session.add(
    Post(uid=174, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=181, c2_number=259, league="Hardcore Legacy",
         name="Highlander Monk", time=datetime.datetime(2016, 2, 11, 12, 54, 3)))
db.session.add(
    Post(uid=175, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=316, c2_number=98, league="Hardcore Legacy",
         name="Overrun", time=datetime.datetime(2016, 9, 23, 2, 8, 10)))
db.session.add(
    Post(uid=176, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=23, c2_number=198, league="Hardcore Legacy",
         name="Zesty Dragon", time=datetime.datetime(2016, 4, 11, 9, 19, 41)))
db.session.add(
    Post(uid=177, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=76, c2_number=158, league="Hardcore Legacy",
         name="Zod", time=datetime.datetime(2016, 1, 27, 11, 8, 16)))
db.session.add(
    Post(uid=0, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=298, c2_number=235, league="Hardcore Legacy",
         name="101", time=datetime.datetime(2016, 5, 11, 0, 28, 31)))
db.session.add(Post(uid=1, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=308, c2_number=130,
                    league="Hardcore Legacy", name="Houston", time=datetime.datetime(2016, 6, 13, 21, 36, 21)))
db.session.add(
    Post(uid=2, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=253, c2_number=108, league="Hardcore Legacy",
         name="Pinball Wizard", time=datetime.datetime(2016, 12, 8, 13, 0, 22)))
db.session.add(Post(uid=3, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=222, c2_number=206,
                    league="Hardcore Legacy", name="Accidental Genius", time=datetime.datetime(2016, 4, 2, 11, 54, 11)))
db.session.add(
    Post(uid=4, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=105, c2_number=277, league="Hardcore Legacy",
         name="Hyper", time=datetime.datetime(2016, 8, 11, 16, 52, 53)))
db.session.add(
    Post(uid=5, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=59, c2_number=175, league="Hardcore Legacy",
         name="Pluto", time=datetime.datetime(2016, 5, 15, 17, 53, 56)))
db.session.add(Post(uid=6, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=196, c2_number=97,
                    league="Hardcore Legacy", name="Alpha", time=datetime.datetime(2016, 4, 9, 0, 45, 5)))
db.session.add(Post(uid=7, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=24, c2_number=119,
                    league="Hardcore Legacy", name="Jester", time=datetime.datetime(2016, 3, 10, 6, 36, 28)))
db.session.add(Post(uid=8, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=102, c2_number=253,
                    league="Hardcore Legacy", name="Pogue", time=datetime.datetime(2016, 1, 15, 16, 57, 0)))
db.session.add(Post(uid=9, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=247, c2_number=84,
                    league="Hardcore Legacy", name="Airport Hobo", time=datetime.datetime(2016, 7, 4, 20, 46, 40)))
db.session.add(Post(uid=10, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=44, c2_number=317,
                    league="Hardcore Legacy", name="Jigsaw", time=datetime.datetime(2016, 10, 7, 13, 5, 26)))
db.session.add(Post(uid=11, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=293, c2_number=300,
                    league="Hardcore Legacy", name="Prometheus", time=datetime.datetime(2016, 12, 12, 16, 0, 45)))
db.session.add(Post(uid=12, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=148, c2_number=189,
                    league="Hardcore Legacy", name="Bearded Angler", time=datetime.datetime(2016, 4, 11, 10, 29, 13)))
db.session.add(Post(uid=13, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=25, c2_number=228,
                    league="Hardcore Legacy", name="Joker's Grin", time=datetime.datetime(2016, 4, 17, 13, 14, 36)))
db.session.add(
    Post(uid=14, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=30, c2_number=212, league="Hardcore Legacy",
         name="Psycho Thinker", time=datetime.datetime(2016, 4, 23, 18, 46, 34)))
db.session.add(
    Post(uid=15, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=236, c2_number=105, league="Hardcore Legacy",
         name="Beetle King", time=datetime.datetime(2016, 2, 4, 14, 2, 16)))
db.session.add(Post(uid=16, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=184, c2_number=222,
                    league="Hardcore Legacy", name="Judge", time=datetime.datetime(2016, 2, 23, 0, 1, 10)))
db.session.add(
    Post(uid=17, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=187, c2_number=170, league="Hardcore Legacy",
         name="Pusher", time=datetime.datetime(2016, 7, 5, 9, 0, 13)))
db.session.add(
    Post(uid=18, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=291, c2_number=250, league="Hardcore Legacy",
         name="Bitmap", time=datetime.datetime(2016, 10, 21, 2, 45, 52)))
db.session.add(Post(uid=19, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=143, c2_number=191,
                    league="Hardcore Legacy", name="Junkyard Dog", time=datetime.datetime(2016, 7, 28, 1, 45, 3)))
db.session.add(
    Post(uid=20, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=196, c2_number=243, league="Hardcore Legacy",
         name="Riff Raff", time=datetime.datetime(2016, 2, 26, 4, 47, 45)))
db.session.add(
    Post(uid=21, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=170, c2_number=175, league="Hardcore Legacy",
         name="Blister", time=datetime.datetime(2016, 5, 7, 6, 0, 39)))
db.session.add(
    Post(uid=22, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=87, c2_number=296, league="Hardcore Legacy",
         name="K-9", time=datetime.datetime(2016, 1, 1, 7, 48, 27)))
db.session.add(
    Post(uid=23, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=294, c2_number=82, league="Hardcore Legacy",
         name="Roadblock", time=datetime.datetime(2016, 8, 14, 7, 27, 54)))
db.session.add(Post(uid=24, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=222, c2_number=237,
                    league="Hardcore Legacy", name="Bowie", time=datetime.datetime(2016, 1, 17, 18, 40, 44)))
db.session.add(
    Post(uid=25, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=132, c2_number=24, league="Hardcore Legacy",
         name="Keystone", time=datetime.datetime(2016, 3, 2, 2, 15, 48)))
db.session.add(Post(uid=26, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=286, c2_number=140,
                    league="Hardcore Legacy", name="Rooster", time=datetime.datetime(2016, 8, 13, 10, 6, 27)))
db.session.add(Post(uid=27, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=120, c2_number=185,
                    league="Hardcore Legacy", name="Bowler", time=datetime.datetime(2016, 8, 19, 10, 11, 30)))
db.session.add(
    Post(uid=28, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=140, c2_number=63, league="Hardcore Legacy",
         name="Kickstart", time=datetime.datetime(2016, 11, 14, 20, 47, 45)))
db.session.add(
    Post(uid=29, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=87, c2_number=31, league="Hardcore Legacy",
         name="Sandbox", time=datetime.datetime(2016, 5, 27, 18, 29, 21)))
db.session.add(
    Post(uid=30, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=149, c2_number=317, league="Hardcore Legacy",
         name="Breadmaker", time=datetime.datetime(2016, 11, 11, 9, 28, 42)))
db.session.add(Post(uid=31, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=74, c2_number=152,
                    league="Hardcore Legacy", name="Kill Switch", time=datetime.datetime(2016, 2, 26, 12, 26, 52)))
db.session.add(
    Post(uid=32, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=142, c2_number=271, league="Hardcore Legacy",
         name="Scrapper", time=datetime.datetime(2016, 5, 4, 16, 35, 2)))
db.session.add(
    Post(uid=33, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=114, c2_number=69, league="Hardcore Legacy",
         name="Broomspun", time=datetime.datetime(2016, 5, 26, 17, 51, 56)))
db.session.add(
    Post(uid=34, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=72, c2_number=68, league="Hardcore Legacy",
         name="Kingfisher", time=datetime.datetime(2016, 4, 27, 12, 50, 44)))
db.session.add(
    Post(uid=35, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=251, c2_number=111, league="Hardcore Legacy",
         name="Screwtape", time=datetime.datetime(2016, 3, 25, 3, 48, 56)))
db.session.add(
    Post(uid=36, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=66, c2_number=255, league="Standard",
         name="Buckshot", time=datetime.datetime(2016, 3, 7, 17, 16, 30)))
db.session.add(Post(uid=37, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=240, c2_number=258,
                    league="Standard", name="Kitchen", time=datetime.datetime(2016, 8, 13, 8, 3, 32)))
db.session.add(Post(uid=38, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=225, c2_number=227, league="Standard",
                    name="Sexual Chocolate", time=datetime.datetime(2016, 5, 20, 14, 49, 32)))
db.session.add(
    Post(uid=39, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=230, c2_number=92, league="Standard",
         name="Bugger", time=datetime.datetime(2016, 7, 23, 9, 9, 52)))
db.session.add(Post(uid=40, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=76, c2_number=91, league="Standard",
                    name="Knuckles", time=datetime.datetime(2016, 9, 9, 10, 45, 29)))
db.session.add(
    Post(uid=41, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=93, c2_number=161, league="Standard",
         name="Shadow Chaser", time=datetime.datetime(2016, 2, 22, 3, 20, 23)))
db.session.add(
    Post(uid=42, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=20, c2_number=79, league="Standard",
         name="Cabbie", time=datetime.datetime(2016, 7, 18, 11, 4, 37)))
db.session.add(
    Post(uid=43, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=66, c2_number=210, league="Standard",
         name="Lady Killer", time=datetime.datetime(2016, 6, 25, 21, 43, 44)))
db.session.add(
    Post(uid=44, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=160, c2_number=181, league="Standard",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 9, 18, 12, 36, 35)))
db.session.add(
    Post(uid=45, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=138, c2_number=63, league="Standard",
         name="Candy Butcher", time=datetime.datetime(2016, 4, 13, 3, 53, 53)))
db.session.add(
    Post(uid=46, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=114, c2_number=168, league="Standard",
         name="Liquid Science", time=datetime.datetime(2016, 6, 20, 1, 3, 13)))
db.session.add(
    Post(uid=47, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=172, c2_number=296, league="Standard",
         name="Shooter", time=datetime.datetime(2016, 7, 10, 16, 18, 1)))
db.session.add(
    Post(uid=48, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=56, c2_number=154, league="Standard",
         name="Capital F", time=datetime.datetime(2016, 3, 7, 1, 51, 0)))
db.session.add(
    Post(uid=49, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=78, c2_number=49, league="Standard",
         name="Little Cobra", time=datetime.datetime(2016, 10, 9, 1, 17, 37)))
db.session.add(Post(uid=50, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=51, c2_number=81, league="Standard",
                    name="Sidewalk Enforcer", time=datetime.datetime(2016, 1, 4, 17, 38, 54)))
db.session.add(Post(uid=51, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=168, c2_number=286, league="Standard",
                    name="Captain Peroxide", time=datetime.datetime(2016, 2, 7, 2, 40, 34)))
db.session.add(
    Post(uid=52, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=261, c2_number=40, league="Standard",
         name="Little General", time=datetime.datetime(2016, 9, 3, 16, 56, 25)))
db.session.add(
    Post(uid=53, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=319, c2_number=73, league="Standard",
         name="Skull Crusher", time=datetime.datetime(2016, 3, 4, 10, 3, 56)))
db.session.add(Post(uid=54, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=145, c2_number=122,
                    league="Standard", name="Celtic Charger", time=datetime.datetime(2016, 12, 15, 15, 1, 45)))
db.session.add(
    Post(uid=55, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=274, c2_number=69,
         league="Standard", name="Lord Nikon", time=datetime.datetime(2016, 7, 4, 21, 12, 53)))
db.session.add(
    Post(uid=56, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=311, c2_number=236, league="Standard",
         name="Sky Bully", time=datetime.datetime(2016, 4, 4, 4, 22, 48)))
db.session.add(Post(uid=57, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=171, c2_number=46,
                    league="Standard", name="Cereal Killer", time=datetime.datetime(2016, 4, 1, 2, 32, 29)))
db.session.add(
    Post(uid=58, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=255, c2_number=57, league="Standard",
         name="Lord Pistachio", time=datetime.datetime(2016, 10, 11, 17, 57, 35)))
db.session.add(
    Post(uid=59, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=26, c2_number=289, league="Standard",
         name="Slow Trot", time=datetime.datetime(2016, 4, 23, 5, 3, 4)))
db.session.add(Post(uid=60, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=231, c2_number=127,
                    league="Standard", name="Chicago Blackout", time=datetime.datetime(2016, 4, 6, 7, 34, 40)))
db.session.add(Post(uid=61, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=94, c2_number=315,
                    league="Standard", name="Mad Irishman", time=datetime.datetime(2016, 4, 8, 2, 29, 20)))
db.session.add(Post(uid=62, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=113, c2_number=152,
                    league="Standard", name="Snake Eyes", time=datetime.datetime(2016, 1, 2, 10, 29, 9)))
db.session.add(Post(uid=63, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=108, c2_number=121,
                    league="Standard", name="Chocolate Thunder", time=datetime.datetime(2016, 6, 9, 22, 36, 50)))
db.session.add(Post(uid=64, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=84, c2_number=118,
                    league="Standard", name="Mad Jack", time=datetime.datetime(2016, 11, 22, 16, 39, 49)))
db.session.add(Post(uid=65, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=297, c2_number=55,
                    league="Standard", name="Snow Hound", time=datetime.datetime(2016, 11, 3, 7, 31, 25)))
db.session.add(Post(uid=66, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=264, c2_number=275,
                    league="Standard", name="Chuckles", time=datetime.datetime(2016, 12, 23, 5, 41, 48)))
db.session.add(Post(uid=67, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=29, c2_number=218,
                    league="Standard", name="Mad Rascal", time=datetime.datetime(2016, 9, 25, 19, 10, 0)))
db.session.add(
    Post(uid=68, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=21, c2_number=149, league="Standard",
         name="Sofa King", time=datetime.datetime(2016, 8, 17, 15, 7, 37)))
db.session.add(
    Post(uid=69, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=142, c2_number=70, league="Standard",
         name="Commando", time=datetime.datetime(2016, 12, 22, 11, 47, 48)))
db.session.add(Post(uid=70, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=92, c2_number=79,
                    league="Standard", name="Manimal", time=datetime.datetime(2016, 3, 2, 12, 7, 20)))
db.session.add(Post(uid=71, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=203, c2_number=260,
                    league="Standard", name="Speedwell", time=datetime.datetime(2016, 11, 2, 5, 25, 1)))
db.session.add(Post(uid=72, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=177, c2_number=143, league="Standard",
                    name="Cool Whip", time=datetime.datetime(2016, 11, 9, 6, 36, 42)))
db.session.add(
    Post(uid=73, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=92, c2_number=281, league="Standard",
         name="Marbles", time=datetime.datetime(2016, 12, 19, 4, 29, 29)))
db.session.add(Post(uid=74, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=186, c2_number=82, league="Standard",
                    name="Spider Fuji", time=datetime.datetime(2016, 5, 3, 21, 49, 31)))
db.session.add(
    Post(uid=75, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=22, c2_number=272, league="Standard",
         name="Cosmo", time=datetime.datetime(2016, 4, 7, 4, 14, 57)))
db.session.add(Post(uid=76, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=164, c2_number=41, league="Standard",
                    name="Married Man", time=datetime.datetime(2016, 2, 16, 11, 7, 58)))
db.session.add(Post(uid=77, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=255, c2_number=290, league="Standard",
                    name="Springheel Jack", time=datetime.datetime(2016, 10, 4, 18, 57, 10)))
db.session.add(
    Post(uid=78, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=273, c2_number=207, league="Standard",
         name="Crash Override", time=datetime.datetime(2016, 8, 18, 5, 9, 22)))
db.session.add(
    Post(uid=79, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=157, c2_number=170, league="Standard",
         name="Marshmallow", time=datetime.datetime(2016, 1, 16, 21, 6, 34)))
db.session.add(
    Post(uid=80, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=99, c2_number=118, league="Standard",
         name="Squatch", time=datetime.datetime(2016, 3, 14, 14, 44, 36)))
db.session.add(
    Post(uid=81, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=47, c2_number=123, league="Standard",
         name="Crash Test", time=datetime.datetime(2016, 8, 28, 19, 12, 48)))
db.session.add(
    Post(uid=82, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=316, c2_number=228, league="Standard",
         name="Mental", time=datetime.datetime(2016, 8, 21, 22, 27, 50)))
db.session.add(
    Post(uid=83, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=115, c2_number=190, league="Standard",
         name="Stacker of Wheat", time=datetime.datetime(2016, 2, 20, 15, 57, 29)))
db.session.add(
    Post(uid=84, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=217, c2_number=193, league="Standard",
         name="Crazy Eights", time=datetime.datetime(2016, 4, 2, 7, 2, 14)))
db.session.add(
    Post(uid=85, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=291, c2_number=290, league="Standard",
         name="Mercury Reborn", time=datetime.datetime(2016, 11, 6, 4, 13, 4)))
db.session.add(Post(uid=86, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=74, c2_number=274, league="Standard",
                    name="Sugar Man", time=datetime.datetime(2016, 1, 11, 8, 45, 4)))
db.session.add(Post(uid=87, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=154, c2_number=126, league="Standard",
                    name="Criss Cross", time=datetime.datetime(2016, 11, 17, 15, 30, 52)))
db.session.add(
    Post(uid=88, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=270, c2_number=219, league="Standard",
         name="Midas", time=datetime.datetime(2016, 2, 4, 11, 39, 1)))
db.session.add(Post(uid=89, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=27, c2_number=236, league="Standard",
                    name="Suicide Jockey", time=datetime.datetime(2016, 11, 19, 18, 11, 0)))
db.session.add(
    Post(uid=90, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=172, c2_number=238, league="Standard",
         name="Cross Thread", time=datetime.datetime(2016, 10, 14, 3, 34, 57)))
db.session.add(Post(uid=91, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=36, c2_number=62,
                    league="Standard", name="Midnight Rambler", time=datetime.datetime(2016, 11, 9, 9, 41, 5)))
db.session.add(
    Post(uid=92, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=231, c2_number=289, league="Standard",
         name="Swampmasher", time=datetime.datetime(2016, 10, 20, 1, 52, 55)))
db.session.add(
    Post(uid=93, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=174, c2_number=59, league="Standard",
         name="Cujo", time=datetime.datetime(2016, 8, 17, 13, 41, 12)))
db.session.add(
    Post(uid=94, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=127, c2_number=196, league="Standard",
         name="Midnight Rider", time=datetime.datetime(2016, 8, 28, 2, 17, 15)))
db.session.add(
    Post(uid=95, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=88, c2_number=92, league="Standard",
         name="Swerve", time=datetime.datetime(2016, 12, 7, 6, 31, 34)))
db.session.add(
    Post(uid=96, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=305, c2_number=123, league="Standard",
         name="Dancing Madman", time=datetime.datetime(2016, 4, 25, 12, 18, 44)))
db.session.add(
    Post(uid=97, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=28, c2_number=200, league="Standard",
         name="Mindless Bobcat", time=datetime.datetime(2016, 1, 9, 18, 34, 0)))
db.session.add(
    Post(uid=98, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=219, c2_number=138, league="Standard",
         name="Tacklebox", time=datetime.datetime(2016, 2, 5, 5, 15, 32)))
db.session.add(
    Post(uid=99, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=259, c2_number=184, league="Standard",
         name="Dangle", time=datetime.datetime(2016, 4, 18, 16, 23, 49)))
db.session.add(
    Post(uid=100, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=225, c2_number=218, league="Standard",
         name="Mr. 44", time=datetime.datetime(2016, 7, 28, 21, 40, 9)))
db.session.add(
    Post(uid=101, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=240, c2_number=54, league="Standard",
         name="Take Away", time=datetime.datetime(2016, 10, 21, 15, 50, 47)))
db.session.add(
    Post(uid=102, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=318, c2_number=243, league="Standard",
         name="Dark Horse", time=datetime.datetime(2016, 6, 17, 21, 49, 35)))
db.session.add(
    Post(uid=103, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=158, c2_number=202, league="Standard",
         name="Mr. Fabulous", time=datetime.datetime(2016, 8, 26, 7, 39, 55)))
db.session.add(
    Post(uid=104, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=83, c2_number=188, league="Standard",
         name="Tan Stallion", time=datetime.datetime(2016, 3, 10, 10, 30, 58)))
db.session.add(
    Post(uid=105, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=318, c2_number=235, league="Standard",
         name="Day Hawk", time=datetime.datetime(2016, 6, 2, 0, 19, 21)))
db.session.add(
    Post(uid=106, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=94, c2_number=306, league="Standard",
         name="Mr. Gadget", time=datetime.datetime(2016, 4, 7, 18, 48, 57)))
db.session.add(
    Post(uid=107, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=141, c2_number=305, league="Standard",
         name="The China Wall", time=datetime.datetime(2016, 4, 14, 13, 56, 22)))
db.session.add(
    Post(uid=108, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=196, c2_number=301, league="Standard",
         name="Desert Haze", time=datetime.datetime(2016, 2, 20, 13, 45, 16)))
db.session.add(
    Post(uid=109, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=42, c2_number=56, league="Standard",
         name="Mr. Lucky", time=datetime.datetime(2016, 9, 11, 18, 31, 49)))
db.session.add(Post(uid=110, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=41, c2_number=152, league="Standard",
                    name="The Dude", time=datetime.datetime(2016, 10, 3, 17, 8, 19)))
db.session.add(
    Post(uid=111, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=312, c2_number=300, league="Standard",
         name="Digger", time=datetime.datetime(2016, 1, 2, 9, 34, 38)))
db.session.add(
    Post(uid=112, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=178, c2_number=136, league="Standard",
         name="Mr. Peppermint", time=datetime.datetime(2016, 12, 6, 7, 37, 10)))
db.session.add(
    Post(uid=113, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=302, c2_number=158, league="Standard",
         name="The Flying Mouse", time=datetime.datetime(2016, 4, 20, 22, 52, 35)))
db.session.add(
    Post(uid=114, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=128, c2_number=197, league="Standard",
         name="Disco Thunder", time=datetime.datetime(2016, 2, 13, 17, 47, 34)))
db.session.add(
    Post(uid=115, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=49, c2_number=187, league="Standard",
         name="Mr. Spy", time=datetime.datetime(2016, 5, 10, 22, 51, 24)))
db.session.add(
    Post(uid=116, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=283, c2_number=260, league="Standard",
         name="The Happy Jock", time=datetime.datetime(2016, 4, 8, 15, 37, 45)))
db.session.add(
    Post(uid=117, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=39, c2_number=225, league="Standard",
         name="Disco Potato", time=datetime.datetime(2016, 2, 19, 17, 5, 47)))
db.session.add(
    Post(uid=118, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=309, c2_number=69, league="Standard",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 4, 17, 9, 19, 29)))
db.session.add(
    Post(uid=119, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=153, c2_number=217, league="Standard",
         name="The Howling Swede", time=datetime.datetime(2016, 12, 16, 2, 54, 27)))
db.session.add(
    Post(uid=120, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=100, c2_number=120, league="Standard",
         name="Dr. Cocktail", time=datetime.datetime(2016, 2, 11, 13, 25, 50)))
db.session.add(
    Post(uid=121, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=292, c2_number=263, league="Standard",
         name="Mr. Wholesome", time=datetime.datetime(2016, 2, 12, 16, 15, 27)))
db.session.add(Post(uid=122, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=140, c2_number=64, league="Standard",
                    name="Thrasher", time=datetime.datetime(2016, 10, 19, 21, 0, 3)))
db.session.add(Post(uid=123, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=148, c2_number=172, league="Standard",
                    name="Dredd", time=datetime.datetime(2016, 2, 4, 12, 47, 3)))
db.session.add(
    Post(uid=124, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=168, c2_number=305, league="Standard",
         name="Mud Pie Man", time=datetime.datetime(2016, 7, 13, 5, 33, 32)))
db.session.add(
    Post(uid=125, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=239, c2_number=59, league="Standard",
         name="Toe", time=datetime.datetime(2016, 6, 16, 2, 15, 42)))
db.session.add(
    Post(uid=126, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=214, c2_number=275, league="Standard",
         name="Dropkick", time=datetime.datetime(2016, 4, 20, 13, 22, 40)))
db.session.add(Post(uid=127, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=119, c2_number=97,
                    league="Standard", name="Mule Skinner", time=datetime.datetime(2016, 9, 1, 3, 20, 41)))
db.session.add(Post(uid=128, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=78, c2_number=88, league="Standard",
                    name="Toolmaker", time=datetime.datetime(2016, 8, 1, 22, 23, 3)))
db.session.add(
    Post(uid=129, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=262, c2_number=165, league="Standard",
         name="Drop Stone", time=datetime.datetime(2016, 11, 18, 8, 38, 15)))
db.session.add(
    Post(uid=130, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=42, c2_number=275, league="Standard",
         name="Murmur", time=datetime.datetime(2016, 2, 2, 20, 45, 23)))
db.session.add(
    Post(uid=131, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=295, c2_number=224, league="Standard",
         name="Tough Nut", time=datetime.datetime(2016, 8, 25, 16, 47, 43)))
db.session.add(
    Post(uid=132, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=191, c2_number=29, league="Standard",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 8, 25, 8, 33, 9)))
db.session.add(
    Post(uid=133, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=86, c2_number=69, league="Standard",
         name="Nacho", time=datetime.datetime(2016, 5, 7, 8, 26, 54)))
db.session.add(
    Post(uid=134, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=134, c2_number=42, league="Standard",
         name="Trip", time=datetime.datetime(2016, 9, 20, 5, 9, 53)))
db.session.add(
    Post(uid=135, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=317, c2_number=193, league="Standard",
         name="Easy Sweep", time=datetime.datetime(2016, 3, 15, 9, 22, 55)))
db.session.add(
    Post(uid=136, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=185, c2_number=51, league="Standard",
         name="Natural Mess", time=datetime.datetime(2016, 8, 4, 6, 3, 37)))
db.session.add(
    Post(uid=137, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=241, c2_number=155, league="Standard",
         name="Troubadour", time=datetime.datetime(2016, 10, 8, 13, 53, 12)))
db.session.add(
    Post(uid=138, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=277, c2_number=105, league="Standard",
         name="Electric Player", time=datetime.datetime(2016, 4, 16, 2, 24, 18)))
db.session.add(
    Post(uid=139, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=147, c2_number=202, league="Standard",
         name="Necromancer", time=datetime.datetime(2016, 5, 25, 17, 28, 32)))
db.session.add(
    Post(uid=140, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=103, c2_number=126, league="Standard",
         name="Turnip King", time=datetime.datetime(2016, 12, 5, 17, 4, 48)))
db.session.add(Post(uid=141, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=88, c2_number=202, league="Standard",
                    name="Esquire", time=datetime.datetime(2016, 4, 6, 16, 42, 40)))
db.session.add(
    Post(uid=142, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=133, c2_number=214, league="Standard",
         name="Neophyte Believer", time=datetime.datetime(2016, 3, 14, 5, 18, 38)))
db.session.add(
    Post(uid=143, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=62, c2_number=218, league="Standard",
         name="Twitch", time=datetime.datetime(2016, 3, 12, 16, 25, 27)))
db.session.add(
    Post(uid=144, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=283, c2_number=50, league="Standard",
         name="Fast Draw", time=datetime.datetime(2016, 8, 26, 11, 16, 37)))
db.session.add(Post(uid=145, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=165, c2_number=43,
                    league="Standard", name="Nessie", time=datetime.datetime(2016, 10, 5, 7, 1, 53)))
db.session.add(
    Post(uid=146, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=198, c2_number=42, league="Standard",
         name="Vagabond Warrior", time=datetime.datetime(2016, 2, 16, 8, 11, 49)))
db.session.add(
    Post(uid=147, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=196, c2_number=267, league="Standard",
         name="Flakes", time=datetime.datetime(2016, 4, 7, 20, 53, 51)))
db.session.add(
    Post(uid=148, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=186, c2_number=81, league="Standard",
         name="New Cycle", time=datetime.datetime(2016, 12, 12, 1, 41, 12)))
db.session.add(
    Post(uid=149, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=41, c2_number=284, league="Standard",
         name="Voluntary", time=datetime.datetime(2016, 4, 19, 2, 35, 40)))
db.session.add(Post(uid=150, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=98, c2_number=125,
                    league="Standard", name="Flint", time=datetime.datetime(2016, 5, 27, 2, 35, 54)))
db.session.add(
    Post(uid=151, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=62, c2_number=193, league="Standard",
         name="Nickname Master", time=datetime.datetime(2016, 11, 8, 1, 15, 56)))
db.session.add(Post(uid=152, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=130, c2_number=149,
                    league="Standard", name="Vortex", time=datetime.datetime(2016, 5, 14, 1, 17, 47)))
db.session.add(Post(uid=153, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=87, c2_number=193,
                    league="Standard", name="Freak", time=datetime.datetime(2016, 12, 26, 2, 6, 10)))
db.session.add(
    Post(uid=154, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=38, c2_number=40, league="Standard",
         name="Nightmare King", time=datetime.datetime(2016, 5, 27, 17, 37, 29)))
db.session.add(
    Post(uid=155, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=271, c2_number=144, league="Standard",
         name="Washer", time=datetime.datetime(2016, 7, 17, 5, 20, 11)))
db.session.add(
    Post(uid=156, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=219, c2_number=291, league="Standard",
         name="Gas Man", time=datetime.datetime(2016, 5, 24, 5, 51, 11)))
db.session.add(Post(uid=157, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=189, c2_number=275,
                    league="Standard", name="Night Train", time=datetime.datetime(2016, 5, 22, 21, 29, 57)))
db.session.add(
    Post(uid=158, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=113, c2_number=184, league="Standard",
         name="Waylay Dave", time=datetime.datetime(2016, 2, 1, 1, 15, 52)))
db.session.add(
    Post(uid=159, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=234, c2_number=46, league="Standard",
         name="Glyph", time=datetime.datetime(2016, 3, 24, 22, 36, 44)))
db.session.add(
    Post(uid=160, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=299, c2_number=317, league="Standard",
         name="Old Man Winter", time=datetime.datetime(2016, 6, 24, 11, 9, 36)))
db.session.add(
    Post(uid=161, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=210, c2_number=179, league="Standard",
         name="Wheels", time=datetime.datetime(2016, 10, 8, 10, 20, 43)))
db.session.add(
    Post(uid=162, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=232, c2_number=308, league="Standard",
         name="Grave Digger", time=datetime.datetime(2016, 2, 17, 16, 46, 25)))
db.session.add(Post(uid=163, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=275, c2_number=179,
                    league="Standard", name="Old Orange Eyes", time=datetime.datetime(2016, 12, 24, 9, 0, 7)))
db.session.add(
    Post(uid=164, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=260, c2_number=119, league="Standard",
         name="Wooden Man", time=datetime.datetime(2016, 3, 9, 8, 57, 16)))
db.session.add(
    Post(uid=165, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=28, c2_number=36, league="Standard",
         name="Guillotine", time=datetime.datetime(2016, 10, 23, 15, 28, 47)))
db.session.add(
    Post(uid=166, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=255, c2_number=291, league="Standard",
         name="Old Regret", time=datetime.datetime(2016, 9, 5, 19, 33, 27)))
db.session.add(
    Post(uid=167, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=58, c2_number=56, league="Standard",
         name="Woo Woo", time=datetime.datetime(2016, 7, 7, 14, 53, 34)))
db.session.add(
    Post(uid=168, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=85, c2_number=76, league="Standard",
         name="Gunhawk", time=datetime.datetime(2016, 1, 8, 21, 43, 25)))
db.session.add(
    Post(uid=169, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=313, c2_number=195, league="Standard",
         name="Onion King", time=datetime.datetime(2016, 12, 14, 7, 16, 52)))
db.session.add(
    Post(uid=170, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=305, c2_number=222, league="Standard",
         name="Yellow Menace", time=datetime.datetime(2016, 12, 28, 19, 47, 13)))
db.session.add(
    Post(uid=171, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=154, c2_number=62, league="Standard",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 11, 26, 18, 27, 0)))
db.session.add(
    Post(uid=172, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=79, c2_number=191, league="Standard",
         name="Osprey", time=datetime.datetime(2016, 2, 5, 14, 36, 20)))
db.session.add(
    Post(uid=173, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=48, c2_number=167, league="Standard",
         name="Zero Charisma", time=datetime.datetime(2016, 1, 28, 8, 27, 47)))
db.session.add(
    Post(uid=174, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=280, c2_number=176, league="Standard",
         name="Highlander Monk", time=datetime.datetime(2016, 1, 25, 9, 43, 51)))
db.session.add(
    Post(uid=175, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=294, c2_number=131, league="Standard",
         name="Overrun", time=datetime.datetime(2016, 3, 4, 15, 8, 37)))
db.session.add(
    Post(uid=176, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=93, c2_number=312, league="Standard",
         name="Zesty Dragon", time=datetime.datetime(2016, 2, 14, 16, 32, 46)))
db.session.add(
    Post(uid=177, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=272, c2_number=237, league="Standard",
         name="Zod", time=datetime.datetime(2016, 11, 21, 20, 21, 39)))
db.session.add(
    Post(uid=0, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=229, c2_number=297, league="Standard",
         name="101", time=datetime.datetime(2016, 1, 8, 14, 1, 28)))
db.session.add(
    Post(uid=1, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=110, c2_number=130, league="Standard",
         name="Houston", time=datetime.datetime(2016, 8, 26, 21, 23, 46)))
db.session.add(
    Post(uid=2, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=162, c2_number=278, league="Standard",
         name="Pinball Wizard", time=datetime.datetime(2016, 11, 28, 22, 4, 45)))
db.session.add(Post(uid=3, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=67, c2_number=159,
                    league="Standard", name="Accidental Genius", time=datetime.datetime(2016, 12, 1, 4, 11, 53)))
db.session.add(
    Post(uid=4, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=308, c2_number=62, league="Standard",
         name="Hyper", time=datetime.datetime(2016, 1, 15, 17, 35, 7)))
db.session.add(
    Post(uid=5, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=223, c2_number=177, league="Standard",
         name="Pluto", time=datetime.datetime(2016, 2, 17, 12, 24, 21)))
db.session.add(
    Post(uid=6, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=153, c2_number=96, league="Standard",
         name="Alpha", time=datetime.datetime(2016, 6, 3, 6, 0, 56)))
db.session.add(
    Post(uid=7, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=186, c2_number=207, league="Standard",
         name="Jester", time=datetime.datetime(2016, 4, 4, 12, 17, 27)))
db.session.add(
    Post(uid=8, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=307, c2_number=247, league="Standard",
         name="Pogue", time=datetime.datetime(2016, 8, 28, 10, 17, 4)))
db.session.add(
    Post(uid=9, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=308, c2_number=33, league="Standard",
         name="Airport Hobo", time=datetime.datetime(2016, 5, 15, 5, 42, 1)))
db.session.add(
    Post(uid=10, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=73, c2_number=46, league="Standard",
         name="Jigsaw", time=datetime.datetime(2016, 6, 21, 14, 53, 6)))
db.session.add(
    Post(uid=11, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=189, c2_number=78, league="Standard",
         name="Prometheus", time=datetime.datetime(2016, 2, 10, 14, 40, 14)))
db.session.add(
    Post(uid=12, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=149, c2_number=101, league="Standard",
         name="Bearded Angler", time=datetime.datetime(2016, 1, 18, 19, 57, 53)))
db.session.add(
    Post(uid=13, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=185, c2_number=290, league="Standard",
         name="Joker's Grin", time=datetime.datetime(2016, 7, 14, 2, 35, 14)))
db.session.add(
    Post(uid=14, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=94, c2_number=54, league="Standard",
         name="Psycho Thinker", time=datetime.datetime(2016, 5, 12, 0, 44, 3)))
db.session.add(
    Post(uid=15, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=178, c2_number=314, league="Standard",
         name="Beetle King", time=datetime.datetime(2016, 6, 8, 11, 54, 54)))
db.session.add(
    Post(uid=16, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=242, c2_number=36, league="Standard",
         name="Judge", time=datetime.datetime(2016, 6, 22, 21, 18, 56)))
db.session.add(
    Post(uid=17, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=30, c2_number=152, league="Standard",
         name="Pusher", time=datetime.datetime(2016, 4, 22, 1, 28, 5)))
db.session.add(
    Post(uid=18, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=234, c2_number=139, league="Standard",
         name="Bitmap", time=datetime.datetime(2016, 8, 14, 10, 16, 12)))
db.session.add(
    Post(uid=19, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=313, c2_number=59, league="Standard",
         name="Junkyard Dog", time=datetime.datetime(2016, 5, 13, 18, 50, 9)))
db.session.add(
    Post(uid=20, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=21, c2_number=126, league="Standard",
         name="Riff Raff", time=datetime.datetime(2016, 5, 3, 18, 35, 18)))
db.session.add(Post(uid=21, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=129, c2_number=181,
                    league="Standard", name="Blister", time=datetime.datetime(2016, 4, 3, 5, 22, 38)))
db.session.add(
    Post(uid=22, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=169, c2_number=175, league="Standard",
         name="K-9", time=datetime.datetime(2016, 2, 15, 16, 28, 30)))
db.session.add(
    Post(uid=23, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=30, c2_number=285, league="Standard",
         name="Roadblock", time=datetime.datetime(2016, 1, 10, 20, 35, 45)))
db.session.add(
    Post(uid=24, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=207, c2_number=83, league="Standard",
         name="Bowie", time=datetime.datetime(2016, 7, 13, 3, 14, 51)))
db.session.add(
    Post(uid=25, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=194, c2_number=106, league="Standard",
         name="Keystone", time=datetime.datetime(2016, 7, 6, 11, 49, 54)))
db.session.add(Post(uid=26, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=70, c2_number=239,
                    league="Standard", name="Rooster", time=datetime.datetime(2016, 1, 27, 2, 41, 57)))
db.session.add(
    Post(uid=27, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=163, c2_number=85, league="Standard",
         name="Bowler", time=datetime.datetime(2016, 3, 5, 4, 22, 28)))
db.session.add(
    Post(uid=28, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=139, c2_number=131, league="Standard",
         name="Kickstart", time=datetime.datetime(2016, 4, 17, 21, 55, 19)))
db.session.add(Post(uid=29, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=195, c2_number=315,
                    league="Standard", name="Sandbox", time=datetime.datetime(2016, 10, 13, 15, 23, 23)))
db.session.add(
    Post(uid=30, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=123, c2_number=155, league="Standard",
         name="Breadmaker", time=datetime.datetime(2016, 6, 7, 13, 5, 42)))
db.session.add(
    Post(uid=31, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=51, c2_number=195, league="Standard",
         name="Kill Switch", time=datetime.datetime(2016, 3, 12, 12, 18, 44)))
db.session.add(
    Post(uid=32, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=207, c2_number=186, league="Standard",
         name="Scrapper", time=datetime.datetime(2016, 11, 13, 0, 47, 10)))
db.session.add(Post(uid=33, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=319, c2_number=163,
                    league="Standard", name="Broomspun", time=datetime.datetime(2016, 8, 28, 9, 9, 9)))
db.session.add(
    Post(uid=34, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=233, c2_number=131, league="Standard",
         name="Kingfisher", time=datetime.datetime(2016, 9, 7, 7, 5, 19)))
db.session.add(
    Post(uid=35, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=112, c2_number=188, league="Standard",
         name="Screwtape", time=datetime.datetime(2016, 7, 15, 1, 21, 13)))
db.session.add(
    Post(uid=36, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=303, c2_number=159, league="Standard",
         name="Buckshot", time=datetime.datetime(2016, 5, 18, 21, 17, 18)))
db.session.add(
    Post(uid=37, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=187, c2_number=128, league="Standard",
         name="Kitchen", time=datetime.datetime(2016, 11, 14, 1, 15, 35)))
db.session.add(
    Post(uid=38, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=136, c2_number=224, league="Standard",
         name="Sexual Chocolate", time=datetime.datetime(2016, 11, 7, 16, 6, 57)))
db.session.add(Post(uid=39, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=210, c2_number=89,
                    league="Standard", name="Bugger", time=datetime.datetime(2016, 4, 22, 18, 50, 50)))
db.session.add(
    Post(uid=40, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=115, c2_number=72, league="Standard",
         name="Knuckles", time=datetime.datetime(2016, 4, 4, 13, 31, 51)))
db.session.add(
    Post(uid=41, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=20, c2_number=66, league="Standard",
         name="Shadow Chaser", time=datetime.datetime(2016, 7, 7, 10, 57, 5)))
db.session.add(
    Post(uid=42, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=178, c2_number=244, league="Standard",
         name="Cabbie", time=datetime.datetime(2016, 1, 14, 11, 20, 24)))
db.session.add(
    Post(uid=43, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=129, c2_number=79, league="Standard",
         name="Lady Killer", time=datetime.datetime(2016, 9, 13, 14, 6, 11)))
db.session.add(
    Post(uid=44, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=85, c2_number=170, league="Standard",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 5, 27, 6, 57, 22)))
db.session.add(
    Post(uid=45, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=219, c2_number=148, league="Standard",
         name="Candy Butcher", time=datetime.datetime(2016, 3, 4, 1, 48, 56)))
db.session.add(
    Post(uid=46, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=93, c2_number=181, league="Standard",
         name="Liquid Science", time=datetime.datetime(2016, 1, 16, 13, 57, 16)))
db.session.add(
    Post(uid=47, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=281, c2_number=155, league="Standard",
         name="Shooter", time=datetime.datetime(2016, 3, 17, 22, 0, 24)))
db.session.add(
    Post(uid=48, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=114, c2_number=81, league="Standard",
         name="Capital F", time=datetime.datetime(2016, 10, 4, 13, 14, 14)))
db.session.add(
    Post(uid=49, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=167, c2_number=28, league="Standard",
         name="Little Cobra", time=datetime.datetime(2016, 12, 16, 22, 23, 13)))
db.session.add(
    Post(uid=50, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=190, c2_number=61, league="Standard",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 6, 28, 20, 42, 30)))
db.session.add(
    Post(uid=51, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=263, c2_number=316, league="Standard",
         name="Captain Peroxide", time=datetime.datetime(2016, 12, 28, 8, 5, 56)))
db.session.add(
    Post(uid=52, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=310, c2_number=212, league="Standard",
         name="Little General", time=datetime.datetime(2016, 11, 19, 8, 37, 52)))
db.session.add(
    Post(uid=53, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=140, c2_number=227, league="Standard",
         name="Skull Crusher", time=datetime.datetime(2016, 12, 3, 6, 46, 32)))
db.session.add(
    Post(uid=54, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=255, c2_number=149, league="Standard",
         name="Celtic Charger", time=datetime.datetime(2016, 5, 12, 13, 25, 23)))
db.session.add(
    Post(uid=55, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=259, c2_number=257, league="Standard",
         name="Lord Nikon", time=datetime.datetime(2016, 7, 4, 4, 29, 3)))
db.session.add(
    Post(uid=56, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=177, c2_number=260, league="Standard",
         name="Sky Bully", time=datetime.datetime(2016, 7, 3, 19, 29, 8)))
db.session.add(Post(uid=57, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=120, c2_number=51,
                    league="Standard", name="Cereal Killer", time=datetime.datetime(2016, 8, 24, 14, 10, 57)))
db.session.add(
    Post(uid=58, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=159, c2_number=318, league="Standard",
         name="Lord Pistachio", time=datetime.datetime(2016, 1, 26, 1, 5, 35)))
db.session.add(
    Post(uid=59, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=150, c2_number=245, league="Standard",
         name="Slow Trot", time=datetime.datetime(2016, 9, 28, 17, 0, 31)))
db.session.add(
    Post(uid=60, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=284, c2_number=117, league="Standard",
         name="Chicago Blackout", time=datetime.datetime(2016, 12, 6, 22, 50, 14)))
db.session.add(
    Post(uid=61, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=160, c2_number=281, league="Standard",
         name="Mad Irishman", time=datetime.datetime(2016, 8, 11, 0, 44, 56)))
db.session.add(
    Post(uid=62, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=233, c2_number=32, league="Standard",
         name="Snake Eyes", time=datetime.datetime(2016, 4, 21, 18, 4, 21)))
db.session.add(
    Post(uid=63, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=75, c2_number=161, league="Standard",
         name="Chocolate Thunder", time=datetime.datetime(2016, 2, 26, 6, 1, 19)))
db.session.add(
    Post(uid=64, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=279, c2_number=109, league="Standard",
         name="Mad Jack", time=datetime.datetime(2016, 8, 19, 8, 38, 19)))
db.session.add(
    Post(uid=65, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=145, c2_number=93, league="Standard",
         name="Snow Hound", time=datetime.datetime(2016, 9, 27, 22, 31, 54)))
db.session.add(
    Post(uid=66, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=155, c2_number=28, league="Standard",
         name="Chuckles", time=datetime.datetime(2016, 12, 9, 14, 25, 23)))
db.session.add(
    Post(uid=67, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=209, c2_number=81, league="Standard",
         name="Mad Rascal", time=datetime.datetime(2016, 2, 5, 12, 23, 26)))
db.session.add(
    Post(uid=68, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=303, c2_number=109, league="Standard",
         name="Sofa King", time=datetime.datetime(2016, 6, 18, 11, 35, 37)))
db.session.add(
    Post(uid=69, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=140, c2_number=75, league="Standard",
         name="Commando", time=datetime.datetime(2016, 8, 16, 0, 1, 57)))
db.session.add(
    Post(uid=70, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=103, c2_number=125, league="Standard",
         name="Manimal", time=datetime.datetime(2016, 3, 4, 9, 50, 18)))
db.session.add(
    Post(uid=71, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=104, c2_number=296, league="Standard",
         name="Speedwell", time=datetime.datetime(2016, 11, 4, 22, 53, 20)))
db.session.add(
    Post(uid=72, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=100, c2_number=106, league="Standard",
         name="Cool Whip", time=datetime.datetime(2016, 2, 5, 22, 11, 44)))
db.session.add(
    Post(uid=73, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=170, c2_number=68, league="Standard",
         name="Marbles", time=datetime.datetime(2016, 1, 2, 13, 22, 55)))
db.session.add(
    Post(uid=74, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=63, c2_number=104, league="Standard",
         name="Spider Fuji", time=datetime.datetime(2016, 5, 8, 10, 19, 28)))
db.session.add(Post(uid=75, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=49, c2_number=127,
                    league="Standard", name="Cosmo", time=datetime.datetime(2016, 11, 13, 18, 21, 9)))
db.session.add(
    Post(uid=76, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=144, c2_number=170, league="Standard",
         name="Married Man", time=datetime.datetime(2016, 9, 7, 8, 15, 42)))
db.session.add(
    Post(uid=77, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=127, c2_number=111, league="Standard",
         name="Springheel Jack", time=datetime.datetime(2016, 8, 22, 1, 52, 25)))
db.session.add(
    Post(uid=78, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=86, c2_number=300, league="Standard",
         name="Crash Override", time=datetime.datetime(2016, 7, 21, 19, 12, 14)))
db.session.add(
    Post(uid=79, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=132, c2_number=25, league="Standard",
         name="Marshmallow", time=datetime.datetime(2016, 2, 8, 8, 46, 19)))
db.session.add(
    Post(uid=80, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=82, c2_number=208, league="Standard",
         name="Squatch", time=datetime.datetime(2016, 8, 1, 11, 53, 35)))
db.session.add(
    Post(uid=81, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=223, c2_number=256, league="Standard",
         name="Crash Test", time=datetime.datetime(2016, 6, 24, 21, 45, 39)))
db.session.add(
    Post(uid=82, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=171, c2_number=270, league="Standard",
         name="Mental", time=datetime.datetime(2016, 12, 27, 11, 29, 39)))
db.session.add(
    Post(uid=83, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=220, c2_number=130, league="Standard",
         name="Stacker of Wheat", time=datetime.datetime(2016, 10, 16, 4, 12, 55)))
db.session.add(
    Post(uid=84, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=238, c2_number=20, league="Standard",
         name="Crazy Eights", time=datetime.datetime(2016, 11, 10, 3, 10, 51)))
db.session.add(
    Post(uid=85, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=31, c2_number=298, league="Standard",
         name="Mercury Reborn", time=datetime.datetime(2016, 9, 4, 1, 25, 52)))
db.session.add(
    Post(uid=86, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=112, c2_number=89, league="Standard",
         name="Sugar Man", time=datetime.datetime(2016, 8, 1, 17, 1, 18)))
db.session.add(
    Post(uid=87, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=253, c2_number=50, league="Standard",
         name="Criss Cross", time=datetime.datetime(2016, 8, 26, 15, 41, 15)))
db.session.add(
    Post(uid=88, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=50, c2_number=210, league="Standard",
         name="Midas", time=datetime.datetime(2016, 4, 3, 4, 25, 17)))
db.session.add(Post(uid=89, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=181, c2_number=73, league="Standard",
                    name="Suicide Jockey", time=datetime.datetime(2016, 8, 3, 11, 21, 22)))
db.session.add(
    Post(uid=90, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=118, c2_number=283, league="Standard",
         name="Cross Thread", time=datetime.datetime(2016, 3, 23, 10, 9, 30)))
db.session.add(
    Post(uid=91, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=276, c2_number=26, league="Standard",
         name="Midnight Rambler", time=datetime.datetime(2016, 1, 18, 14, 8, 47)))
db.session.add(
    Post(uid=92, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=264, c2_number=112, league="Standard",
         name="Swampmasher", time=datetime.datetime(2016, 5, 22, 5, 2, 5)))
db.session.add(Post(uid=93, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=280, c2_number=121,
                    league="Standard", name="Cujo", time=datetime.datetime(2016, 12, 4, 13, 38, 8)))
db.session.add(
    Post(uid=94, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=25, c2_number=234, league="Standard",
         name="Midnight Rider", time=datetime.datetime(2016, 2, 17, 8, 25, 26)))
db.session.add(
    Post(uid=95, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=292, c2_number=45, league="Standard",
         name="Swerve", time=datetime.datetime(2016, 5, 27, 10, 31, 20)))
db.session.add(
    Post(uid=96, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=92, c2_number=297, league="Standard",
         name="Dancing Madman", time=datetime.datetime(2016, 2, 13, 9, 6, 10)))
db.session.add(
    Post(uid=97, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=102, c2_number=111, league="Standard",
         name="Mindless Bobcat", time=datetime.datetime(2016, 7, 9, 4, 29, 13)))
db.session.add(
    Post(uid=98, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=45, c2_number=94, league="Standard",
         name="Tacklebox", time=datetime.datetime(2016, 6, 20, 15, 17, 11)))
db.session.add(
    Post(uid=99, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=316, c2_number=134, league="Standard",
         name="Dangle", time=datetime.datetime(2016, 10, 24, 4, 19, 56)))
db.session.add(
    Post(uid=100, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=211, c2_number=230, league="Standard",
         name="Mr. 44", time=datetime.datetime(2016, 7, 14, 11, 38, 18)))
db.session.add(Post(uid=101, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=310, c2_number=131,
                    league="Standard", name="Take Away", time=datetime.datetime(2016, 6, 28, 13, 40, 51)))
db.session.add(
    Post(uid=102, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=94, c2_number=57, league="Standard",
         name="Dark Horse", time=datetime.datetime(2016, 7, 28, 21, 24, 36)))
db.session.add(
    Post(uid=103, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=176, c2_number=94, league="Standard",
         name="Mr. Fabulous", time=datetime.datetime(2016, 1, 19, 20, 19, 6)))
db.session.add(
    Post(uid=104, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=81, c2_number=225, league="Standard",
         name="Tan Stallion", time=datetime.datetime(2016, 2, 26, 11, 12, 5)))
db.session.add(
    Post(uid=105, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=130, c2_number=151, league="Standard",
         name="Day Hawk", time=datetime.datetime(2016, 4, 28, 22, 10, 21)))
db.session.add(
    Post(uid=106, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=28, c2_number=239, league="Standard",
         name="Mr. Gadget", time=datetime.datetime(2016, 11, 11, 11, 46, 43)))
db.session.add(
    Post(uid=107, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=49, c2_number=87, league="Standard",
         name="The China Wall", time=datetime.datetime(2016, 9, 25, 11, 53, 54)))
db.session.add(
    Post(uid=108, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=310, c2_number=146, league="Standard",
         name="Desert Haze", time=datetime.datetime(2016, 6, 2, 1, 36, 38)))
db.session.add(
    Post(uid=109, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=165, c2_number=223, league="Standard",
         name="Mr. Lucky", time=datetime.datetime(2016, 4, 14, 20, 33, 48)))
db.session.add(Post(uid=110, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=51, c2_number=87, league="Standard",
                    name="The Dude", time=datetime.datetime(2016, 12, 28, 2, 43, 58)))
db.session.add(
    Post(uid=111, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=113, c2_number=204, league="Standard",
         name="Digger", time=datetime.datetime(2016, 7, 24, 21, 14, 57)))
db.session.add(Post(uid=112, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=262, c2_number=123, league="Standard",
                    name="Mr. Peppermint", time=datetime.datetime(2016, 2, 1, 19, 58, 32)))
db.session.add(
    Post(uid=113, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=202, c2_number=21, league="Standard",
         name="The Flying Mouse", time=datetime.datetime(2016, 10, 6, 6, 44, 25)))
db.session.add(Post(uid=114, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=245, c2_number=231, league="Standard",
                    name="Disco Thunder", time=datetime.datetime(2016, 1, 15, 0, 54, 17)))
db.session.add(
    Post(uid=115, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=275, c2_number=111, league="Standard",
         name="Mr. Spy", time=datetime.datetime(2016, 4, 8, 5, 49, 19)))
db.session.add(
    Post(uid=116, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=223, c2_number=287, league="Standard",
         name="The Happy Jock", time=datetime.datetime(2016, 3, 11, 20, 8, 14)))
db.session.add(
    Post(uid=117, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=110, c2_number=87, league="Standard",
         name="Disco Potato", time=datetime.datetime(2016, 9, 2, 22, 27, 21)))
db.session.add(
    Post(uid=118, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=62, c2_number=248, league="Standard",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 6, 2, 16, 14, 47)))
db.session.add(
    Post(uid=119, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=135, c2_number=290, league="Standard",
         name="The Howling Swede", time=datetime.datetime(2016, 5, 9, 15, 0, 52)))
db.session.add(
    Post(uid=120, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=50, c2_number=292, league="Standard",
         name="Dr. Cocktail", time=datetime.datetime(2016, 6, 13, 18, 2, 47)))
db.session.add(
    Post(uid=121, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=171, c2_number=43, league="Standard",
         name="Mr. Wholesome", time=datetime.datetime(2016, 4, 28, 4, 30, 24)))
db.session.add(
    Post(uid=122, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=240, c2_number=282, league="Standard",
         name="Thrasher", time=datetime.datetime(2016, 10, 12, 7, 11, 16)))
db.session.add(
    Post(uid=123, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=96, c2_number=214, league="Standard",
         name="Dredd", time=datetime.datetime(2016, 1, 14, 2, 36, 54)))
db.session.add(Post(uid=124, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=38, c2_number=107, league="Standard",
                    name="Mud Pie Man", time=datetime.datetime(2016, 11, 12, 4, 12, 18)))
db.session.add(
    Post(uid=125, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=101, c2_number=122, league="Standard", name="Toe",
         time=datetime.datetime(2016, 5, 19, 18, 30, 22)))
db.session.add(
    Post(uid=126, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=204, c2_number=179, league="Standard",
         name="Dropkick", time=datetime.datetime(2016, 2, 17, 4, 5, 37)))
db.session.add(
    Post(uid=127, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=124, c2_number=163, league="Standard",
         name="Mule Skinner", time=datetime.datetime(2016, 6, 25, 3, 12, 26)))
db.session.add(Post(uid=128, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=318, c2_number=149, league="Standard",
                    name="Toolmaker", time=datetime.datetime(2016, 11, 21, 4, 1, 10)))
db.session.add(
    Post(uid=129, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=159, c2_number=278, league="Standard",
         name="Drop Stone", time=datetime.datetime(2016, 6, 3, 13, 18, 50)))
db.session.add(Post(uid=130, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=183, c2_number=89, league="Standard",
                    name="Murmur", time=datetime.datetime(2016, 6, 23, 3, 48, 10)))
db.session.add(
    Post(uid=131, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=282, c2_number=106, league="Standard",
         name="Tough Nut", time=datetime.datetime(2016, 2, 7, 5, 12, 29)))
db.session.add(Post(uid=132, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=318, c2_number=59, league="Standard",
                    name="Drugstore Cowboy", time=datetime.datetime(2016, 5, 2, 16, 22, 37)))
db.session.add(Post(uid=133, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=144, c2_number=275, league="Standard",
                    name="Nacho", time=datetime.datetime(2016, 1, 23, 9, 49, 44)))
db.session.add(
    Post(uid=134, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=204, c2_number=253, league="Standard",
         name="Trip", time=datetime.datetime(2016, 12, 9, 11, 16, 29)))
db.session.add(
    Post(uid=135, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=24, c2_number=279, league="Standard",
         name="Easy Sweep", time=datetime.datetime(2016, 8, 14, 14, 50, 15)))
db.session.add(
    Post(uid=136, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=149, c2_number=146, league="Standard",
         name="Natural Mess", time=datetime.datetime(2016, 11, 20, 6, 39, 42)))
db.session.add(
    Post(uid=137, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=75, c2_number=291, league="Standard",
         name="Troubadour", time=datetime.datetime(2016, 2, 17, 11, 38, 56)))
db.session.add(
    Post(uid=138, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=214, c2_number=172, league="Standard",
         name="Electric Player", time=datetime.datetime(2016, 1, 3, 21, 43, 33)))
db.session.add(
    Post(uid=139, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=270, c2_number=86, league="Standard",
         name="Necromancer", time=datetime.datetime(2016, 1, 4, 13, 52, 28)))
db.session.add(
    Post(uid=140, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=299, c2_number=224, league="Standard",
         name="Turnip King", time=datetime.datetime(2016, 11, 20, 13, 17, 57)))
db.session.add(
    Post(uid=141, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=253, c2_number=39, league="Standard",
         name="Esquire", time=datetime.datetime(2016, 2, 8, 20, 7, 47)))
db.session.add(Post(uid=142, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=58, c2_number=123, league="Standard",
                    name="Neophyte Believer", time=datetime.datetime(2016, 3, 6, 3, 6, 50)))
db.session.add(Post(uid=143, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=307, c2_number=206, league="Standard",
                    name="Twitch", time=datetime.datetime(2016, 7, 6, 1, 50, 43)))
db.session.add(
    Post(uid=144, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=105, c2_number=47, league="Standard",
         name="Fast Draw", time=datetime.datetime(2016, 5, 14, 18, 36, 26)))
db.session.add(Post(uid=145, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=77, c2_number=280, league="Standard",
                    name="Nessie", time=datetime.datetime(2016, 8, 18, 17, 16, 56)))
db.session.add(
    Post(uid=146, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=44, c2_number=222, league="Standard",
         name="Vagabond Warrior", time=datetime.datetime(2016, 3, 25, 9, 3, 45)))
db.session.add(Post(uid=147, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=267, c2_number=181,
                    league="Standard", name="Flakes", time=datetime.datetime(2016, 6, 12, 20, 34, 40)))
db.session.add(
    Post(uid=148, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=27, c2_number=147, league="Standard",
         name="New Cycle", time=datetime.datetime(2016, 11, 10, 11, 37, 32)))
db.session.add(
    Post(uid=149, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=277, c2_number=202, league="Standard",
         name="Voluntary", time=datetime.datetime(2016, 12, 22, 15, 50, 43)))
db.session.add(
    Post(uid=150, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=149, c2_number=90, league="Standard",
         name="Flint", time=datetime.datetime(2016, 12, 5, 8, 12, 27)))
db.session.add(
    Post(uid=151, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=152, c2_number=240, league="Standard",
         name="Nickname Master", time=datetime.datetime(2016, 1, 26, 5, 22, 26)))
db.session.add(
    Post(uid=152, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=125, c2_number=258, league="Standard",
         name="Vortex", time=datetime.datetime(2016, 11, 15, 18, 35, 23)))
db.session.add(
    Post(uid=153, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=160, c2_number=28, league="Standard",
         name="Freak", time=datetime.datetime(2016, 3, 13, 6, 10, 53)))
db.session.add(
    Post(uid=154, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=153, c2_number=112, league="Standard",
         name="Nightmare King", time=datetime.datetime(2016, 3, 11, 12, 54, 42)))
db.session.add(
    Post(uid=155, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=274, c2_number=288, league="Standard",
         name="Washer", time=datetime.datetime(2016, 6, 20, 20, 8, 19)))
db.session.add(
    Post(uid=156, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=291, c2_number=261, league="Standard",
         name="Gas Man", time=datetime.datetime(2016, 8, 25, 15, 50, 0)))
db.session.add(
    Post(uid=157, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=260, c2_number=160, league="Standard",
         name="Night Train", time=datetime.datetime(2016, 6, 13, 16, 16, 45)))
db.session.add(
    Post(uid=158, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=125, c2_number=184, league="Standard",
         name="Waylay Dave", time=datetime.datetime(2016, 9, 1, 17, 43, 48)))
db.session.add(
    Post(uid=159, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=148, c2_number=270, league="Standard",
         name="Glyph", time=datetime.datetime(2016, 6, 16, 7, 29, 51)))
db.session.add(
    Post(uid=160, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=45, c2_number=41, league="Standard",
         name="Old Man Winter", time=datetime.datetime(2016, 4, 22, 20, 54, 45)))
db.session.add(
    Post(uid=161, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=191, c2_number=300, league="Standard",
         name="Wheels", time=datetime.datetime(2016, 6, 7, 16, 5, 51)))
db.session.add(
    Post(uid=162, c1_item="Perandus Coin", c2_item="Perandus Coin", c1_number=285, c2_number=289, league="Standard",
         name="Grave Digger", time=datetime.datetime(2016, 8, 27, 0, 37, 33)))
db.session.add(
    Post(uid=163, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=178, c2_number=275, league="Standard",
         name="Old Orange Eyes", time=datetime.datetime(2016, 7, 28, 0, 35, 16)))
db.session.add(
    Post(uid=164, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=287, c2_number=24, league="Standard",
         name="Wooden Man", time=datetime.datetime(2016, 12, 4, 22, 12, 30)))
db.session.add(Post(uid=165, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=263, c2_number=220,
                    league="Standard", name="Guillotine", time=datetime.datetime(2016, 2, 28, 6, 35, 20)))
db.session.add(Post(uid=166, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=89, c2_number=312, league="Standard",
                    name="Old Regret", time=datetime.datetime(2016, 2, 9, 4, 51, 22)))
db.session.add(
    Post(uid=167, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=231, c2_number=267, league="Standard",
         name="Woo Woo", time=datetime.datetime(2016, 11, 18, 11, 16, 2)))
db.session.add(Post(uid=168, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=29, c2_number=46, league="Standard",
                    name="Gunhawk", time=datetime.datetime(2016, 4, 5, 22, 8, 4)))
db.session.add(
    Post(uid=169, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=244, c2_number=272, league="Standard",
         name="Onion King", time=datetime.datetime(2016, 7, 9, 21, 24, 47)))
db.session.add(
    Post(uid=170, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=50, c2_number=133, league="Standard",
         name="Yellow Menace", time=datetime.datetime(2016, 10, 14, 4, 7, 38)))
db.session.add(
    Post(uid=171, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=49, c2_number=245, league="Standard",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 5, 25, 17, 9, 14)))
db.session.add(
    Post(uid=172, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=208, c2_number=200, league="Standard",
         name="Osprey", time=datetime.datetime(2016, 10, 6, 0, 47, 27)))
db.session.add(
    Post(uid=173, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=148, c2_number=149, league="Standard",
         name="Zero Charisma", time=datetime.datetime(2016, 3, 27, 5, 48, 58)))
db.session.add(
    Post(uid=174, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=247, c2_number=95, league="Standard",
         name="Highlander Monk", time=datetime.datetime(2016, 12, 16, 5, 58, 58)))
db.session.add(
    Post(uid=175, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=121, c2_number=244, league="Standard",
         name="Overrun", time=datetime.datetime(2016, 4, 13, 8, 17, 20)))
db.session.add(
    Post(uid=176, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=34, c2_number=156, league="Standard",
         name="Zesty Dragon", time=datetime.datetime(2016, 4, 14, 6, 46, 12)))
db.session.add(
    Post(uid=177, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=280, c2_number=275, league="Standard",
         name="Zod", time=datetime.datetime(2016, 8, 8, 0, 54, 53)))
db.session.add(
    Post(uid=0, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=180, c2_number=149, league="Standard", name="101",
         time=datetime.datetime(2016, 2, 2, 12, 22, 55)))
db.session.add(Post(uid=1, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=153, c2_number=61, league="Standard",
                    name="Houston", time=datetime.datetime(2016, 6, 16, 6, 36, 11)))
db.session.add(
    Post(uid=2, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=174, c2_number=31, league="Standard",
         name="Pinball Wizard", time=datetime.datetime(2016, 8, 3, 4, 43, 25)))
db.session.add(
    Post(uid=3, c1_item="Silver Coin", c2_item="Silver Coin", c1_number=208, c2_number=267, league="Standard",
         name="Accidental Genius", time=datetime.datetime(2016, 7, 26, 10, 27, 19)))
db.session.add(
    Post(uid=4, c1_item="Blessed Orb", c2_item="Blessed Orb", c1_number=289, c2_number=109, league="Hardcore",
         name="Hyper", time=datetime.datetime(2016, 6, 13, 15, 56, 6)))
db.session.add(
    Post(uid=5, c1_item="Blessed Orb", c2_item="Cartographer's Chisel", c1_number=315, c2_number=31, league="Hardcore",
         name="Pluto", time=datetime.datetime(2016, 6, 23, 5, 22, 43)))
db.session.add(Post(uid=6, c1_item="Blessed Orb", c2_item="Chaos Orb", c1_number=242, c2_number=217, league="Hardcore",
                    name="Alpha", time=datetime.datetime(2016, 2, 28, 12, 7, 23)))
db.session.add(
    Post(uid=7, c1_item="Blessed Orb", c2_item="Chromatic Orb", c1_number=90, c2_number=281, league="Hardcore",
         name="Jester", time=datetime.datetime(2016, 7, 18, 10, 38, 11)))
db.session.add(Post(uid=8, c1_item="Blessed Orb", c2_item="Divine Orb", c1_number=90, c2_number=152, league="Hardcore",
                    name="Pogue", time=datetime.datetime(2016, 6, 12, 7, 26, 23)))
db.session.add(
    Post(uid=9, c1_item="Blessed Orb", c2_item="Exalted Orb", c1_number=278, c2_number=282, league="Hardcore",
         name="Airport Hobo", time=datetime.datetime(2016, 2, 2, 8, 32, 30)))
db.session.add(
    Post(uid=10, c1_item="Blessed Orb", c2_item="Gemcutter's Prism", c1_number=118, c2_number=219, league="Hardcore",
         name="Jigsaw", time=datetime.datetime(2016, 2, 18, 14, 17, 14)))
db.session.add(
    Post(uid=11, c1_item="Blessed Orb", c2_item="Jeweller's Orb", c1_number=297, c2_number=71, league="Hardcore",
         name="Prometheus", time=datetime.datetime(2016, 4, 20, 12, 4, 29)))
db.session.add(
    Post(uid=12, c1_item="Blessed Orb", c2_item="Orb of Alchemy", c1_number=202, c2_number=303, league="Hardcore",
         name="Bearded Angler", time=datetime.datetime(2016, 6, 13, 3, 30, 49)))
db.session.add(
    Post(uid=13, c1_item="Blessed Orb", c2_item="Orb of Alteration", c1_number=247, c2_number=147, league="Hardcore",
         name="Joker's Grin", time=datetime.datetime(2016, 12, 12, 13, 53, 52)))
db.session.add(
    Post(uid=14, c1_item="Blessed Orb", c2_item="Orb of Chance", c1_number=256, c2_number=209, league="Hardcore",
         name="Psycho Thinker", time=datetime.datetime(2016, 2, 2, 19, 23, 6)))
db.session.add(
    Post(uid=15, c1_item="Blessed Orb", c2_item="Orb of Fusing", c1_number=197, c2_number=279, league="Hardcore",
         name="Beetle King", time=datetime.datetime(2016, 4, 18, 21, 49, 34)))
db.session.add(
    Post(uid=16, c1_item="Blessed Orb", c2_item="Orb of Regret", c1_number=51, c2_number=31, league="Hardcore",
         name="Judge", time=datetime.datetime(2016, 10, 13, 8, 49, 22)))
db.session.add(
    Post(uid=17, c1_item="Blessed Orb", c2_item="Orb of Scouring", c1_number=115, c2_number=173, league="Hardcore",
         name="Pusher", time=datetime.datetime(2016, 9, 28, 11, 18, 21)))
db.session.add(Post(uid=18, c1_item="Blessed Orb", c2_item="Regal Orb", c1_number=303, c2_number=186, league="Hardcore",
                    name="Bitmap", time=datetime.datetime(2016, 3, 8, 4, 10, 6)))
db.session.add(Post(uid=19, c1_item="Blessed Orb", c2_item="Vaal Orb", c1_number=293, c2_number=244, league="Hardcore",
                    name="Junkyard Dog", time=datetime.datetime(2016, 11, 14, 3, 55, 9)))
db.session.add(
    Post(uid=20, c1_item="Blessed Orb", c2_item="Perandus Coin", c1_number=54, c2_number=153, league="Hardcore",
         name="Riff Raff", time=datetime.datetime(2016, 7, 15, 14, 34, 44)))
db.session.add(
    Post(uid=21, c1_item="Blessed Orb", c2_item="Silver Coin", c1_number=237, c2_number=56, league="Hardcore",
         name="Blister", time=datetime.datetime(2016, 10, 18, 4, 3, 6)))
db.session.add(
    Post(uid=22, c1_item="Cartographer's Chisel", c2_item="Blessed Orb", c1_number=26, c2_number=76, league="Hardcore",
         name="K-9", time=datetime.datetime(2016, 10, 10, 9, 13, 47)))
db.session.add(
    Post(uid=23, c1_item="Cartographer's Chisel", c2_item="Cartographer's Chisel", c1_number=278, c2_number=305,
         league="Hardcore", name="Roadblock", time=datetime.datetime(2016, 6, 20, 7, 54, 30)))
db.session.add(
    Post(uid=24, c1_item="Cartographer's Chisel", c2_item="Chaos Orb", c1_number=168, c2_number=226, league="Hardcore",
         name="Bowie", time=datetime.datetime(2016, 7, 22, 10, 39, 17)))
db.session.add(Post(uid=25, c1_item="Cartographer's Chisel", c2_item="Chromatic Orb", c1_number=150, c2_number=174,
                    league="Hardcore", name="Keystone", time=datetime.datetime(2016, 6, 7, 11, 37, 26)))
db.session.add(
    Post(uid=26, c1_item="Cartographer's Chisel", c2_item="Divine Orb", c1_number=44, c2_number=97, league="Hardcore",
         name="Rooster", time=datetime.datetime(2016, 2, 8, 7, 3, 13)))
db.session.add(Post(uid=27, c1_item="Cartographer's Chisel", c2_item="Exalted Orb", c1_number=294, c2_number=191,
                    league="Hardcore", name="Bowler", time=datetime.datetime(2016, 2, 9, 12, 49, 22)))
db.session.add(Post(uid=28, c1_item="Cartographer's Chisel", c2_item="Gemcutter's Prism", c1_number=283, c2_number=78,
                    league="Hardcore", name="Kickstart", time=datetime.datetime(2016, 10, 10, 0, 4, 7)))
db.session.add(Post(uid=29, c1_item="Cartographer's Chisel", c2_item="Jeweller's Orb", c1_number=74, c2_number=64,
                    league="Hardcore", name="Sandbox", time=datetime.datetime(2016, 11, 6, 19, 37, 11)))
db.session.add(Post(uid=30, c1_item="Cartographer's Chisel", c2_item="Orb of Alchemy", c1_number=148, c2_number=110,
                    league="Hardcore", name="Breadmaker", time=datetime.datetime(2016, 8, 27, 9, 55, 18)))
db.session.add(Post(uid=31, c1_item="Cartographer's Chisel", c2_item="Orb of Alteration", c1_number=152, c2_number=125,
                    league="Hardcore", name="Kill Switch", time=datetime.datetime(2016, 11, 16, 1, 57, 16)))
db.session.add(Post(uid=32, c1_item="Cartographer's Chisel", c2_item="Orb of Chance", c1_number=129, c2_number=240,
                    league="Hardcore", name="Scrapper", time=datetime.datetime(2016, 11, 6, 5, 50, 14)))
db.session.add(Post(uid=33, c1_item="Cartographer's Chisel", c2_item="Orb of Fusing", c1_number=167, c2_number=144,
                    league="Hardcore", name="Broomspun", time=datetime.datetime(2016, 1, 2, 4, 37, 8)))
db.session.add(Post(uid=34, c1_item="Cartographer's Chisel", c2_item="Orb of Regret", c1_number=144, c2_number=157,
                    league="Hardcore", name="Kingfisher", time=datetime.datetime(2016, 10, 2, 20, 42, 31)))
db.session.add(Post(uid=35, c1_item="Cartographer's Chisel", c2_item="Orb of Scouring", c1_number=229, c2_number=93,
                    league="Hardcore", name="Screwtape", time=datetime.datetime(2016, 12, 17, 18, 29, 28)))
db.session.add(
    Post(uid=36, c1_item="Cartographer's Chisel", c2_item="Regal Orb", c1_number=188, c2_number=134, league="Hardcore",
         name="Buckshot", time=datetime.datetime(2016, 11, 13, 2, 27, 2)))
db.session.add(
    Post(uid=37, c1_item="Cartographer's Chisel", c2_item="Vaal Orb", c1_number=104, c2_number=269, league="Hardcore",
         name="Kitchen", time=datetime.datetime(2016, 10, 10, 9, 44, 12)))
db.session.add(Post(uid=38, c1_item="Cartographer's Chisel", c2_item="Perandus Coin", c1_number=167, c2_number=175,
                    league="Hardcore", name="Sexual Chocolate", time=datetime.datetime(2016, 9, 4, 0, 0, 22)))
db.session.add(
    Post(uid=39, c1_item="Cartographer's Chisel", c2_item="Silver Coin", c1_number=57, c2_number=96, league="Hardcore",
         name="Bugger", time=datetime.datetime(2016, 8, 14, 4, 43, 13)))
db.session.add(Post(uid=40, c1_item="Chaos Orb", c2_item="Blessed Orb", c1_number=158, c2_number=270, league="Hardcore",
                    name="Knuckles", time=datetime.datetime(2016, 8, 11, 11, 12, 8)))
db.session.add(
    Post(uid=41, c1_item="Chaos Orb", c2_item="Cartographer's Chisel", c1_number=44, c2_number=27, league="Hardcore",
         name="Shadow Chaser", time=datetime.datetime(2016, 2, 2, 8, 12, 32)))
db.session.add(Post(uid=42, c1_item="Chaos Orb", c2_item="Chaos Orb", c1_number=184, c2_number=318, league="Hardcore",
                    name="Cabbie", time=datetime.datetime(2016, 2, 5, 22, 49, 16)))
db.session.add(
    Post(uid=43, c1_item="Chaos Orb", c2_item="Chromatic Orb", c1_number=140, c2_number=86, league="Hardcore",
         name="Lady Killer", time=datetime.datetime(2016, 9, 16, 5, 6, 33)))
db.session.add(Post(uid=44, c1_item="Chaos Orb", c2_item="Divine Orb", c1_number=205, c2_number=146, league="Hardcore",
                    name="Sherwood Gladiator", time=datetime.datetime(2016, 4, 12, 11, 11, 19)))
db.session.add(Post(uid=45, c1_item="Chaos Orb", c2_item="Exalted Orb", c1_number=240, c2_number=279, league="Hardcore",
                    name="Candy Butcher", time=datetime.datetime(2016, 11, 25, 16, 8, 11)))
db.session.add(
    Post(uid=46, c1_item="Chaos Orb", c2_item="Gemcutter's Prism", c1_number=167, c2_number=309, league="Hardcore",
         name="Liquid Science", time=datetime.datetime(2016, 11, 16, 20, 57, 20)))
db.session.add(
    Post(uid=47, c1_item="Chaos Orb", c2_item="Jeweller's Orb", c1_number=297, c2_number=43, league="Hardcore",
         name="Shooter", time=datetime.datetime(2016, 6, 5, 14, 40, 41)))
db.session.add(
    Post(uid=48, c1_item="Chaos Orb", c2_item="Orb of Alchemy", c1_number=100, c2_number=245, league="Hardcore",
         name="Capital F", time=datetime.datetime(2016, 5, 1, 9, 5, 31)))
db.session.add(
    Post(uid=49, c1_item="Chaos Orb", c2_item="Orb of Alteration", c1_number=124, c2_number=93, league="Hardcore",
         name="Little Cobra", time=datetime.datetime(2016, 8, 1, 4, 21, 6)))
db.session.add(
    Post(uid=50, c1_item="Chaos Orb", c2_item="Orb of Chance", c1_number=208, c2_number=255, league="Hardcore",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 3, 8, 4, 10, 44)))
db.session.add(
    Post(uid=51, c1_item="Chaos Orb", c2_item="Orb of Fusing", c1_number=69, c2_number=304, league="Hardcore",
         name="Captain Peroxide", time=datetime.datetime(2016, 10, 23, 4, 8, 6)))
db.session.add(
    Post(uid=52, c1_item="Chaos Orb", c2_item="Orb of Regret", c1_number=108, c2_number=153, league="Hardcore",
         name="Little General", time=datetime.datetime(2016, 5, 24, 16, 50, 35)))
db.session.add(
    Post(uid=53, c1_item="Chaos Orb", c2_item="Orb of Scouring", c1_number=185, c2_number=174, league="Hardcore",
         name="Skull Crusher", time=datetime.datetime(2016, 7, 17, 0, 58, 12)))
db.session.add(Post(uid=54, c1_item="Chaos Orb", c2_item="Regal Orb", c1_number=232, c2_number=228, league="Hardcore",
                    name="Celtic Charger", time=datetime.datetime(2016, 4, 2, 9, 23, 19)))
db.session.add(Post(uid=55, c1_item="Chaos Orb", c2_item="Vaal Orb", c1_number=136, c2_number=225, league="Hardcore",
                    name="Lord Nikon", time=datetime.datetime(2016, 7, 8, 20, 17, 27)))
db.session.add(
    Post(uid=56, c1_item="Chaos Orb", c2_item="Perandus Coin", c1_number=203, c2_number=279, league="Hardcore",
         name="Sky Bully", time=datetime.datetime(2016, 9, 23, 5, 8, 18)))
db.session.add(Post(uid=57, c1_item="Chaos Orb", c2_item="Silver Coin", c1_number=270, c2_number=50, league="Hardcore",
                    name="Cereal Killer", time=datetime.datetime(2016, 11, 25, 16, 46, 41)))
db.session.add(
    Post(uid=58, c1_item="Chromatic Orb", c2_item="Blessed Orb", c1_number=217, c2_number=207, league="Hardcore",
         name="Lord Pistachio", time=datetime.datetime(2016, 3, 26, 9, 39, 7)))
db.session.add(Post(uid=59, c1_item="Chromatic Orb", c2_item="Cartographer's Chisel", c1_number=43, c2_number=223,
                    league="Hardcore", name="Slow Trot", time=datetime.datetime(2016, 7, 23, 15, 15, 7)))
db.session.add(Post(uid=60, c1_item="Chromatic Orb", c2_item="Chaos Orb", c1_number=82, c2_number=89, league="Hardcore",
                    name="Chicago Blackout", time=datetime.datetime(2016, 2, 26, 0, 21, 34)))
db.session.add(
    Post(uid=61, c1_item="Chromatic Orb", c2_item="Chromatic Orb", c1_number=58, c2_number=253, league="Hardcore",
         name="Mad Irishman", time=datetime.datetime(2016, 12, 1, 8, 36, 3)))
db.session.add(
    Post(uid=62, c1_item="Chromatic Orb", c2_item="Divine Orb", c1_number=211, c2_number=145, league="Hardcore",
         name="Snake Eyes", time=datetime.datetime(2016, 5, 2, 13, 51, 9)))
db.session.add(
    Post(uid=63, c1_item="Chromatic Orb", c2_item="Exalted Orb", c1_number=80, c2_number=191, league="Hardcore",
         name="Chocolate Thunder", time=datetime.datetime(2016, 5, 5, 2, 43, 38)))
db.session.add(
    Post(uid=64, c1_item="Chromatic Orb", c2_item="Gemcutter's Prism", c1_number=95, c2_number=301, league="Hardcore",
         name="Mad Jack", time=datetime.datetime(2016, 11, 9, 6, 12, 56)))
db.session.add(
    Post(uid=65, c1_item="Chromatic Orb", c2_item="Jeweller's Orb", c1_number=134, c2_number=40, league="Hardcore",
         name="Snow Hound", time=datetime.datetime(2016, 10, 25, 20, 48, 30)))
db.session.add(
    Post(uid=66, c1_item="Chromatic Orb", c2_item="Orb of Alchemy", c1_number=241, c2_number=280, league="Hardcore",
         name="Chuckles", time=datetime.datetime(2016, 7, 14, 22, 27, 25)))
db.session.add(
    Post(uid=67, c1_item="Chromatic Orb", c2_item="Orb of Alteration", c1_number=152, c2_number=27, league="Hardcore",
         name="Mad Rascal", time=datetime.datetime(2016, 8, 10, 5, 2, 28)))
db.session.add(
    Post(uid=68, c1_item="Chromatic Orb", c2_item="Orb of Chance", c1_number=246, c2_number=96, league="Hardcore",
         name="Sofa King", time=datetime.datetime(2016, 3, 27, 18, 58, 34)))
db.session.add(
    Post(uid=69, c1_item="Chromatic Orb", c2_item="Orb of Fusing", c1_number=56, c2_number=205, league="Hardcore",
         name="Commando", time=datetime.datetime(2016, 10, 4, 2, 23, 49)))
db.session.add(
    Post(uid=70, c1_item="Chromatic Orb", c2_item="Orb of Regret", c1_number=217, c2_number=253, league="Hardcore",
         name="Manimal", time=datetime.datetime(2016, 8, 7, 3, 0, 52)))
db.session.add(
    Post(uid=71, c1_item="Chromatic Orb", c2_item="Orb of Scouring", c1_number=56, c2_number=43, league="Hardcore",
         name="Speedwell", time=datetime.datetime(2016, 5, 16, 11, 37, 53)))
db.session.add(
    Post(uid=72, c1_item="Chromatic Orb", c2_item="Regal Orb", c1_number=260, c2_number=308, league="Hardcore",
         name="Cool Whip", time=datetime.datetime(2016, 11, 4, 10, 22, 54)))
db.session.add(
    Post(uid=73, c1_item="Chromatic Orb", c2_item="Vaal Orb", c1_number=225, c2_number=259, league="Hardcore",
         name="Marbles", time=datetime.datetime(2016, 10, 4, 8, 38, 52)))
db.session.add(
    Post(uid=74, c1_item="Chromatic Orb", c2_item="Perandus Coin", c1_number=261, c2_number=158, league="Hardcore",
         name="Spider Fuji", time=datetime.datetime(2016, 6, 9, 2, 16, 14)))
db.session.add(
    Post(uid=75, c1_item="Chromatic Orb", c2_item="Silver Coin", c1_number=163, c2_number=156, league="Hardcore",
         name="Cosmo", time=datetime.datetime(2016, 1, 23, 11, 55, 34)))
db.session.add(Post(uid=76, c1_item="Divine Orb", c2_item="Blessed Orb", c1_number=24, c2_number=268, league="Hardcore",
                    name="Married Man", time=datetime.datetime(2016, 7, 19, 7, 35, 49)))
db.session.add(
    Post(uid=77, c1_item="Divine Orb", c2_item="Cartographer's Chisel", c1_number=281, c2_number=202, league="Hardcore",
         name="Springheel Jack", time=datetime.datetime(2016, 5, 24, 1, 36, 51)))
db.session.add(Post(uid=78, c1_item="Divine Orb", c2_item="Chaos Orb", c1_number=251, c2_number=249, league="Hardcore",
                    name="Crash Override", time=datetime.datetime(2016, 4, 7, 17, 57, 55)))
db.session.add(
    Post(uid=79, c1_item="Divine Orb", c2_item="Chromatic Orb", c1_number=197, c2_number=44, league="Hardcore",
         name="Marshmallow", time=datetime.datetime(2016, 2, 3, 14, 20, 49)))
db.session.add(Post(uid=80, c1_item="Divine Orb", c2_item="Divine Orb", c1_number=258, c2_number=51, league="Hardcore",
                    name="Squatch", time=datetime.datetime(2016, 5, 15, 20, 1, 14)))
db.session.add(
    Post(uid=81, c1_item="Divine Orb", c2_item="Exalted Orb", c1_number=129, c2_number=266, league="Hardcore",
         name="Crash Test", time=datetime.datetime(2016, 6, 21, 3, 15, 8)))
db.session.add(
    Post(uid=82, c1_item="Divine Orb", c2_item="Gemcutter's Prism", c1_number=201, c2_number=288, league="Hardcore",
         name="Mental", time=datetime.datetime(2016, 9, 16, 8, 27, 7)))
db.session.add(
    Post(uid=83, c1_item="Divine Orb", c2_item="Jeweller's Orb", c1_number=310, c2_number=119, league="Hardcore",
         name="Stacker of Wheat", time=datetime.datetime(2016, 12, 9, 15, 36, 36)))
db.session.add(
    Post(uid=84, c1_item="Divine Orb", c2_item="Orb of Alchemy", c1_number=306, c2_number=161, league="Hardcore",
         name="Crazy Eights", time=datetime.datetime(2016, 8, 18, 19, 34, 5)))
db.session.add(
    Post(uid=85, c1_item="Divine Orb", c2_item="Orb of Alteration", c1_number=142, c2_number=189, league="Hardcore",
         name="Mercury Reborn", time=datetime.datetime(2016, 4, 10, 14, 18, 58)))
db.session.add(
    Post(uid=86, c1_item="Divine Orb", c2_item="Orb of Chance", c1_number=120, c2_number=296, league="Hardcore",
         name="Sugar Man", time=datetime.datetime(2016, 1, 13, 19, 57, 51)))
db.session.add(
    Post(uid=87, c1_item="Divine Orb", c2_item="Orb of Fusing", c1_number=185, c2_number=261, league="Hardcore",
         name="Criss Cross", time=datetime.datetime(2016, 9, 8, 22, 19, 15)))
db.session.add(
    Post(uid=88, c1_item="Divine Orb", c2_item="Orb of Regret", c1_number=256, c2_number=60, league="Hardcore",
         name="Midas", time=datetime.datetime(2016, 12, 17, 4, 46, 50)))
db.session.add(
    Post(uid=89, c1_item="Divine Orb", c2_item="Orb of Scouring", c1_number=219, c2_number=267, league="Hardcore",
         name="Suicide Jockey", time=datetime.datetime(2016, 9, 14, 21, 27, 0)))
db.session.add(Post(uid=90, c1_item="Divine Orb", c2_item="Regal Orb", c1_number=315, c2_number=301, league="Hardcore",
                    name="Cross Thread", time=datetime.datetime(2016, 10, 22, 7, 31, 29)))
db.session.add(Post(uid=91, c1_item="Divine Orb", c2_item="Vaal Orb", c1_number=152, c2_number=86, league="Hardcore",
                    name="Midnight Rambler", time=datetime.datetime(2016, 3, 1, 13, 25, 38)))
db.session.add(
    Post(uid=92, c1_item="Divine Orb", c2_item="Perandus Coin", c1_number=317, c2_number=314, league="Hardcore",
         name="Swampmasher", time=datetime.datetime(2016, 8, 1, 9, 35, 30)))
db.session.add(Post(uid=93, c1_item="Divine Orb", c2_item="Silver Coin", c1_number=86, c2_number=25, league="Hardcore",
                    name="Cujo", time=datetime.datetime(2016, 5, 6, 7, 15, 1)))
db.session.add(
    Post(uid=94, c1_item="Exalted Orb", c2_item="Blessed Orb", c1_number=306, c2_number=145, league="Hardcore",
         name="Midnight Rider", time=datetime.datetime(2016, 1, 25, 9, 47, 27)))
db.session.add(Post(uid=95, c1_item="Exalted Orb", c2_item="Cartographer's Chisel", c1_number=104, c2_number=213,
                    league="Hardcore", name="Swerve", time=datetime.datetime(2016, 11, 23, 17, 16, 48)))
db.session.add(Post(uid=96, c1_item="Exalted Orb", c2_item="Chaos Orb", c1_number=250, c2_number=261, league="Hardcore",
                    name="Dancing Madman", time=datetime.datetime(2016, 1, 24, 22, 21, 40)))
db.session.add(
    Post(uid=97, c1_item="Exalted Orb", c2_item="Chromatic Orb", c1_number=79, c2_number=194, league="Hardcore",
         name="Mindless Bobcat", time=datetime.datetime(2016, 4, 19, 8, 21, 1)))
db.session.add(
    Post(uid=98, c1_item="Exalted Orb", c2_item="Divine Orb", c1_number=234, c2_number=121, league="Hardcore",
         name="Tacklebox", time=datetime.datetime(2016, 3, 6, 4, 4, 3)))
db.session.add(
    Post(uid=99, c1_item="Exalted Orb", c2_item="Exalted Orb", c1_number=296, c2_number=180, league="Hardcore",
         name="Dangle", time=datetime.datetime(2016, 2, 12, 12, 58, 37)))
db.session.add(
    Post(uid=100, c1_item="Exalted Orb", c2_item="Gemcutter's Prism", c1_number=121, c2_number=279, league="Hardcore",
         name="Mr. 44", time=datetime.datetime(2016, 12, 14, 16, 34, 58)))
db.session.add(
    Post(uid=101, c1_item="Exalted Orb", c2_item="Jeweller's Orb", c1_number=118, c2_number=197, league="Hardcore",
         name="Take Away", time=datetime.datetime(2016, 9, 13, 18, 26, 58)))
db.session.add(
    Post(uid=102, c1_item="Exalted Orb", c2_item="Orb of Alchemy", c1_number=288, c2_number=74, league="Hardcore",
         name="Dark Horse", time=datetime.datetime(2016, 8, 6, 17, 24, 37)))
db.session.add(
    Post(uid=103, c1_item="Exalted Orb", c2_item="Orb of Alteration", c1_number=113, c2_number=73, league="Hardcore",
         name="Mr. Fabulous", time=datetime.datetime(2016, 8, 27, 3, 4, 45)))
db.session.add(
    Post(uid=104, c1_item="Exalted Orb", c2_item="Orb of Chance", c1_number=106, c2_number=35, league="Hardcore",
         name="Tan Stallion", time=datetime.datetime(2016, 8, 7, 19, 26, 53)))
db.session.add(
    Post(uid=105, c1_item="Exalted Orb", c2_item="Orb of Fusing", c1_number=105, c2_number=211, league="Hardcore",
         name="Day Hawk", time=datetime.datetime(2016, 8, 10, 15, 35, 17)))
db.session.add(
    Post(uid=106, c1_item="Exalted Orb", c2_item="Orb of Regret", c1_number=144, c2_number=254, league="Hardcore",
         name="Mr. Gadget", time=datetime.datetime(2016, 1, 1, 3, 37, 56)))
db.session.add(
    Post(uid=107, c1_item="Exalted Orb", c2_item="Orb of Scouring", c1_number=127, c2_number=242, league="Hardcore",
         name="The China Wall", time=datetime.datetime(2016, 12, 16, 18, 49, 3)))
db.session.add(Post(uid=108, c1_item="Exalted Orb", c2_item="Regal Orb", c1_number=211, c2_number=39, league="Hardcore",
                    name="Desert Haze", time=datetime.datetime(2016, 9, 13, 5, 6, 16)))
db.session.add(Post(uid=109, c1_item="Exalted Orb", c2_item="Vaal Orb", c1_number=142, c2_number=224, league="Hardcore",
                    name="Mr. Lucky", time=datetime.datetime(2016, 4, 19, 11, 9, 17)))
db.session.add(
    Post(uid=110, c1_item="Exalted Orb", c2_item="Perandus Coin", c1_number=233, c2_number=202, league="Hardcore",
         name="The Dude", time=datetime.datetime(2016, 11, 28, 3, 52, 21)))
db.session.add(
    Post(uid=111, c1_item="Exalted Orb", c2_item="Silver Coin", c1_number=240, c2_number=240, league="Hardcore",
         name="Digger", time=datetime.datetime(2016, 9, 19, 2, 51, 7)))
db.session.add(
    Post(uid=112, c1_item="Gemcutter's Prism", c2_item="Blessed Orb", c1_number=43, c2_number=38, league="Hardcore",
         name="Mr. Peppermint", time=datetime.datetime(2016, 8, 23, 13, 49, 45)))
db.session.add(Post(uid=113, c1_item="Gemcutter's Prism", c2_item="Cartographer's Chisel", c1_number=273, c2_number=122,
                    league="Hardcore", name="The Flying Mouse", time=datetime.datetime(2016, 4, 20, 10, 28, 20)))
db.session.add(
    Post(uid=114, c1_item="Gemcutter's Prism", c2_item="Chaos Orb", c1_number=125, c2_number=251, league="Hardcore",
         name="Disco Thunder", time=datetime.datetime(2016, 7, 3, 21, 29, 44)))
db.session.add(
    Post(uid=115, c1_item="Gemcutter's Prism", c2_item="Chromatic Orb", c1_number=81, c2_number=238, league="Hardcore",
         name="Mr. Spy", time=datetime.datetime(2016, 1, 18, 2, 47, 42)))
db.session.add(
    Post(uid=116, c1_item="Gemcutter's Prism", c2_item="Divine Orb", c1_number=251, c2_number=78, league="Hardcore",
         name="The Happy Jock", time=datetime.datetime(2016, 7, 5, 3, 54, 32)))
db.session.add(
    Post(uid=117, c1_item="Gemcutter's Prism", c2_item="Exalted Orb", c1_number=298, c2_number=304, league="Hardcore",
         name="Disco Potato", time=datetime.datetime(2016, 5, 19, 19, 57, 6)))
db.session.add(Post(uid=118, c1_item="Gemcutter's Prism", c2_item="Gemcutter's Prism", c1_number=307, c2_number=199,
                    league="Hardcore", name="Mr. Thanksgiving", time=datetime.datetime(2016, 10, 23, 4, 31, 40)))
db.session.add(
    Post(uid=119, c1_item="Gemcutter's Prism", c2_item="Jeweller's Orb", c1_number=160, c2_number=85, league="Hardcore",
         name="The Howling Swede", time=datetime.datetime(2016, 8, 1, 9, 47, 31)))
db.session.add(
    Post(uid=120, c1_item="Gemcutter's Prism", c2_item="Orb of Alchemy", c1_number=42, c2_number=175, league="Hardcore",
         name="Dr. Cocktail", time=datetime.datetime(2016, 1, 15, 3, 58, 43)))
db.session.add(Post(uid=121, c1_item="Gemcutter's Prism", c2_item="Orb of Alteration", c1_number=279, c2_number=262,
                    league="Hardcore", name="Mr. Wholesome", time=datetime.datetime(2016, 10, 11, 18, 0, 46)))
db.session.add(
    Post(uid=122, c1_item="Gemcutter's Prism", c2_item="Orb of Chance", c1_number=57, c2_number=117, league="Hardcore",
         name="Thrasher", time=datetime.datetime(2016, 9, 5, 5, 42, 13)))
db.session.add(
    Post(uid=123, c1_item="Gemcutter's Prism", c2_item="Orb of Fusing", c1_number=259, c2_number=28, league="Hardcore",
         name="Dredd", time=datetime.datetime(2016, 9, 19, 22, 31, 50)))
db.session.add(
    Post(uid=124, c1_item="Gemcutter's Prism", c2_item="Orb of Regret", c1_number=296, c2_number=217, league="Hardcore",
         name="Mud Pie Man", time=datetime.datetime(2016, 7, 6, 18, 1, 26)))
db.session.add(Post(uid=125, c1_item="Gemcutter's Prism", c2_item="Orb of Scouring", c1_number=199, c2_number=181,
                    league="Hardcore", name="Toe", time=datetime.datetime(2016, 2, 17, 10, 40, 36)))
db.session.add(
    Post(uid=126, c1_item="Gemcutter's Prism", c2_item="Regal Orb", c1_number=68, c2_number=290, league="Hardcore",
         name="Dropkick", time=datetime.datetime(2016, 1, 5, 11, 48, 8)))
db.session.add(
    Post(uid=127, c1_item="Gemcutter's Prism", c2_item="Vaal Orb", c1_number=99, c2_number=28, league="Hardcore",
         name="Mule Skinner", time=datetime.datetime(2016, 1, 22, 3, 7, 29)))
db.session.add(
    Post(uid=128, c1_item="Gemcutter's Prism", c2_item="Perandus Coin", c1_number=46, c2_number=182, league="Hardcore",
         name="Toolmaker", time=datetime.datetime(2016, 2, 21, 17, 17, 14)))
db.session.add(
    Post(uid=129, c1_item="Gemcutter's Prism", c2_item="Silver Coin", c1_number=295, c2_number=278, league="Hardcore",
         name="Drop Stone", time=datetime.datetime(2016, 7, 21, 19, 56, 18)))
db.session.add(
    Post(uid=130, c1_item="Jeweller's Orb", c2_item="Blessed Orb", c1_number=173, c2_number=182, league="Hardcore",
         name="Murmur", time=datetime.datetime(2016, 8, 17, 19, 48, 8)))
db.session.add(Post(uid=131, c1_item="Jeweller's Orb", c2_item="Cartographer's Chisel", c1_number=176, c2_number=21,
                    league="Hardcore", name="Tough Nut", time=datetime.datetime(2016, 10, 13, 21, 13, 34)))
db.session.add(
    Post(uid=132, c1_item="Jeweller's Orb", c2_item="Chaos Orb", c1_number=85, c2_number=143, league="Hardcore",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 3, 22, 1, 51, 26)))
db.session.add(
    Post(uid=133, c1_item="Jeweller's Orb", c2_item="Chromatic Orb", c1_number=188, c2_number=35, league="Hardcore",
         name="Nacho", time=datetime.datetime(2016, 4, 18, 4, 45, 42)))
db.session.add(
    Post(uid=134, c1_item="Jeweller's Orb", c2_item="Divine Orb", c1_number=154, c2_number=29, league="Hardcore",
         name="Trip", time=datetime.datetime(2016, 7, 19, 4, 27, 43)))
db.session.add(
    Post(uid=135, c1_item="Jeweller's Orb", c2_item="Exalted Orb", c1_number=182, c2_number=105, league="Hardcore",
         name="Easy Sweep", time=datetime.datetime(2016, 9, 20, 22, 44, 47)))
db.session.add(
    Post(uid=136, c1_item="Jeweller's Orb", c2_item="Gemcutter's Prism", c1_number=197, c2_number=83, league="Hardcore",
         name="Natural Mess", time=datetime.datetime(2016, 10, 4, 2, 58, 54)))
db.session.add(
    Post(uid=137, c1_item="Jeweller's Orb", c2_item="Jeweller's Orb", c1_number=94, c2_number=73, league="Hardcore",
         name="Troubadour", time=datetime.datetime(2016, 6, 4, 20, 0, 13)))
db.session.add(
    Post(uid=138, c1_item="Jeweller's Orb", c2_item="Orb of Alchemy", c1_number=29, c2_number=157, league="Hardcore",
         name="Electric Player", time=datetime.datetime(2016, 12, 13, 19, 2, 8)))
db.session.add(
    Post(uid=139, c1_item="Jeweller's Orb", c2_item="Orb of Alteration", c1_number=285, c2_number=83, league="Hardcore",
         name="Necromancer", time=datetime.datetime(2016, 10, 15, 1, 34, 39)))
db.session.add(
    Post(uid=140, c1_item="Jeweller's Orb", c2_item="Orb of Chance", c1_number=193, c2_number=86, league="Hardcore",
         name="Turnip King", time=datetime.datetime(2016, 7, 9, 7, 34, 26)))
db.session.add(
    Post(uid=141, c1_item="Jeweller's Orb", c2_item="Orb of Fusing", c1_number=60, c2_number=222, league="Hardcore",
         name="Esquire", time=datetime.datetime(2016, 11, 4, 6, 56, 30)))
db.session.add(
    Post(uid=142, c1_item="Jeweller's Orb", c2_item="Orb of Regret", c1_number=164, c2_number=86, league="Hardcore",
         name="Neophyte Believer", time=datetime.datetime(2016, 1, 10, 8, 48, 57)))
db.session.add(
    Post(uid=143, c1_item="Jeweller's Orb", c2_item="Orb of Scouring", c1_number=121, c2_number=243, league="Hardcore",
         name="Twitch", time=datetime.datetime(2016, 11, 27, 2, 33, 11)))
db.session.add(
    Post(uid=144, c1_item="Jeweller's Orb", c2_item="Regal Orb", c1_number=113, c2_number=216, league="Hardcore",
         name="Fast Draw", time=datetime.datetime(2016, 5, 23, 3, 16, 12)))
db.session.add(
    Post(uid=145, c1_item="Jeweller's Orb", c2_item="Vaal Orb", c1_number=137, c2_number=22, league="Hardcore",
         name="Nessie", time=datetime.datetime(2016, 3, 23, 14, 12, 12)))
db.session.add(
    Post(uid=146, c1_item="Jeweller's Orb", c2_item="Perandus Coin", c1_number=315, c2_number=271, league="Hardcore",
         name="Vagabond Warrior", time=datetime.datetime(2016, 4, 11, 21, 52, 32)))
db.session.add(
    Post(uid=147, c1_item="Jeweller's Orb", c2_item="Silver Coin", c1_number=317, c2_number=170, league="Hardcore",
         name="Flakes", time=datetime.datetime(2016, 1, 6, 19, 32, 33)))
db.session.add(
    Post(uid=148, c1_item="Orb of Alchemy", c2_item="Blessed Orb", c1_number=186, c2_number=222, league="Hardcore",
         name="New Cycle", time=datetime.datetime(2016, 10, 11, 1, 2, 36)))
db.session.add(Post(uid=149, c1_item="Orb of Alchemy", c2_item="Cartographer's Chisel", c1_number=34, c2_number=21,
                    league="Hardcore", name="Voluntary", time=datetime.datetime(2016, 5, 5, 19, 5, 38)))
db.session.add(
    Post(uid=150, c1_item="Orb of Alchemy", c2_item="Chaos Orb", c1_number=194, c2_number=87, league="Hardcore",
         name="Flint", time=datetime.datetime(2016, 7, 17, 19, 26, 26)))
db.session.add(
    Post(uid=151, c1_item="Orb of Alchemy", c2_item="Chromatic Orb", c1_number=303, c2_number=29, league="Hardcore",
         name="Nickname Master", time=datetime.datetime(2016, 5, 7, 19, 58, 55)))
db.session.add(
    Post(uid=152, c1_item="Orb of Alchemy", c2_item="Divine Orb", c1_number=208, c2_number=34, league="Hardcore",
         name="Vortex", time=datetime.datetime(2016, 11, 12, 16, 18, 51)))
db.session.add(
    Post(uid=153, c1_item="Orb of Alchemy", c2_item="Exalted Orb", c1_number=132, c2_number=112, league="Hardcore",
         name="Freak", time=datetime.datetime(2016, 1, 18, 16, 26, 18)))
db.session.add(Post(uid=154, c1_item="Orb of Alchemy", c2_item="Gemcutter's Prism", c1_number=312, c2_number=223,
                    league="Hardcore", name="Nightmare King", time=datetime.datetime(2016, 6, 4, 2, 31, 54)))
db.session.add(
    Post(uid=155, c1_item="Orb of Alchemy", c2_item="Jeweller's Orb", c1_number=31, c2_number=212, league="Hardcore",
         name="Washer", time=datetime.datetime(2016, 11, 26, 13, 22, 36)))
db.session.add(
    Post(uid=156, c1_item="Orb of Alchemy", c2_item="Orb of Alchemy", c1_number=116, c2_number=117, league="Hardcore",
         name="Gas Man", time=datetime.datetime(2016, 10, 15, 6, 21, 56)))
db.session.add(Post(uid=157, c1_item="Orb of Alchemy", c2_item="Orb of Alteration", c1_number=165, c2_number=143,
                    league="Hardcore", name="Night Train", time=datetime.datetime(2016, 7, 2, 5, 11, 16)))
db.session.add(
    Post(uid=158, c1_item="Orb of Alchemy", c2_item="Orb of Chance", c1_number=96, c2_number=279, league="Hardcore",
         name="Waylay Dave", time=datetime.datetime(2016, 10, 20, 13, 28, 17)))
db.session.add(
    Post(uid=159, c1_item="Orb of Alchemy", c2_item="Orb of Fusing", c1_number=31, c2_number=55, league="Hardcore",
         name="Glyph", time=datetime.datetime(2016, 11, 28, 16, 25, 30)))
db.session.add(
    Post(uid=160, c1_item="Orb of Alchemy", c2_item="Orb of Regret", c1_number=300, c2_number=51, league="Hardcore",
         name="Old Man Winter", time=datetime.datetime(2016, 2, 23, 3, 1, 36)))
db.session.add(
    Post(uid=161, c1_item="Orb of Alchemy", c2_item="Orb of Scouring", c1_number=297, c2_number=67, league="Hardcore",
         name="Wheels", time=datetime.datetime(2016, 10, 25, 11, 46, 21)))
db.session.add(
    Post(uid=162, c1_item="Orb of Alchemy", c2_item="Regal Orb", c1_number=87, c2_number=215, league="Hardcore",
         name="Grave Digger", time=datetime.datetime(2016, 2, 18, 6, 17, 5)))
db.session.add(
    Post(uid=163, c1_item="Orb of Alchemy", c2_item="Vaal Orb", c1_number=273, c2_number=152, league="Hardcore",
         name="Old Orange Eyes", time=datetime.datetime(2016, 6, 28, 19, 53, 55)))
db.session.add(
    Post(uid=164, c1_item="Orb of Alchemy", c2_item="Perandus Coin", c1_number=40, c2_number=223, league="Hardcore",
         name="Wooden Man", time=datetime.datetime(2016, 3, 19, 0, 8, 24)))
db.session.add(
    Post(uid=165, c1_item="Orb of Alchemy", c2_item="Silver Coin", c1_number=120, c2_number=43, league="Hardcore",
         name="Guillotine", time=datetime.datetime(2016, 9, 1, 11, 26, 14)))
db.session.add(
    Post(uid=166, c1_item="Orb of Alteration", c2_item="Blessed Orb", c1_number=146, c2_number=219, league="Hardcore",
         name="Old Regret", time=datetime.datetime(2016, 10, 3, 21, 3, 23)))
db.session.add(Post(uid=167, c1_item="Orb of Alteration", c2_item="Cartographer's Chisel", c1_number=125, c2_number=84,
                    league="Hardcore", name="Woo Woo", time=datetime.datetime(2016, 6, 10, 15, 57, 35)))
db.session.add(
    Post(uid=168, c1_item="Orb of Alteration", c2_item="Chaos Orb", c1_number=175, c2_number=255, league="Hardcore",
         name="Gunhawk", time=datetime.datetime(2016, 6, 9, 19, 46, 54)))
db.session.add(
    Post(uid=169, c1_item="Orb of Alteration", c2_item="Chromatic Orb", c1_number=97, c2_number=231, league="Hardcore",
         name="Onion King", time=datetime.datetime(2016, 8, 11, 20, 39, 12)))
db.session.add(
    Post(uid=170, c1_item="Orb of Alteration", c2_item="Divine Orb", c1_number=84, c2_number=259, league="Hardcore",
         name="Yellow Menace", time=datetime.datetime(2016, 11, 4, 14, 2, 39)))
db.session.add(
    Post(uid=171, c1_item="Orb of Alteration", c2_item="Exalted Orb", c1_number=172, c2_number=235, league="Hardcore",
         name="High Kingdom Warrior", time=datetime.datetime(2016, 12, 5, 1, 17, 58)))
db.session.add(Post(uid=172, c1_item="Orb of Alteration", c2_item="Gemcutter's Prism", c1_number=166, c2_number=306,
                    league="Hardcore", name="Osprey", time=datetime.datetime(2016, 5, 21, 21, 25, 0)))
db.session.add(Post(uid=173, c1_item="Orb of Alteration", c2_item="Jeweller's Orb", c1_number=170, c2_number=318,
                    league="Hardcore", name="Zero Charisma", time=datetime.datetime(2016, 2, 26, 15, 45, 45)))
db.session.add(
    Post(uid=174, c1_item="Orb of Alteration", c2_item="Orb of Alchemy", c1_number=60, c2_number=27, league="Hardcore",
         name="Highlander Monk", time=datetime.datetime(2016, 11, 2, 22, 12, 9)))
db.session.add(Post(uid=175, c1_item="Orb of Alteration", c2_item="Orb of Alteration", c1_number=87, c2_number=147,
                    league="Hardcore", name="Overrun", time=datetime.datetime(2016, 1, 3, 7, 17, 21)))
db.session.add(
    Post(uid=176, c1_item="Orb of Alteration", c2_item="Orb of Chance", c1_number=189, c2_number=137, league="Hardcore",
         name="Zesty Dragon", time=datetime.datetime(2016, 8, 1, 22, 39, 45)))
db.session.add(
    Post(uid=177, c1_item="Orb of Alteration", c2_item="Orb of Fusing", c1_number=125, c2_number=60, league="Hardcore",
         name="Zod", time=datetime.datetime(2016, 10, 26, 15, 19, 23)))
db.session.add(
    Post(uid=0, c1_item="Orb of Alteration", c2_item="Orb of Regret", c1_number=133, c2_number=46, league="Hardcore",
         name="101", time=datetime.datetime(2016, 6, 22, 3, 45, 53)))
db.session.add(
    Post(uid=1, c1_item="Orb of Alteration", c2_item="Orb of Scouring", c1_number=228, c2_number=199, league="Hardcore",
         name="Houston", time=datetime.datetime(2016, 8, 9, 20, 32, 8)))
db.session.add(
    Post(uid=2, c1_item="Orb of Alteration", c2_item="Regal Orb", c1_number=49, c2_number=261, league="Hardcore",
         name="Pinball Wizard", time=datetime.datetime(2016, 6, 20, 7, 23, 40)))
db.session.add(
    Post(uid=3, c1_item="Orb of Alteration", c2_item="Vaal Orb", c1_number=72, c2_number=183, league="Hardcore",
         name="Accidental Genius", time=datetime.datetime(2016, 10, 3, 11, 46, 38)))
db.session.add(
    Post(uid=4, c1_item="Orb of Alteration", c2_item="Perandus Coin", c1_number=182, c2_number=216, league="Hardcore",
         name="Hyper", time=datetime.datetime(2016, 1, 25, 3, 38, 1)))
db.session.add(
    Post(uid=5, c1_item="Orb of Alteration", c2_item="Silver Coin", c1_number=181, c2_number=281, league="Hardcore",
         name="Pluto", time=datetime.datetime(2016, 8, 21, 14, 28, 23)))
db.session.add(
    Post(uid=6, c1_item="Orb of Chance", c2_item="Blessed Orb", c1_number=128, c2_number=101, league="Hardcore",
         name="Alpha", time=datetime.datetime(2016, 8, 27, 16, 35, 1)))
db.session.add(Post(uid=7, c1_item="Orb of Chance", c2_item="Cartographer's Chisel", c1_number=265, c2_number=117,
                    league="Hardcore", name="Jester", time=datetime.datetime(2016, 11, 2, 14, 7, 22)))
db.session.add(
    Post(uid=8, c1_item="Orb of Chance", c2_item="Chaos Orb", c1_number=300, c2_number=251, league="Hardcore",
         name="Pogue", time=datetime.datetime(2016, 9, 22, 16, 52, 22)))
db.session.add(
    Post(uid=9, c1_item="Orb of Chance", c2_item="Chromatic Orb", c1_number=86, c2_number=296, league="Hardcore",
         name="Airport Hobo", time=datetime.datetime(2016, 6, 22, 21, 29, 40)))
db.session.add(
    Post(uid=10, c1_item="Orb of Chance", c2_item="Divine Orb", c1_number=189, c2_number=139, league="Hardcore",
         name="Jigsaw", time=datetime.datetime(2016, 7, 19, 0, 5, 46)))
db.session.add(
    Post(uid=11, c1_item="Orb of Chance", c2_item="Exalted Orb", c1_number=136, c2_number=167, league="Hardcore",
         name="Prometheus", time=datetime.datetime(2016, 1, 21, 4, 37, 58)))
db.session.add(
    Post(uid=12, c1_item="Orb of Chance", c2_item="Gemcutter's Prism", c1_number=133, c2_number=120, league="Hardcore",
         name="Bearded Angler", time=datetime.datetime(2016, 2, 14, 2, 38, 25)))
db.session.add(
    Post(uid=13, c1_item="Orb of Chance", c2_item="Jeweller's Orb", c1_number=291, c2_number=64, league="Hardcore",
         name="Joker's Grin", time=datetime.datetime(2016, 12, 7, 20, 19, 1)))
db.session.add(
    Post(uid=14, c1_item="Orb of Chance", c2_item="Orb of Alchemy", c1_number=263, c2_number=239, league="Hardcore",
         name="Psycho Thinker", time=datetime.datetime(2016, 2, 7, 21, 48, 18)))
db.session.add(
    Post(uid=15, c1_item="Orb of Chance", c2_item="Orb of Alteration", c1_number=244, c2_number=74, league="Hardcore",
         name="Beetle King", time=datetime.datetime(2016, 5, 1, 7, 29, 15)))
db.session.add(
    Post(uid=16, c1_item="Orb of Chance", c2_item="Orb of Chance", c1_number=47, c2_number=190, league="Hardcore",
         name="Judge", time=datetime.datetime(2016, 8, 11, 13, 43, 0)))
db.session.add(
    Post(uid=17, c1_item="Orb of Chance", c2_item="Orb of Fusing", c1_number=273, c2_number=259, league="Hardcore",
         name="Pusher", time=datetime.datetime(2016, 3, 20, 16, 11, 4)))
db.session.add(
    Post(uid=18, c1_item="Orb of Chance", c2_item="Orb of Regret", c1_number=119, c2_number=199, league="Hardcore",
         name="Bitmap", time=datetime.datetime(2016, 9, 2, 16, 37, 9)))
db.session.add(
    Post(uid=19, c1_item="Orb of Chance", c2_item="Orb of Scouring", c1_number=108, c2_number=161, league="Hardcore",
         name="Junkyard Dog", time=datetime.datetime(2016, 9, 24, 19, 52, 40)))
db.session.add(
    Post(uid=20, c1_item="Orb of Chance", c2_item="Regal Orb", c1_number=106, c2_number=71, league="Hardcore",
         name="Riff Raff", time=datetime.datetime(2016, 6, 8, 17, 42, 38)))
db.session.add(Post(uid=21, c1_item="Orb of Chance", c2_item="Vaal Orb", c1_number=60, c2_number=112, league="Hardcore",
                    name="Blister", time=datetime.datetime(2016, 6, 22, 13, 35, 45)))
db.session.add(
    Post(uid=22, c1_item="Orb of Chance", c2_item="Perandus Coin", c1_number=261, c2_number=303, league="Hardcore",
         name="K-9", time=datetime.datetime(2016, 12, 7, 12, 8, 53)))
db.session.add(
    Post(uid=23, c1_item="Orb of Chance", c2_item="Silver Coin", c1_number=56, c2_number=283, league="Hardcore",
         name="Roadblock", time=datetime.datetime(2016, 7, 21, 14, 41, 43)))
db.session.add(
    Post(uid=24, c1_item="Orb of Fusing", c2_item="Blessed Orb", c1_number=75, c2_number=63, league="Hardcore",
         name="Bowie", time=datetime.datetime(2016, 5, 11, 15, 3, 14)))
db.session.add(Post(uid=25, c1_item="Orb of Fusing", c2_item="Cartographer's Chisel", c1_number=161, c2_number=196,
                    league="Hardcore", name="Keystone", time=datetime.datetime(2016, 6, 12, 9, 43, 24)))
db.session.add(Post(uid=26, c1_item="Orb of Fusing", c2_item="Chaos Orb", c1_number=62, c2_number=64, league="Hardcore",
                    name="Rooster", time=datetime.datetime(2016, 3, 11, 15, 0, 32)))
db.session.add(
    Post(uid=27, c1_item="Orb of Fusing", c2_item="Chromatic Orb", c1_number=305, c2_number=119, league="Hardcore",
         name="Bowler", time=datetime.datetime(2016, 5, 4, 2, 24, 15)))
db.session.add(
    Post(uid=28, c1_item="Orb of Fusing", c2_item="Divine Orb", c1_number=231, c2_number=288, league="Hardcore",
         name="Kickstart", time=datetime.datetime(2016, 2, 10, 2, 51, 42)))
db.session.add(
    Post(uid=29, c1_item="Orb of Fusing", c2_item="Exalted Orb", c1_number=102, c2_number=232, league="Hardcore",
         name="Sandbox", time=datetime.datetime(2016, 12, 12, 22, 52, 1)))
db.session.add(
    Post(uid=30, c1_item="Orb of Fusing", c2_item="Gemcutter's Prism", c1_number=57, c2_number=303, league="Hardcore",
         name="Breadmaker", time=datetime.datetime(2016, 6, 6, 19, 22, 7)))
db.session.add(
    Post(uid=31, c1_item="Orb of Fusing", c2_item="Jeweller's Orb", c1_number=227, c2_number=152, league="Hardcore",
         name="Kill Switch", time=datetime.datetime(2016, 8, 18, 0, 39, 36)))
db.session.add(
    Post(uid=32, c1_item="Orb of Fusing", c2_item="Orb of Alchemy", c1_number=170, c2_number=145, league="Hardcore",
         name="Scrapper", time=datetime.datetime(2016, 3, 1, 16, 12, 44)))
db.session.add(
    Post(uid=33, c1_item="Orb of Fusing", c2_item="Orb of Alteration", c1_number=80, c2_number=269, league="Hardcore",
         name="Broomspun", time=datetime.datetime(2016, 12, 2, 13, 5, 16)))
db.session.add(
    Post(uid=34, c1_item="Orb of Fusing", c2_item="Orb of Chance", c1_number=108, c2_number=27, league="Hardcore",
         name="Kingfisher", time=datetime.datetime(2016, 9, 12, 17, 7, 38)))
db.session.add(
    Post(uid=35, c1_item="Orb of Fusing", c2_item="Orb of Fusing", c1_number=194, c2_number=289, league="Hardcore",
         name="Screwtape", time=datetime.datetime(2016, 3, 16, 21, 10, 1)))
db.session.add(
    Post(uid=36, c1_item="Orb of Fusing", c2_item="Orb of Regret", c1_number=59, c2_number=304, league="Hardcore",
         name="Buckshot", time=datetime.datetime(2016, 12, 24, 12, 43, 25)))
db.session.add(
    Post(uid=37, c1_item="Orb of Fusing", c2_item="Orb of Scouring", c1_number=271, c2_number=159, league="Hardcore",
         name="Kitchen", time=datetime.datetime(2016, 9, 11, 19, 10, 31)))
db.session.add(
    Post(uid=38, c1_item="Orb of Fusing", c2_item="Regal Orb", c1_number=271, c2_number=310, league="Hardcore",
         name="Sexual Chocolate", time=datetime.datetime(2016, 7, 17, 0, 31, 42)))
db.session.add(
    Post(uid=39, c1_item="Orb of Fusing", c2_item="Vaal Orb", c1_number=156, c2_number=142, league="Hardcore",
         name="Bugger", time=datetime.datetime(2016, 2, 22, 7, 30, 7)))
db.session.add(
    Post(uid=40, c1_item="Orb of Fusing", c2_item="Perandus Coin", c1_number=266, c2_number=212, league="Hardcore",
         name="Knuckles", time=datetime.datetime(2016, 12, 24, 8, 49, 26)))
db.session.add(
    Post(uid=41, c1_item="Orb of Fusing", c2_item="Silver Coin", c1_number=289, c2_number=289, league="Hardcore",
         name="Shadow Chaser", time=datetime.datetime(2016, 11, 21, 13, 25, 36)))
db.session.add(
    Post(uid=42, c1_item="Orb of Regret", c2_item="Blessed Orb", c1_number=250, c2_number=150, league="Hardcore",
         name="Cabbie", time=datetime.datetime(2016, 1, 7, 19, 49, 1)))
db.session.add(Post(uid=43, c1_item="Orb of Regret", c2_item="Cartographer's Chisel", c1_number=194, c2_number=22,
                    league="Hardcore", name="Lady Killer", time=datetime.datetime(2016, 2, 26, 13, 55, 13)))
db.session.add(
    Post(uid=44, c1_item="Orb of Regret", c2_item="Chaos Orb", c1_number=26, c2_number=111, league="Hardcore",
         name="Sherwood Gladiator", time=datetime.datetime(2016, 1, 13, 16, 37, 4)))
db.session.add(
    Post(uid=45, c1_item="Orb of Regret", c2_item="Chromatic Orb", c1_number=305, c2_number=114, league="Hardcore",
         name="Candy Butcher", time=datetime.datetime(2016, 8, 21, 4, 33, 6)))
db.session.add(
    Post(uid=46, c1_item="Orb of Regret", c2_item="Divine Orb", c1_number=151, c2_number=246, league="Hardcore",
         name="Liquid Science", time=datetime.datetime(2016, 8, 8, 14, 46, 48)))
db.session.add(
    Post(uid=47, c1_item="Orb of Regret", c2_item="Exalted Orb", c1_number=41, c2_number=176, league="Hardcore",
         name="Shooter", time=datetime.datetime(2016, 2, 4, 10, 41, 3)))
db.session.add(
    Post(uid=48, c1_item="Orb of Regret", c2_item="Gemcutter's Prism", c1_number=312, c2_number=116, league="Hardcore",
         name="Capital F", time=datetime.datetime(2016, 1, 20, 10, 47, 0)))
db.session.add(
    Post(uid=49, c1_item="Orb of Regret", c2_item="Jeweller's Orb", c1_number=85, c2_number=136, league="Hardcore",
         name="Little Cobra", time=datetime.datetime(2016, 8, 18, 0, 2, 16)))
db.session.add(
    Post(uid=50, c1_item="Orb of Regret", c2_item="Orb of Alchemy", c1_number=156, c2_number=48, league="Hardcore",
         name="Sidewalk Enforcer", time=datetime.datetime(2016, 1, 9, 10, 3, 39)))
db.session.add(
    Post(uid=51, c1_item="Orb of Regret", c2_item="Orb of Alteration", c1_number=247, c2_number=298, league="Hardcore",
         name="Captain Peroxide", time=datetime.datetime(2016, 11, 16, 4, 43, 0)))
db.session.add(
    Post(uid=52, c1_item="Orb of Regret", c2_item="Orb of Chance", c1_number=209, c2_number=124, league="Hardcore",
         name="Little General", time=datetime.datetime(2016, 5, 28, 15, 41, 30)))
db.session.add(
    Post(uid=53, c1_item="Orb of Regret", c2_item="Orb of Fusing", c1_number=187, c2_number=57, league="Hardcore",
         name="Skull Crusher", time=datetime.datetime(2016, 2, 2, 19, 11, 27)))
db.session.add(
    Post(uid=54, c1_item="Orb of Regret", c2_item="Orb of Regret", c1_number=61, c2_number=192, league="Hardcore",
         name="Celtic Charger", time=datetime.datetime(2016, 8, 21, 13, 30, 2)))
db.session.add(
    Post(uid=55, c1_item="Orb of Regret", c2_item="Orb of Scouring", c1_number=271, c2_number=221, league="Hardcore",
         name="Lord Nikon", time=datetime.datetime(2016, 8, 7, 11, 37, 10)))
db.session.add(
    Post(uid=56, c1_item="Orb of Regret", c2_item="Regal Orb", c1_number=289, c2_number=134, league="Hardcore",
         name="Sky Bully", time=datetime.datetime(2016, 8, 4, 13, 1, 17)))
db.session.add(
    Post(uid=57, c1_item="Orb of Regret", c2_item="Vaal Orb", c1_number=105, c2_number=193, league="Hardcore",
         name="Cereal Killer", time=datetime.datetime(2016, 2, 12, 19, 39, 14)))
db.session.add(
    Post(uid=58, c1_item="Orb of Regret", c2_item="Perandus Coin", c1_number=87, c2_number=253, league="Hardcore",
         name="Lord Pistachio", time=datetime.datetime(2016, 2, 14, 18, 11, 2)))
db.session.add(
    Post(uid=59, c1_item="Orb of Regret", c2_item="Silver Coin", c1_number=174, c2_number=149, league="Hardcore",
         name="Slow Trot", time=datetime.datetime(2016, 7, 5, 9, 25, 16)))
db.session.add(
    Post(uid=60, c1_item="Orb of Scouring", c2_item="Blessed Orb", c1_number=169, c2_number=84, league="Hardcore",
         name="Chicago Blackout", time=datetime.datetime(2016, 6, 24, 9, 15, 33)))
db.session.add(Post(uid=61, c1_item="Orb of Scouring", c2_item="Cartographer's Chisel", c1_number=295, c2_number=139,
                    league="Hardcore", name="Mad Irishman", time=datetime.datetime(2016, 1, 11, 0, 52, 22)))
db.session.add(
    Post(uid=62, c1_item="Orb of Scouring", c2_item="Chaos Orb", c1_number=45, c2_number=38, league="Hardcore",
         name="Snake Eyes", time=datetime.datetime(2016, 11, 6, 3, 26, 3)))
db.session.add(
    Post(uid=63, c1_item="Orb of Scouring", c2_item="Chromatic Orb", c1_number=55, c2_number=185, league="Hardcore",
         name="Chocolate Thunder", time=datetime.datetime(2016, 1, 18, 20, 27, 36)))
db.session.add(
    Post(uid=64, c1_item="Orb of Scouring", c2_item="Divine Orb", c1_number=31, c2_number=71, league="Hardcore",
         name="Mad Jack", time=datetime.datetime(2016, 6, 2, 4, 9, 1)))
db.session.add(
    Post(uid=65, c1_item="Orb of Scouring", c2_item="Exalted Orb", c1_number=149, c2_number=146, league="Hardcore",
         name="Snow Hound", time=datetime.datetime(2016, 4, 27, 4, 6, 46)))
db.session.add(
    Post(uid=66, c1_item="Orb of Scouring", c2_item="Gemcutter's Prism", c1_number=176, c2_number=97, league="Hardcore",
         name="Chuckles", time=datetime.datetime(2016, 9, 26, 21, 42, 48)))
db.session.add(
    Post(uid=67, c1_item="Orb of Scouring", c2_item="Jeweller's Orb", c1_number=40, c2_number=88, league="Hardcore",
         name="Mad Rascal", time=datetime.datetime(2016, 7, 24, 12, 38, 37)))
db.session.add(
    Post(uid=68, c1_item="Orb of Scouring", c2_item="Orb of Alchemy", c1_number=165, c2_number=155, league="Hardcore",
         name="Sofa King", time=datetime.datetime(2016, 11, 19, 14, 15, 0)))
db.session.add(
    Post(uid=69, c1_item="Orb of Scouring", c2_item="Orb of Alteration", c1_number=23, c2_number=155, league="Hardcore",
         name="Commando", time=datetime.datetime(2016, 7, 6, 11, 38, 31)))
db.session.add(
    Post(uid=70, c1_item="Orb of Scouring", c2_item="Orb of Chance", c1_number=148, c2_number=60, league="Hardcore",
         name="Manimal", time=datetime.datetime(2016, 4, 10, 18, 13, 33)))
db.session.add(
    Post(uid=71, c1_item="Orb of Scouring", c2_item="Orb of Fusing", c1_number=125, c2_number=249, league="Hardcore",
         name="Speedwell", time=datetime.datetime(2016, 6, 26, 18, 12, 15)))
db.session.add(
    Post(uid=72, c1_item="Orb of Scouring", c2_item="Orb of Regret", c1_number=31, c2_number=83, league="Hardcore",
         name="Cool Whip", time=datetime.datetime(2016, 6, 20, 5, 28, 52)))
db.session.add(
    Post(uid=73, c1_item="Orb of Scouring", c2_item="Orb of Scouring", c1_number=229, c2_number=277, league="Hardcore",
         name="Marbles", time=datetime.datetime(2016, 5, 26, 7, 21, 5)))
db.session.add(
    Post(uid=74, c1_item="Orb of Scouring", c2_item="Regal Orb", c1_number=231, c2_number=58, league="Hardcore",
         name="Spider Fuji", time=datetime.datetime(2016, 7, 1, 1, 11, 37)))
db.session.add(
    Post(uid=75, c1_item="Orb of Scouring", c2_item="Vaal Orb", c1_number=266, c2_number=157, league="Hardcore",
         name="Cosmo", time=datetime.datetime(2016, 2, 25, 9, 1, 5)))
db.session.add(
    Post(uid=76, c1_item="Orb of Scouring", c2_item="Perandus Coin", c1_number=160, c2_number=279, league="Hardcore",
         name="Married Man", time=datetime.datetime(2016, 10, 12, 4, 37, 29)))
db.session.add(
    Post(uid=77, c1_item="Orb of Scouring", c2_item="Silver Coin", c1_number=211, c2_number=65, league="Hardcore",
         name="Springheel Jack", time=datetime.datetime(2016, 1, 20, 14, 14, 33)))
db.session.add(Post(uid=78, c1_item="Regal Orb", c2_item="Blessed Orb", c1_number=165, c2_number=209, league="Hardcore",
                    name="Crash Override", time=datetime.datetime(2016, 6, 10, 0, 36, 27)))
db.session.add(
    Post(uid=79, c1_item="Regal Orb", c2_item="Cartographer's Chisel", c1_number=312, c2_number=108, league="Hardcore",
         name="Marshmallow", time=datetime.datetime(2016, 9, 16, 16, 28, 4)))
db.session.add(Post(uid=80, c1_item="Regal Orb", c2_item="Chaos Orb", c1_number=42, c2_number=253, league="Hardcore",
                    name="Squatch", time=datetime.datetime(2016, 9, 3, 10, 25, 47)))
db.session.add(
    Post(uid=81, c1_item="Regal Orb", c2_item="Chromatic Orb", c1_number=33, c2_number=179, league="Hardcore",
         name="Crash Test", time=datetime.datetime(2016, 7, 16, 18, 23, 2)))
db.session.add(Post(uid=82, c1_item="Regal Orb", c2_item="Divine Orb", c1_number=135, c2_number=64, league="Hardcore",
                    name="Mental", time=datetime.datetime(2016, 2, 23, 3, 23, 35)))
db.session.add(Post(uid=83, c1_item="Regal Orb", c2_item="Exalted Orb", c1_number=165, c2_number=157, league="Hardcore",
                    name="Stacker of Wheat", time=datetime.datetime(2016, 10, 16, 1, 29, 17)))
db.session.add(
    Post(uid=84, c1_item="Regal Orb", c2_item="Gemcutter's Prism", c1_number=70, c2_number=298, league="Hardcore",
         name="Crazy Eights", time=datetime.datetime(2016, 2, 1, 17, 29, 16)))
db.session.add(
    Post(uid=85, c1_item="Regal Orb", c2_item="Jeweller's Orb", c1_number=94, c2_number=138, league="Hardcore",
         name="Mercury Reborn", time=datetime.datetime(2016, 8, 3, 16, 25, 20)))
db.session.add(
    Post(uid=86, c1_item="Regal Orb", c2_item="Orb of Alchemy", c1_number=143, c2_number=127, league="Hardcore",
         name="Sugar Man", time=datetime.datetime(2016, 7, 17, 10, 11, 57)))
db.session.add(
    Post(uid=87, c1_item="Regal Orb", c2_item="Orb of Alteration", c1_number=291, c2_number=199, league="Hardcore",
         name="Criss Cross", time=datetime.datetime(2016, 12, 1, 21, 29, 6)))
db.session.add(
    Post(uid=88, c1_item="Regal Orb", c2_item="Orb of Chance", c1_number=109, c2_number=226, league="Hardcore",
         name="Midas", time=datetime.datetime(2016, 7, 26, 3, 25, 1)))
db.session.add(
    Post(uid=89, c1_item="Regal Orb", c2_item="Orb of Fusing", c1_number=143, c2_number=52, league="Hardcore",
         name="Suicide Jockey", time=datetime.datetime(2016, 7, 20, 14, 34, 9)))
db.session.add(
    Post(uid=90, c1_item="Regal Orb", c2_item="Orb of Regret", c1_number=140, c2_number=40, league="Hardcore",
         name="Cross Thread", time=datetime.datetime(2016, 8, 13, 10, 16, 22)))
db.session.add(
    Post(uid=91, c1_item="Regal Orb", c2_item="Orb of Scouring", c1_number=218, c2_number=39, league="Hardcore",
         name="Midnight Rambler", time=datetime.datetime(2016, 5, 23, 12, 5, 23)))
db.session.add(Post(uid=92, c1_item="Regal Orb", c2_item="Regal Orb", c1_number=227, c2_number=61, league="Hardcore",
                    name="Swampmasher", time=datetime.datetime(2016, 6, 15, 22, 53, 33)))
db.session.add(
    Post(uid=93, c1_item="Regal Orb", c2_item="Vaal Orb", c1_number=280, c2_number=221, league="Hardcore", name="Cujo",
         time=datetime.datetime(2016, 12, 3, 15, 31, 22)))
db.session.add(
    Post(uid=94, c1_item="Regal Orb", c2_item="Perandus Coin", c1_number=70, c2_number=241, league="Hardcore",
         name="Midnight Rider", time=datetime.datetime(2016, 8, 2, 19, 26, 26)))
db.session.add(Post(uid=95, c1_item="Regal Orb", c2_item="Silver Coin", c1_number=157, c2_number=255, league="Hardcore",
                    name="Swerve", time=datetime.datetime(2016, 7, 26, 22, 9, 35)))
db.session.add(Post(uid=96, c1_item="Vaal Orb", c2_item="Blessed Orb", c1_number=83, c2_number=310, league="Hardcore",
                    name="Dancing Madman", time=datetime.datetime(2016, 1, 28, 22, 17, 21)))
db.session.add(
    Post(uid=97, c1_item="Vaal Orb", c2_item="Cartographer's Chisel", c1_number=49, c2_number=253, league="Hardcore",
         name="Mindless Bobcat", time=datetime.datetime(2016, 3, 12, 4, 24, 58)))
db.session.add(Post(uid=98, c1_item="Vaal Orb", c2_item="Chaos Orb", c1_number=89, c2_number=56, league="Hardcore",
                    name="Tacklebox", time=datetime.datetime(2016, 9, 11, 13, 55, 3)))
db.session.add(Post(uid=99, c1_item="Vaal Orb", c2_item="Chromatic Orb", c1_number=281, c2_number=42, league="Hardcore",
                    name="Dangle", time=datetime.datetime(2016, 11, 5, 22, 24, 38)))
db.session.add(Post(uid=100, c1_item="Vaal Orb", c2_item="Divine Orb", c1_number=232, c2_number=64, league="Hardcore",
                    name="Mr. 44", time=datetime.datetime(2016, 3, 14, 4, 18, 53)))
db.session.add(Post(uid=101, c1_item="Vaal Orb", c2_item="Exalted Orb", c1_number=205, c2_number=153, league="Hardcore",
                    name="Take Away", time=datetime.datetime(2016, 10, 26, 3, 35, 3)))
db.session.add(
    Post(uid=102, c1_item="Vaal Orb", c2_item="Gemcutter's Prism", c1_number=228, c2_number=90, league="Hardcore",
         name="Dark Horse", time=datetime.datetime(2016, 2, 3, 18, 14, 37)))
db.session.add(
    Post(uid=103, c1_item="Vaal Orb", c2_item="Jeweller's Orb", c1_number=267, c2_number=194, league="Hardcore",
         name="Mr. Fabulous", time=datetime.datetime(2016, 2, 13, 19, 17, 21)))
db.session.add(
    Post(uid=104, c1_item="Vaal Orb", c2_item="Orb of Alchemy", c1_number=311, c2_number=70, league="Hardcore",
         name="Tan Stallion", time=datetime.datetime(2016, 10, 11, 7, 1, 40)))
db.session.add(
    Post(uid=105, c1_item="Vaal Orb", c2_item="Orb of Alteration", c1_number=67, c2_number=236, league="Hardcore",
         name="Day Hawk", time=datetime.datetime(2016, 12, 3, 16, 51, 25)))
db.session.add(
    Post(uid=106, c1_item="Vaal Orb", c2_item="Orb of Chance", c1_number=319, c2_number=194, league="Hardcore",
         name="Mr. Gadget", time=datetime.datetime(2016, 10, 27, 15, 39, 12)))
db.session.add(
    Post(uid=107, c1_item="Vaal Orb", c2_item="Orb of Fusing", c1_number=109, c2_number=229, league="Hardcore",
         name="The China Wall", time=datetime.datetime(2016, 12, 7, 11, 47, 46)))
db.session.add(
    Post(uid=108, c1_item="Vaal Orb", c2_item="Orb of Regret", c1_number=162, c2_number=204, league="Hardcore",
         name="Desert Haze", time=datetime.datetime(2016, 12, 5, 17, 13, 41)))
db.session.add(
    Post(uid=109, c1_item="Vaal Orb", c2_item="Orb of Scouring", c1_number=220, c2_number=72, league="Hardcore",
         name="Mr. Lucky", time=datetime.datetime(2016, 5, 17, 4, 1, 1)))
db.session.add(Post(uid=110, c1_item="Vaal Orb", c2_item="Regal Orb", c1_number=174, c2_number=94, league="Hardcore",
                    name="The Dude", time=datetime.datetime(2016, 9, 10, 7, 32, 26)))
db.session.add(
    Post(uid=111, c1_item="Vaal Orb", c2_item="Vaal Orb", c1_number=149, c2_number=27, league="Hardcore", name="Digger",
         time=datetime.datetime(2016, 6, 17, 1, 20, 16)))
db.session.add(
    Post(uid=112, c1_item="Vaal Orb", c2_item="Perandus Coin", c1_number=297, c2_number=189, league="Hardcore",
         name="Mr. Peppermint", time=datetime.datetime(2016, 4, 26, 11, 55, 24)))
db.session.add(Post(uid=113, c1_item="Vaal Orb", c2_item="Silver Coin", c1_number=224, c2_number=168, league="Hardcore",
                    name="The Flying Mouse", time=datetime.datetime(2016, 4, 2, 2, 33, 39)))
db.session.add(
    Post(uid=114, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=112, c2_number=58, league="Hardcore",
         name="Disco Thunder", time=datetime.datetime(2016, 8, 19, 22, 57, 41)))
db.session.add(Post(uid=115, c1_item="Perandus Coin", c2_item="Cartographer's Chisel", c1_number=234, c2_number=44,
                    league="Hardcore", name="Mr. Spy", time=datetime.datetime(2016, 3, 17, 1, 2, 14)))
db.session.add(
    Post(uid=116, c1_item="Perandus Coin", c2_item="Chaos Orb", c1_number=20, c2_number=35, league="Hardcore",
         name="The Happy Jock", time=datetime.datetime(2016, 4, 8, 13, 29, 6)))
db.session.add(
    Post(uid=117, c1_item="Perandus Coin", c2_item="Chromatic Orb", c1_number=228, c2_number=82, league="Hardcore",
         name="Disco Potato", time=datetime.datetime(2016, 10, 24, 8, 43, 38)))
db.session.add(
    Post(uid=118, c1_item="Perandus Coin", c2_item="Divine Orb", c1_number=100, c2_number=63, league="Hardcore",
         name="Mr. Thanksgiving", time=datetime.datetime(2016, 12, 13, 8, 34, 23)))
db.session.add(
    Post(uid=119, c1_item="Perandus Coin", c2_item="Exalted Orb", c1_number=283, c2_number=68, league="Hardcore",
         name="The Howling Swede", time=datetime.datetime(2016, 2, 15, 4, 17, 47)))
db.session.add(
    Post(uid=120, c1_item="Perandus Coin", c2_item="Gemcutter's Prism", c1_number=284, c2_number=180, league="Hardcore",
         name="Dr. Cocktail", time=datetime.datetime(2016, 12, 2, 4, 33, 46)))
db.session.add(
    Post(uid=121, c1_item="Perandus Coin", c2_item="Jeweller's Orb", c1_number=85, c2_number=238, league="Hardcore",
         name="Mr. Wholesome", time=datetime.datetime(2016, 6, 14, 1, 40, 48)))
db.session.add(
    Post(uid=122, c1_item="Perandus Coin", c2_item="Orb of Alchemy", c1_number=201, c2_number=285, league="Hardcore",
         name="Thrasher", time=datetime.datetime(2016, 4, 22, 20, 2, 21)))
db.session.add(
    Post(uid=123, c1_item="Perandus Coin", c2_item="Orb of Alteration", c1_number=130, c2_number=100, league="Hardcore",
         name="Dredd", time=datetime.datetime(2016, 7, 18, 1, 33, 3)))
db.session.add(
    Post(uid=124, c1_item="Perandus Coin", c2_item="Orb of Chance", c1_number=55, c2_number=59, league="Hardcore",
         name="Mud Pie Man", time=datetime.datetime(2016, 1, 2, 13, 12, 43)))
db.session.add(
    Post(uid=125, c1_item="Perandus Coin", c2_item="Orb of Fusing", c1_number=49, c2_number=274, league="Hardcore",
         name="Toe", time=datetime.datetime(2016, 12, 21, 20, 58, 50)))
db.session.add(
    Post(uid=126, c1_item="Perandus Coin", c2_item="Orb of Regret", c1_number=269, c2_number=211, league="Hardcore",
         name="Dropkick", time=datetime.datetime(2016, 7, 17, 14, 38, 20)))
db.session.add(
    Post(uid=127, c1_item="Perandus Coin", c2_item="Orb of Scouring", c1_number=104, c2_number=71, league="Hardcore",
         name="Mule Skinner", time=datetime.datetime(2016, 10, 13, 3, 20, 44)))
db.session.add(
    Post(uid=128, c1_item="Perandus Coin", c2_item="Regal Orb", c1_number=291, c2_number=244, league="Hardcore",
         name="Toolmaker", time=datetime.datetime(2016, 12, 14, 20, 27, 57)))
db.session.add(
    Post(uid=129, c1_item="Perandus Coin", c2_item="Vaal Orb", c1_number=239, c2_number=185, league="Hardcore",
         name="Drop Stone", time=datetime.datetime(2016, 11, 21, 20, 12, 24)))
db.session.add(
    Post(uid=130, c1_item="Perandus Coin", c2_item="Blessed Orb", c1_number=271, c2_number=134, league="Hardcore",
         name="Murmur", time=datetime.datetime(2016, 10, 27, 7, 57, 21)))
db.session.add(
    Post(uid=131, c1_item="Perandus Coin", c2_item="Silver Coin", c1_number=261, c2_number=68, league="Hardcore",
         name="Tough Nut", time=datetime.datetime(2016, 6, 16, 13, 12, 12)))
db.session.add(
    Post(uid=132, c1_item="Silver Coin", c2_item="Blessed Orb", c1_number=101, c2_number=97, league="Hardcore",
         name="Drugstore Cowboy", time=datetime.datetime(2016, 4, 23, 16, 19, 45)))
db.session.add(Post(uid=133, c1_item="Silver Coin", c2_item="Cartographer's Chisel", c1_number=207, c2_number=129,
                    league="Hardcore", name="Nacho", time=datetime.datetime(2016, 7, 15, 10, 40, 31)))
db.session.add(Post(uid=134, c1_item="Silver Coin", c2_item="Chaos Orb", c1_number=31, c2_number=219, league="Hardcore",
                    name="Trip", time=datetime.datetime(2016, 6, 1, 1, 48, 14)))
db.session.add(
    Post(uid=135, c1_item="Silver Coin", c2_item="Chromatic Orb", c1_number=58, c2_number=202, league="Hardcore",
         name="Easy Sweep", time=datetime.datetime(2016, 11, 16, 1, 49, 33)))
db.session.add(
    Post(uid=136, c1_item="Silver Coin", c2_item="Divine Orb", c1_number=218, c2_number=40, league="Hardcore",
         name="Natural Mess", time=datetime.datetime(2016, 2, 23, 15, 7, 29)))
db.session.add(
    Post(uid=137, c1_item="Silver Coin", c2_item="Exalted Orb", c1_number=255, c2_number=203, league="Hardcore",
         name="Troubadour", time=datetime.datetime(2016, 6, 7, 19, 1, 23)))
db.session.add(
    Post(uid=138, c1_item="Silver Coin", c2_item="Gemcutter's Prism", c1_number=182, c2_number=267, league="Hardcore",
         name="Electric Player", time=datetime.datetime(2016, 7, 1, 18, 53, 57)))
db.session.add(
    Post(uid=139, c1_item="Silver Coin", c2_item="Jeweller's Orb", c1_number=284, c2_number=116, league="Hardcore",
         name="Necromancer", time=datetime.datetime(2016, 8, 11, 1, 34, 14)))
db.session.add(
    Post(uid=140, c1_item="Silver Coin", c2_item="Orb of Alchemy", c1_number=89, c2_number=118, league="Hardcore",
         name="Turnip King", time=datetime.datetime(2016, 10, 22, 5, 23, 45)))
db.session.add(
    Post(uid=141, c1_item="Silver Coin", c2_item="Orb of Alteration", c1_number=50, c2_number=247, league="Hardcore",
         name="Esquire", time=datetime.datetime(2016, 7, 2, 18, 27, 10)))
db.session.add(
    Post(uid=142, c1_item="Silver Coin", c2_item="Orb of Chance", c1_number=78, c2_number=159, league="Hardcore",
         name="Neophyte Believer", time=datetime.datetime(2016, 5, 2, 1, 43, 5)))
db.session.add(
    Post(uid=143, c1_item="Silver Coin", c2_item="Orb of Fusing", c1_number=39, c2_number=262, league="Hardcore",
         name="Twitch", time=datetime.datetime(2016, 4, 5, 18, 17, 0)))
db.session.add(
    Post(uid=144, c1_item="Silver Coin", c2_item="Orb of Regret", c1_number=200, c2_number=101, league="Hardcore",
         name="Fast Draw", time=datetime.datetime(2016, 10, 23, 8, 29, 19)))
db.session.add(
    Post(uid=145, c1_item="Silver Coin", c2_item="Orb of Scouring", c1_number=287, c2_number=207, league="Hardcore",
         name="Nessie", time=datetime.datetime(2016, 2, 6, 21, 48, 9)))
db.session.add(
    Post(uid=146, c1_item="Silver Coin", c2_item="Regal Orb", c1_number=210, c2_number=131, league="Hardcore",
         name="Vagabond Warrior", time=datetime.datetime(2016, 2, 27, 11, 43, 18)))
db.session.add(Post(uid=147, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=154, c2_number=242, league="Hardcore",
                    name="Flakes", time=datetime.datetime(2016, 12, 5, 5, 29, 49)))
db.session.add(
    Post(uid=148, c1_item="Silver Coin", c2_item="Perandus Coin", c1_number=54, c2_number=310, league="Hardcore",
         name="New Cycle", time=datetime.datetime(2016, 9, 9, 6, 55, 53)))
db.session.add(
    Post(uid=149, c1_item="Silver Coin", c2_item="Vaal Orb", c1_number=149, c2_number=156, league="Hardcore",
         name="Voluntary", time=datetime.datetime(2016, 3, 10, 14, 15, 35)))

db.session.add(
    Post(uid=1, c1_item='Chaos Orb', c2_item='Vaal Orb', c1_number=100, c2_number=200, league='Hardcore', name='Alpha',
         time=datetime.datetime(2016, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Chaos Orb', c2_item='Orb of Fusing', c1_number=100, c2_number=200, league='Hardcore',
         name='Alpha',
         time=datetime.datetime(2016, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Chaos Orb', c2_item='Orb of Alchemy', c1_number=100, c2_number=200, league='Hardcore',
         name='Alpha', time=datetime.datetime(2016, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Chaos Orb', c2_item='Silver Coin', c1_number=800, c2_number=200, league='Hardcore',
         name='Alpha',
         time=datetime.datetime(2016, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Chaos Orb', c2_item='Silver Coin', c1_number=600, c2_number=200, league='Hardcore',
         name='Alpha',
         time=datetime.datetime(2016, 5, 18, 16, 34, 7)))
db.session.add(Post(uid=1, c1_item='Chaos Orb', c2_item='Regal Orb', c1_number=700, c2_number=200, league='Hardcore',
                    name='Alpha', time=datetime.datetime(2016, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Chaos Orb', c2_item='Jeweller\'s Orb', c1_number=100, c2_number=200, league='Hardcore',
         name='Alpha',
         time=datetime.datetime(2016, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Chaos Orb', c2_item='Blessed Orb', c1_number=100, c2_number=200, league='Hardcore',
         name='Alpha', time=datetime.datetime(2016, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Orb of Fusing', c2_item='Orb of Alchemy', c1_number=22, c2_number=42, league='Standard',
         name='Alpha', time=datetime.datetime(2015, 6, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Orb of Fusing', c2_item='Orb of Alchemy', c1_number=25, c2_number=45, league='Hardcore Legacy',
         name='Alpha', time=datetime.datetime(2015, 6, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Orb of Fusing', c2_item='Orb of Alchemy', c1_number=20, c2_number=40, league='Hardcore',
         name='Alpha', time=datetime.datetime(2015, 6, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Orb of Fusing', c2_item='Orb of Alchemy', c1_number=20, c2_number=40, league='Standard',
         name='Alpha', time=datetime.datetime(2015, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=1, c1_item='Silver Coin', c2_item='Orb of Alchemy', c1_number=50, c2_number=40, league='Hardcore',
         name='Alpha', time=datetime.datetime(2015, 5, 18, 16, 34, 7)))

db.session.add(
    Post(uid=2, c1_item='Regal Orb', c2_item='Chaos Orb', c1_number=50, c2_number=300, league='Standard', name='c',
         time=datetime.datetime(2015, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=2, c1_item='Regal Orb', c2_item='Silver Coin', c1_number=7, c2_number=1, league='Standard', name='c',
         time=datetime.datetime(2015, 5, 18, 16, 34, 7)))
db.session.add(
    Post(uid=2, c1_item='Jeweller\'s Orb', c2_item='Blessed Orb', c1_number=7, c2_number=1, league='Standard', name='c',
         time=datetime.datetime(2015, 5, 18, 16, 34, 7)))

db.session.add(
    Post(uid=3, c1_item='Jeweller\'s Orb', c2_item='Blessed Orb', c1_number=400, c2_number=350, league='Standard',
         name='c', time=datetime.datetime.now()))
db.session.add(
    Post(uid=3, c1_item='Jeweller\'s Orb', c2_item='Blessed Orb', c1_number=7, c2_number=1, league='Standard', name='c',
         time=datetime.datetime.now()))
db.session.add(
    Post(uid=3, c1_item='Jeweller\'s Orb', c2_item='Blessed Orb', c1_number=7, c2_number=1, league='Standard', name='c',
         time=datetime.datetime.now()))
db.session.add(
    Post(uid=3, c1_item='Jeweller\'s Orb', c2_item='Blessed Orb', c1_number=7, c2_number=1, league='Standard', name='c',
         time=datetime.datetime.now()))
db.session.add(
    Post(uid=3, c1_item='Jeweller\'s Orb', c2_item='Blessed Orb', c1_number=7, c2_number=1, league='Standard', name='c',
         time=datetime.datetime.now()))
db.session.add(
    Post(uid=3, c1_item='Jeweller\'s Orb', c2_item='Blessed Orb', c1_number=7, c2_number=1, league='Standard', name='c',
         time=datetime.datetime.now()))

db.session.commit()

db.session.add(Currency(cname='Chaos Orb', cid=1))
db.session.add(Currency(cname='Vaal Orb', cid=2))
db.session.add(Currency(cname='Blessed Orb', cid=3))
db.session.add(Currency(cname='Orb of Alchemy', cid=4))
db.session.add(Currency(cname='Cartographer\'s Chisel', cid=5))
db.session.add(Currency(cname='Chromatic Orb', cid=6))
db.session.add(Currency(cname='Divine Orb', cid=7))
db.session.add(Currency(cname='Exalted Orb', cid=8))
db.session.add(Currency(cname='Gemcutter\'s Prism', cid=9))
db.session.add(Currency(cname='Jeweller\'s Orb', cid=10))
db.session.add(Currency(cname='Orb of Alteration', cid=11))
db.session.add(Currency(cname='Orb of Chance', cid=12))
db.session.add(Currency(cname='Orb of Fusing', cid=13))
db.session.add(Currency(cname='Orb of Regret', cid=14))
db.session.add(Currency(cname='Orb of Scouring', cid=15))
db.session.add(Currency(cname='Regal Orb', cid=16))
db.session.add(Currency(cname='Perandus Coin', cid=17))
db.session.add(Currency(cname='Silver Coin', cid=18))
db.session.commit()

# 101
# Houston
# Pinball Wizard
# Accidental Genius
# Hyper
# Pluto
# Alpha
# Jester
# Pogue
# Airport Hobo
# Jigsaw
# Prometheus
# Bearded Angler
# Joker's Grin
# Psycho Thinker
# Beetle King
# Judge
# Pusher
# Bitmap
# Junkyard Dog
# Riff Raff
# Blister
# K-9
# Roadblock
# Bowie
# Keystone
# Rooster
# Bowler
# Kickstart
# Sandbox
# Breadmaker
# Kill Switch
# Scrapper
# Broomspun
# Kingfisher
# Screwtape
# Buckshot
# Kitchen
# Sexual Chocolate
# Bugger
# Knuckles
# Shadow Chaser
# Cabbie
# Lady Killer
# Sherwood Gladiator
# Candy Butcher
# Liquid Science
# Shooter
# Capital F
# Little Cobra
# Sidewalk Enforcer
# Captain Peroxide
# Little General
# Skull Crusher
# Celtic Charger
# Lord Nikon
# Sky Bully
# Cereal Killer
# Lord Pistachio
# Slow Trot
# Chicago Blackout
# Mad Irishman
# Snake Eyes
# Chocolate Thunder
# Mad Jack
# Snow Hound
# Chuckles
# Mad Rascal
# Sofa King
# Commando
# Manimal
# Speedwell
# Cool Whip
# Marbles
# Spider Fuji
# Cosmo
# Married Man
# Springheel Jack
# Crash Override
# Marshmallow
# Squatch
# Crash Test
# Mental
# Stacker of Wheat
# Crazy Eights
# Mercury Reborn
# Sugar Man
# Criss Cross
# Midas
# Suicide Jockey
# Cross Thread
# Midnight Rambler
# Swampmasher
# Cujo
# Midnight Rider
# Swerve
# Dancing Madman
# Mindless Bobcat
# Tacklebox
# Dangle
# Mr. 44
# Take Away
# Dark Horse
# Mr. Fabulous
# Tan Stallion
# Day Hawk
# Mr. Gadget
# The China Wall
# Desert Haze
# Mr. Lucky
# The Dude
# Digger
# Mr. Peppermint
# The Flying Mouse
# Disco Thunder
# Mr. Spy
# The Happy Jock
# Disco Potato
# Mr. Thanksgiving
# The Howling Swede
# Dr. Cocktail
# Mr. Wholesome
# Thrasher
# Dredd
# Mud Pie Man
# Toe
# Dropkick
# Mule Skinner
# Toolmaker
# Drop Stone
# Murmur
# Tough Nut
# Drugstore Cowboy
# Nacho
# Trip
# Easy Sweep
# Natural Mess
# Troubadour
# Electric Player
# Necromancer
# Turnip King
# Esquire
# Neophyte Believer
# Twitch
# Fast Draw
# Nessie
# Vagabond Warrior
# Flakes
# New Cycle
# Voluntary
# Flint
# Nickname Master
# Vortex
# Freak
# Nightmare King
# Washer
# Gas Man
# Night Train
# Waylay Dave
# Glyph
# Old Man Winter
# Wheels
# Grave Digger
# Old Orange Eyes
# Wooden Man
# Guillotine
# Old Regret
# Woo Woo
# Gunhawk
# Onion King
# Yellow Menace
# High Kingdom Warrior
# Osprey
# Zero Charisma
# Highlander Monk
# Overrun
# Zesty Dragon
# Zod
#
