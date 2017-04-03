from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
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


class PostTradeForm(FlaskForm):
    c1_item = StringField('Item1', validators=[NumberRange(min=1, max=999)])   # The item user wants to sell
    c2_item = StringField('Item2', validators=[NumberRange(min=1, max=999)])     # The item user wants to get
    c1_number = IntegerField('Item1 Qty', validators=[Length(1, 64)])
    c2_number = IntegerField('Item2 Qty', validators=[Length(1, 64)])


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
