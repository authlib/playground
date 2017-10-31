# coding: utf-8

import datetime
import os

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_dict'):
            return o.to_dict()
        if hasattr(o, '_asdict'):
            return o._asdict()
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%SZ')
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        return _JSONEncoder.default(self, o)


class Flask(_Flask):
    json_encoder = JSONEncoder
    jinja_options = dict(
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=[
            'jinja2.ext.autoescape',
            'jinja2.ext.with_',
        ]
    )


def create_flask_app(config=None):
    app = Flask(__name__)

    #: load default configuration
    app.config.from_object('website.settings')

    #: load environment configuration
    if 'WEBSITE_CONF' in os.environ:
        app.config.from_envvar('WEBSITE_CONF')

    #: load app sepcified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    return app
