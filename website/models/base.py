# coding: utf-8

from contextlib import contextmanager
from authlib.client.flask import OAuth
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


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
oauth = OAuth()


class Base(db.Model):
    __abstract__ = True
