from flask import g, session
from werkzeug.local import LocalProxy
from .models import User


def login_user(user):
    session['sid'] = user.id
    session.permanent = True


def logout_user():
    if 'sid' in session:
        del session['sid']
    if 'sig' in session:
        del session['sig']


def _get_session_user():
    sid = session.get('sid')
    if not sid:
        return None

    user = User.query.get(sid)
    if not user:
        logout_user()
        return None
    return user


def get_current_user():
    user = getattr(g, 'current_user', None)
    if user:
        return user

    user = _get_session_user()
    if user is None:
        return None

    g.current_user = user
    return user


current_user = LocalProxy(get_current_user)
