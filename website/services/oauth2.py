from authlib.flask.oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.specs.rfc6749.grants import (
    AuthorizationCodeGrant as _AuthorizationCodeGrant,
    ImplicitGrant as _ImplicitGrant,
    ResourceOwnerPasswordCredentialsGrant as _PasswordGrant,
    ClientCredentialsGrant as _ClientCredentialsGrant,
    RefreshTokenGrant as _RefreshTokenGrant,
)
from authlib.specs.rfc7009 import RevocationEndpoint as _RevocationEndpoint
from werkzeug.security import gen_salt
from ..models import (
    db, User,
    OAuth2Client,
    OAuth2AuthorizationCode,
    OAuth2Token,
)


class AuthorizationCodeGrant(_AuthorizationCodeGrant):
    def create_authorization_code(self, client, user, **kwargs):
        code = gen_salt(48)
        item = OAuth2AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=kwargs.get('redirect_uri', ''),
            scope=kwargs.get('scope', ''),
            user_id=user.id,
        )
        db.session.add(item)
        db.session.commit()
        return code

    def parse_authorization_code(self, code, client):
        item = OAuth2AuthorizationCode.query.filter_by(
            code=code, client_id=client.client_id).first()
        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        db.session.delete(authorization_code)
        db.session.commit()

    def create_access_token(self, token, client, authorization_code):
        item = OAuth2Token(
            client_id=client.client_id,
            user_id=authorization_code.user_id,
            **token
        )
        db.session.add(item)
        db.session.commit()
        token['user_id'] = authorization_code.user_id


class ImplicitGrant(_ImplicitGrant):
    def create_access_token(self, token, client, grant_user):
        item = OAuth2Token(
            client_id=client.client_id,
            user_id=grant_user.id,
            **token
        )
        db.session.add(item)
        db.session.commit()


class PasswordGrant(_PasswordGrant):
    def authenticate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user.check_password(password):
            return user

    def create_access_token(self, token, client, user):
        item = OAuth2Token(
            client_id=client.client_id,
            user_id=user.id,
            **token
        )
        db.session.add(item)
        db.session.commit()
        token['user_id'] = user.id


class ClientCredentialsGrant(_ClientCredentialsGrant):
    def create_access_token(self, token, client):
        item = OAuth2Token(
            client_id=client.client_id,
            user_id=client.user_id,
            **token
        )
        db.session.add(item)
        db.session.commit()


class RefreshTokenGrant(_RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        item = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if item and not item.is_refresh_token_expired():
            return item

    def create_access_token(self, token, authenticated_token):
        item = OAuth2Token(
            client_id=authenticated_token.client_id,
            user_id=authenticated_token.user_id,
            **token
        )
        db.session.add(item)
        db.session.delete(authenticated_token)
        db.session.commit()


class RevocationEndpoint(_RevocationEndpoint):
    def query_token(self, token, token_type_hint, client):
        q = OAuth2Token.query.filter_by(client_id=client.client_id)
        if token_type_hint == 'access_token':
            return q.filter_by(access_token=token).first()
        elif token_type_hint == 'refresh_token':
            return q.filter_by(refresh_token=token).first()
        # without token_type_hint
        item = q.filter_by(access_token=token).first()
        if item:
            return item
        return q.filter_by(refresh_token=token).first()

    def invalidate_token(self, token):
        db.session.delete(token)
        db.session.commit()


authorization = AuthorizationServer(OAuth2Client)

# support all grants
authorization.register_grant_endpoint(AuthorizationCodeGrant)
authorization.register_grant_endpoint(ImplicitGrant)
authorization.register_grant_endpoint(PasswordGrant)
authorization.register_grant_endpoint(ClientCredentialsGrant)
authorization.register_grant_endpoint(RefreshTokenGrant)

# support revocation
authorization.register_revoke_token_endpoint(RevocationEndpoint)

# scopes definition
scopes = {
    'email': 'Client can get your email address.',
    'connects': 'Client can know your connected networks.'
}

# protect resource
require_oauth = ResourceProtector(OAuth2Token.query_token)
