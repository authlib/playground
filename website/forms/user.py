from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField


class AuthenticateForm(FlaskForm):
    username = StringField()
    password = PasswordField()
