from .service import config_service, require_oauth
from .routes import bp


def init_app(app, url_prefix):
    config_service(app)
    app.register_blueprint(bp, url_prefix=url_prefix)
