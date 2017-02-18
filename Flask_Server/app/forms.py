from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    userId = StringField('UserID', validators=[DataRequired()])
    userPW = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
