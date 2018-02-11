# coding: utf-8

from contextlib import contextmanager
from flask import g, current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from werkzeug.local import LocalProxy
from werkzeug.contrib.cache import FileSystemCache


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, throw=True):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            if throw:
                raise e


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True


def _get_cache():
    _cache = g.get('_oauth_cache')
    if _cache:
        return _cache
    _cache = FileSystemCache(current_app.config['OAUTH_CACHE_DIR'])
    g._oauth_cache = _cache
    return _cache


cache = LocalProxy(_get_cache)
