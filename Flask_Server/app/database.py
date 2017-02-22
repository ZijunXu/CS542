from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
from . import login_manager


class User(db.Model, flask_login.UserMixin):
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


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)