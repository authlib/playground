from wtforms.fields import (
    StringField,
    TextAreaField,
    BooleanField,
    SelectMultipleField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.validators import StopValidation
from werkzeug.security import gen_salt
from .base import BaseForm
from ..models import db, OAuth2Client


class ClientCreationForm(BaseForm):
    name = StringField(validators=[DataRequired()])
    is_confidential = BooleanField()
    redirect_uris = TextAreaField()
    website = StringField()
    allowed_scopes = SelectMultipleField()
    allowed_grants = SelectMultipleField()

    def save(self):
        name = self.name.data
        is_confidential = self.is_confidential.data

        client_id = gen_salt(48)
        if is_confidential:
            client_secret = gen_salt(78)
        else:
            client_secret = None

        client = OAuth2Client(
            client_id=client_id,
            client_secret=client_secret,
            name=name,
            is_confidential=is_confidential,
        )
        with db.auto_commit():
            db.session.add(client)
        return client
