from . import front
from . import account
from . import connect
from . import client
from . import oauth1
from . import oauth2
from . import api_1
from . import api_2


def init_app(app):
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(connect.bp, url_prefix='/connect')
    app.register_blueprint(client.bp, url_prefix='/client')
    app.register_blueprint(oauth1.bp, url_prefix='/oauth1')
    app.register_blueprint(oauth2.bp, url_prefix='/oauth2')
    app.register_blueprint(api_1.bp, url_prefix='/api/1')
    app.register_blueprint(api_2.bp, url_prefix='/api/2')
    app.register_blueprint(front.bp, url_prefix='')
