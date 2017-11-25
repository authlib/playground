from flask import Blueprint
from flask import url_for, abort, redirect
from ..auth import require_login
from ..models import oauth, User, Connect

bp = Blueprint(__name__, 'connect')


@bp.route('/bind/<name>')
@require_login
def bind(name):
    service = _get_service_or_404(name)
    callback_uri = url_for('.authorize', name=name, _external=True)
    return service.authorize_redirect(callback_uri)


@bp.route('/authorize/<name>')
@require_login
def authorize(name):
    service = _get_service_or_404(name)
    token = service.authorize_access_token()
    profile = service.fetch_user()
    user = User.get_or_create(profile)
    Connect.create_token(name, token, user)
    user.login()
    return redirect(url_for('.view', name=name))


@bp.route('/view/<name>')
def view(name):
    return 'ok'


def _get_service_or_404(name):
    service = getattr(oauth, name, None)
    if not service:
        abort(404)
    return service
