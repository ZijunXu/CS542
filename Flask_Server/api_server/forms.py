from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from .database import User


class LoginForm(FlaskForm):
    username = StringField('UserID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(1, 64)])
    email = StringField('Email Address', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already used')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValueError('Username already used')


class ItemQueryForm(FlaskForm):
    name = StringField('Itemname', validators=[Length(1, 64)])

    corrupted = BooleanField('Item Corrupted', validators=[DataRequired()])
    verified = BooleanField('Item Verified', validators=[DataRequired()])
    identified = BooleanField('Item Identified', validators=[DataRequired()])

    typeLine = StringField('Item Type Line', validators=[Length(1, 64)])
    ilvl = StringField('Item Level', validators=[Length(1, 64)])

    supported = BooleanField('Support Skill Gem', validators=[DataRequired()])

    socketnumber = StringField('Socket Number', validators=[Length(1, 64)])

    requirements_int = StringField('INT Requirement', validators=[Length(1, 64)])
    requirements_dex = StringField('DEX Requirement', validators=[Length(1, 64)])
    requirements_str = StringField('STR Requirement', validators=[Length(1, 64)])
    requirements_lvl = StringField('LVL Requirement', validators=[Length(1, 64)])

    league = StringField('League', validators=[Length(1, 64)])

    explicitMods = StringField('Explicit Mods', validators=[Length(1, 64)])
