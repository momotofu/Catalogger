from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import validators

class LoginForm(FlaskForm):
    email = StringField(
                ('email',
                [validators.required('i.e. john@smith.com'),
                validators.Email('Please enter a valid email address')]))
    password = PasswordField('password', [validators.required('password yes')])
