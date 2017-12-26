from wtforms.fields import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import StopValidation
from .base import BaseForm
from ..models import db, User
from ..auth import login


class AuthenticateForm(BaseForm):
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(AuthenticateForm, self).__init__(*args, **kwargs)
        self._user = None

    def validate_password(self, field):
        email = self.email.data.lower()
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(field.data):
            raise StopValidation('Email or password is invalid.')
        self._user = user

    def login(self):
        if self._user:
            login(self._user, True)


class UserCreationForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

    def validate_email(self, field):
        email = field.data.lower()
        user = User.query.filter_by(email=email).first()
        if user:
            raise StopValidation('Email has been registered.')

    def signup(self):
        name = self.name.data
        email = self.email.data.lower()
        user = User(name=name, email=email)
        user.password = self.password.data
        with db.auto_commit():
            db.session.add(user)
        login(user, True)
        return user
