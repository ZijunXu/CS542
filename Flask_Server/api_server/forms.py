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
    new_password = PasswordField('New Password',
                                 validators=[EqualTo('confirm_new_password', message='Passwords must match'),
                                             Optional()])
    confirm_new_password = PasswordField('Repeat Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already used')

    def validate_current_password(self, field):
        temp = User.query.filter_by(id=g.user.id).first()
        if not temp.verify_password(field.data):
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
    name = StringField('Item Name', validators=[Length(1, 64), Optional()], default=None)
    type = StringField('Item Type', validators=[Length(1, 64), Optional()], default=None)
    typeLine = StringField('Item Type Line', validators=[Length(1, 64), Optional()], default=None)
    league = StringField('League', validators=[Length(1, 64)], default=None)

    currency_name = StringField('Currency Name', validators=[Length(1, 64), Optional()], default=None)
    min_price = FloatField('Min price', validators=[NumberRange(0, 1000), Optional()], default=None)
    max_price = FloatField('Max price', validators=[NumberRange(0, 1000), Optional()], default=None)

    corrupted = BooleanField('Item Corrupted', validators=[Optional()], default=None)
    verified = BooleanField('Item Verified', validators=[Optional()], default=None)
    identified = BooleanField('Item Identified', validators=[Optional()], default=None)

    min_ilvl = IntegerField('Min Item Level', validators=[NumberRange(0, 100), Optional()], default=None)
    max_ilvl = IntegerField('Max Item Level', validators=[NumberRange(0, 100), Optional()], default=None)

    min_socket_number = IntegerField('Min Socket Number', validators=[NumberRange(0, 6), Optional()], default=None)
    max_socket_number = IntegerField('Max Socket Number', validators=[NumberRange(0, 6), Optional()], default=None)

    min_link_number = IntegerField('Min Link Number', validators=[NumberRange(0, 6), Optional()], default=None)
    max_link_number = IntegerField('Max Link Number', validators=[NumberRange(0, 6), Optional()], default=None)

    str_socket = IntegerField('STR Sockets Number', validators=[NumberRange(0, 6), Optional()], default=None)
    dex_socket = IntegerField('DEX Sockets Number', validators=[NumberRange(0, 6), Optional()], default=None)
    int_socket = IntegerField('INT Sockets Number', validators=[NumberRange(0, 6), Optional()], default=None)
    other_socket = IntegerField('White Sockets Number', validators=[NumberRange(0, 6), Optional()],
                                    default=None)

    supported = BooleanField('Support Skill Gem', validators=[Optional()], default=None)

    # inside the requirement of the document in mongodb
    min_requirements_int = IntegerField('Min INT Requirement', validators=[NumberRange(0, 500), Optional()],
                                        default=None)
    max_requirements_int = IntegerField('Max INT Requirement', validators=[NumberRange(0, 500), Optional()],
                                        default=None)
    min_requirements_dex = IntegerField('Min DEX Requirement', validators=[NumberRange(0, 500), Optional()],
                                        default=None)
    max_requirements_dex = IntegerField('Max DEX Requirement', validators=[NumberRange(0, 500), Optional()],
                                        default=None)
    min_requirements_str = IntegerField('Min STR Requirement', validators=[NumberRange(0, 500), Optional()],
                                        default=None)
    max_requirements_str = IntegerField('Max STR Requirement', validators=[NumberRange(0, 500), Optional()],
                                        default=None)
    min_requirements_lvl = IntegerField('Min Level Requirement', validators=[NumberRange(0, 100), Optional()],
                                        default=None)
    max_requirements_lvl = IntegerField('Max Level Requirement', validators=[NumberRange(0, 100), Optional()],
                                        default=None)

    # inside the properties of the document in mongodb
    # for weapon
    min_physical_damage = FloatField('Physical Damage', validators=[NumberRange(0, 1000), Optional()], default=None)
    max_physical_damage = FloatField('Physical Damage', validators=[NumberRange(0, 1000), Optional()], default=None)
    min_elemental_damage = FloatField('Elemental Damage', validators=[NumberRange(0, 1000), Optional()], default=None)
    max_elemental_damage = FloatField('Elemental Damage', validators=[NumberRange(0, 1000), Optional()], default=None)
    min_critical_strike_chance = FloatField('Critical Strike Chance', validators=[NumberRange(0, 1000), Optional()],
                                            default=None)
    max_critical_strike_chance = FloatField('Critical Strike Chance', validators=[NumberRange(0, 1000), Optional()],
                                            default=None)
    min_attacks_per_second = FloatField('Attacks per Second', validators=[NumberRange(0, 1000), Optional()],
                                        default=None)
    max_attacks_per_second = FloatField('Attacks per Second', validators=[NumberRange(0, 1000), Optional()],
                                        default=None)

    # for armour
    min_armour = FloatField('Min Armour', validators=[NumberRange(0, 1500), Optional()], default=None)
    max_armour = FloatField('Max Armour', validators=[NumberRange(0, 1500), Optional()], default=None)
    min_evasion = FloatField('Min Evasion', validators=[NumberRange(0, 1500), Optional()], default=None)
    max_evasion = FloatField('Max Evasion', validators=[NumberRange(0, 1500), Optional()], default=None)
    min_shield = FloatField('Min Shield', validators=[NumberRange(0, 1500), Optional()])
    max_shield = FloatField('Max Shield', validators=[NumberRange(0, 1500), Optional()])

    min_quality = FloatField('Min Quality', validators=[NumberRange(0, 100), Optional()], default=None)
    max_quality = FloatField('Max Quality', validators=[NumberRange(0, 100), Optional()], default=None)

    # there is a lot of them
    Mods_content = FieldList(FormField(Mods), min_entries=0)
    mods_name = StringField('Mods Name', validators=[Length(1, 64), Optional()], default=None)
    mods_upper_bound = FloatField('Min', validators=[NumberRange(0, 1500), Optional()], default=None)
    mods_lower_bound = FloatField('Max', validators=[NumberRange(0, 1500), Optional()], default=None)
