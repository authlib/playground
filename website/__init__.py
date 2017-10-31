from authlib.client.apps import (
    twitter, github
)
from ._flask import create_flask_app
from .models import db, oauth
from . import routes


def create_app(config=None):
    app = create_flask_app(config)
    db.init_app(app)
    oauth.init_app(app)
    twitter.register_to(oauth)
    github.register_to(oauth)
    routes.init_app(app)
    return app
