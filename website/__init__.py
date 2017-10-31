from ._flask import create_flask_app
from .models import db
from . import routes


def create_app(config=None):
    app = create_flask_app(config)
    db.init_app(app)
    routes.init_app(app)
    return app
