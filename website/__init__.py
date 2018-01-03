from flask import json
from ._flask import create_flask_app
from .models import db
from .services import oauth2
from . import auth, routes


def create_app(config=None):
    app = create_flask_app(config)
    db.init_app(app)
    auth.init_app(app)
    oauth2.init_app(app)
    routes.init_app(app)
    register_hook(app)
    return app


def register_hook(app):
    with open(app.config['ASSETS_FILE'], 'r') as f:
        assets = json.load(f)

    @app.context_processor
    def register_context_processor():
        return dict(
            assets=assets,
            current_user=auth.current_user,
        )
