from . import front
from . import account
from . import connect


def init_app(app):
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(connect.bp, url_prefix='/connect')
    app.register_blueprint(front.bp, url_prefix='')
