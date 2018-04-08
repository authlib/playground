from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func,
    create_revocation_endpoint,
    create_bearer_token_validator,
)
from authlib.specs.rfc6749 import grants
from authlib.specs.oidc import grants as oidc
from werkzeug.security import gen_salt
from .models import (
    OAuth2Client,
    OAuth2AuthorizationCode,
    OAuth2Token,
)
from ..models import db, User

__all__ = ['authorization', 'require_oauth', 'scopes', 'config_service']


class CodeGrantMixin(object):
    def create_authorization_code(self, client, user, request):
        code = gen_salt(48)
        item = OAuth2AuthorizationCode(
            code=code,
            client_id=client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
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

    def authenticate_user(self, authorization_code):
        return User.query.get(authorization_code.user_id)


class OpenIDCodeGrant(CodeGrantMixin, oidc.OpenIDCodeGrant):
    pass


class OpenIDHybridGrant(CodeGrantMixin, oidc.OpenIDHybridGrant):
    pass


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        user = User.query.filter_by(email=username).first()
        if user.check_password(password):
            return user


class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        item = OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        if item and not item.is_refresh_token_expired():
            return item

    def authenticate_user(self, credential):
        return User.query.get(credential.user_id)


authorization = AuthorizationServer()

# scopes definition
scopes = {
    'email': 'Access to your email address.',
    'connects': 'Access to your connected networks.'
}

require_oauth = ResourceProtector()


def config_service(app):
    query_client = create_query_client_func(db.session, OAuth2Client)
    save_token = create_save_token_func(db.session, OAuth2Token)
    authorization.init_app(app, query_client=query_client, save_token=save_token)

    # support all grants
    authorization.register_grant(grants.ImplicitGrant)
    authorization.register_grant(grants.ClientCredentialsGrant)
    authorization.register_grant(PasswordGrant)
    authorization.register_grant(RefreshTokenGrant)

    # support OpenID Connect
    authorization.register_grant(OpenIDCodeGrant)
    authorization.register_grant(OpenIDHybridGrant)
    authorization.register_grant(oidc.OpenIDImplicitGrant)

    # support revocation
    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)

    # protect resource
    bearer_cls = create_bearer_token_validator(db.session, OAuth2Token)
    require_oauth.register_token_validator(bearer_cls())
