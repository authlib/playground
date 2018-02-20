from wtforms.fields import (
    StringField,
    TextAreaField,
    BooleanField,
    SelectMultipleField
)
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired
from werkzeug.security import gen_salt
from .base import BaseForm
from ..services.oauth2 import scopes
from ..models import db, OAuth1Client, OAuth2Client

SCOPES = [(k, k) for k in scopes]
GRANTS = [
    ('authorization_code', 'Authorization Code'),
    ('implicit', 'Implicit'),
    ('password', 'Password'),
    ('client_credentials', 'Client Credentials')
]


class Client1Form(BaseForm):
    name = StringField(validators=[DataRequired()])
    website = URLField()
    default_redirect_uri = URLField()

    def update(self, client):
        client.name = self.name.data
        client.website = self.website.data
        client.default_redirect_uri = self.default_redirect_uri.data
        with db.auto_commit():
            db.session.add(client)
        return client

    def save(self, user):
        name = self.name.data
        client_id = gen_salt(48)
        client_secret = gen_salt(78)

        client = OAuth1Client(
            user_id=user.id,
            client_id=client_id,
            client_secret=client_secret,
            name=name,
            default_redirect_uri=self.default_redirect_uri.data,
            website=self.website.data,
        )
        with db.auto_commit():
            db.session.add(client)
        return client


class OAuth2ClientWrapper(object):
    def __init__(self, client):
        self._client = client
        self.name = client.name
        self.website = client.website
        self.is_confidential = client.is_confidential
        self.redirect_uris = client.redirect_uris
        self.default_redirect_uri = client.default_redirect_uri
        self.allowed_scopes = client.allowed_scopes.split()
        self.allowed_grants = client.allowed_grants.split()


class Client2Form(BaseForm):
    name = StringField(validators=[DataRequired()])
    website = URLField()
    is_confidential = BooleanField('Confidential Client')
    redirect_uris = TextAreaField()
    default_redirect_uri = URLField()
    allowed_scopes = SelectMultipleField(choices=SCOPES)
    allowed_grants = SelectMultipleField(choices=GRANTS)

    def update(self, client):
        client.name = self.name.data
        client.website = self.website.data
        client.is_confidential = self.is_confidential.data
        client.redirect_uris = self.redirect_uris.data
        client.default_redirect_uri = self.default_redirect_uri.data
        client.allowed_scopes = ' '.join(self.allowed_scopes.data)
        client.allowed_grants = ' '.join(self.allowed_grants.data)
        with db.auto_commit():
            db.session.add(client)
        return client

    def save(self, user):
        name = self.name.data
        is_confidential = self.is_confidential.data

        client_id = gen_salt(48)
        if is_confidential:
            client_secret = gen_salt(78)
        else:
            client_secret = ''

        client = OAuth2Client(
            user_id=user.id,
            client_id=client_id,
            client_secret=client_secret,
            name=name,
            is_confidential=is_confidential,
            default_redirect_uri=self.default_redirect_uri.data,
            website=self.website.data,
            allowed_scopes=' '.join(self.allowed_scopes.data),
            allowed_grants=' '.join(self.allowed_grants.data),
        )
        with db.auto_commit():
            db.session.add(client)
        return client
