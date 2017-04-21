from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField, FloatField, FieldList, FormField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from .database import User


class LoginForm(FlaskForm):
    username = StringField('UserID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[Length(1, 64)])
    email = StringField('Email Address', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('New Password',
                             validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Repeat Password', validators=[DataRequired()])
    accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already used')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValueError('Username already used')


class UpdateForm(FlaskForm):
    email = StringField('Email Address', validators=[Length(1, 64), Email(), Optional()])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[EqualTo('confirm_password', message='Passwords must match'), Optional()])
    confirm_new_password = PasswordField('Repeat Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already used')

    def validate_current_password(self, field):
        temp = User.query.filter_by(id=g.user.id).first()
        if not temp.verify_password(field):
            raise ValueError('Wrong Password')


class PostTradeForm(FlaskForm):
    user_name = StringField('Game ID', validators=[DataRequired(), Length(1, 64)])  # USER NAME IN GAME
    c1_item = StringField('Currency 1', validators=[DataRequired(), Length(1, 64)])  # The item user wants to sell
    c2_item = StringField('Currency 2', validators=[DataRequired(), Length(1, 64)])  # The item user wants to get
    c1_number = IntegerField('Currency 1 Qty', validators=[DataRequired(), NumberRange(min=1, max=999)])
    c2_number = IntegerField('Currency 2 Qty', validators=[DataRequired(), NumberRange(min=1, max=999)])
    league = StringField('League', validators=[DataRequired(), Length(1, 64)])


class UserHistoryForm(FlaskForm):
    user_id = IntegerField('User ID')
    item_name = StringField('Item', validators=[Length(1, 64)])


class CurrencySearchForm(FlaskForm):
    league = StringField('League', validators=[DataRequired(), Length(1, 64)])
    c1_item = StringField('Currency 1', validators=[DataRequired(), Length(1, 64)])
    c2_item = StringField('Currency 2', validators=[DataRequired(), Length(1, 64)])


class Mods(FlaskForm):
    mods_name = StringField('Mods Name', validators=[Length(1, 64)])
    mods_upper_bound = FloatField('Min', validators=[NumberRange(0, 1500)])
    mods_lower_bound = FloatField('Max', validators=[NumberRange(0, 1500)])


class ItemQueryForm(FlaskForm):
    name = StringField('Item Name', validators=[Length(1, 64)])
    typeLine = StringField('Item Type Line', validators=[Length(1, 64)])
    league = StringField('League', validators=[Length(1, 64)])

    currency_name = StringField('Currency Name', validators=[Length(1, 64)])
    min_price = FloatField('Min price', validators=[NumberRange(0, 1000)])
    max_price = FloatField('Max price', validators=[NumberRange(0, 1000)])

    corrupted = BooleanField('Item Corrupted', validators=[DataRequired()])
    verified = BooleanField('Item Verified', validators=[DataRequired()])
    identified = BooleanField('Item Identified', validators=[DataRequired()])

    min_ilvl = IntegerField('Min Item Level', validators=[NumberRange(0, 100)])
    max_ilvl = IntegerField('Max Item Level', validators=[NumberRange(0, 100)])

    min_socket_number = IntegerField('Min Socket Number', validators=[NumberRange(0, 6)])
    max_socket_number = IntegerField('Max Socket Number', validators=[NumberRange(0, 6)])

    min_link_number = IntegerField('Min Link Number', validators=[NumberRange(0, 6)])
    max_link_number = IntegerField('Max Link Number', validators=[NumberRange(0, 6)])

    min_str_socket = IntegerField('Min STR Sockets Number', validators=[NumberRange(0, 6)])
    min_dex_socket = IntegerField('Min DEX Sockets Number', validators=[NumberRange(0, 6)])
    min_int_socket = IntegerField('Min INT Sockets Number', validators=[NumberRange(0, 6)])
    min_other_socket = IntegerField('Min White Sockets Number', validators=[NumberRange(0, 6)])

    supported = BooleanField('Support Skill Gem', validators=[DataRequired()])

    # inside the requirement of the document in mongodb
    min_requirements_int = IntegerField('Min INT Requirement', validators=[NumberRange(0, 500)])
    max_requirements_int = IntegerField('Max INT Requirement', validators=[NumberRange(0, 500)])
    min_requirements_dex = IntegerField('Min DEX Requirement', validators=[NumberRange(0, 500)])
    max_requirements_dex = IntegerField('Max DEX Requirement', validators=[NumberRange(0, 500)])
    min_requirements_str = IntegerField('Min STR Requirement', validators=[NumberRange(0, 500)])
    max_requirements_str = IntegerField('Max STR Requirement', validators=[NumberRange(0, 500)])
    min_requirements_lvl = IntegerField('Min Level Requirement', validators=[NumberRange(0, 100)])
    max_requirements_lvl = IntegerField('Max Level Requirement', validators=[NumberRange(0, 100)])

    # inside the properties of the document in mongodb
    # for weapon
    physical_damage = FloatField('Physical Damage', validators=[NumberRange(0, 1000)])
    elemental_damage = FloatField('Elemental Damage', validators=[NumberRange(0, 1000)])
    critical_strike_chance = FloatField('Critical Strike Chance', validators=[NumberRange(0, 100)])
    attacks_per_Second = FloatField('Attacks per Second', validators=[NumberRange(0, 10)])

    # for armour
    min_armour = FloatField('Min Armour', validators=[NumberRange(0, 1500)])
    max_armour = FloatField('Max Armour', validators=[NumberRange(0, 1500)])
    min_evasion = FloatField('Min Evasion', validators=[NumberRange(0, 1500)])
    max_evasion = FloatField('Max Evasion', validators=[NumberRange(0, 1500)])
    min_shield = FloatField('Min Shield', validators=[NumberRange(0, 1500)])
    max_shield = FloatField('Max Shield', validators=[NumberRange(0, 1500)])

    # there is a lot of them
    Mods_content = FieldList(FormField(Mods), min_entries=0)