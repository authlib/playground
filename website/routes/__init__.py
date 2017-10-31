from . import connect


def init_app(app):
    app.register_blueprint(connect.bp, url_prefix='/connect')
