from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import validators

class LoginForm(FlaskForm):
    email = StringField('email', [validators.required('i.e. john@smith.com')])
    password = PasswordField('password', [validators.required('password yes')])
