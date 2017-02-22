from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from .database import User


class LoginForm(FlaskForm):
    username = StringField('UserID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(1,64)])
    email = StringField('Email Address', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])

    def validata_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already used')

    def validata_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValueError('Username already used')
