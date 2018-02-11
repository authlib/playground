from authlib.flask.oauth1 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.flask.oauth1.sqla import (
    create_query_token_func,
    create_query_client_func,
    register_token_credential_hooks,
)
from authlib.flask.oauth1.cache import (
    create_exists_nonce_func,
    register_temporary_credential_hooks,
    register_nonce_hooks,
)
from ..models import db, cache, OAuth1Client, OAuth1Token


query_client = create_query_client_func(db.session, OAuth1Client)
query_token = create_query_token_func(db.session, OAuth1Token)
exists_nonce = create_exists_nonce_func(cache)

authorization = AuthorizationServer(query_client=query_client)
require_oauth = ResourceProtector(
    query_client=query_client,
    query_token=query_token,
    exists_nonce=exists_nonce,
)


def init_app(app):
    authorization.init_app(app)
    register_nonce_hooks(authorization, cache)
    register_temporary_credential_hooks(authorization, cache)
    register_token_credential_hooks(authorization, db.session, OAuth1Token)
    require_oauth.init_app(app)
