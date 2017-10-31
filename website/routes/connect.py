from flask import Blueprint
from flask import url_for, abort, redirect
from ..models import oauth, User, Connect

bp = Blueprint(__name__, 'connect')


@bp.route('/login/<name>')
def login(name):
    service = _get_service_or_404(name)
    callback_uri = url_for('.authorize', name=name, _external=True)
    return service.authorize_redirect(callback_uri)


@bp.route('/authorize/<name>')
def authorize(name):
    service = _get_service_or_404(name)
    token = service.authorize_response()
    user = User.get_or_create(token)
    Connect.create_token(name, token, user)
    user.login()
    return redirect(url_for('.view', name=name))


@bp.route('/view/<name>')
def view(name):
    pass


def _get_service_or_404(name):
    service = getattr(oauth, name, None)
    if not service:
        abort(404)
    return service
