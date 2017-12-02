from functools import wraps
from werkzeug.local import LocalProxy
from flask import url_for, redirect, request
from .models import get_current_user


current_user = LocalProxy(get_current_user)


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user:
            url = url_for('account.login', next=request.path)
            return redirect(url)
        return f(*args, **kwargs)
    return decorated
