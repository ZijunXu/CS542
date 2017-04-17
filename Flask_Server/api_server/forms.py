from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField, FloatField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
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
    username = StringField('Username', validators=[Length(1, 64)])
    email = StringField('Email Address', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('New Password',
                             validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Repeat Password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already used')


class PostTradeForm(FlaskForm):
    user_id = IntegerField('User ID')
    c1_item = StringField('Item1', validators=[Length(1, 64)])  # The item user wants to sell
    c2_item = StringField('Item2', validators=[Length(1, 64)])  # The item user wants to get
    c1_number = IntegerField('Item1 Qty', validators=[NumberRange(min=1, max=999)])
    c2_number = IntegerField('Item2 Qty', validators=[NumberRange(min=1, max=999)])


class UserHistoryForm(FlaskForm):
    user_id = IntegerField('User ID')
    item_name = StringField('Item', validators=[Length(1, 64)])


class CurrencySearchForm(FlaskForm):
    currency_name = StringField('Currency', validators=[DataRequired(), Length(1, 64)])


class ItemQueryForm(FlaskForm):
    name = StringField('Item Name', validators=[Length(1, 64)])
    typeLine = StringField('Item Type Line', validators=[Length(1, 64)])
    league = StringField('League', validators=[Length(1, 64)])

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
    # need a better methods
    lower_bound_explicitMods = FloatField('Explicit Mods', validators=[Length(1, 64)])
    upper_bound_explicitMods = FloatField('Explicit Mods', validators=[Length(1, 64)])
    explicitMods = StringField('Item explicitMods', validators=[Length(1, 64)])