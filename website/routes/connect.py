from flask import Blueprint, url_for
from flask import render_template, abort, redirect
from ..auth import oauth, require_login, current_user
from ..models import Connect

bp = Blueprint('connect', __name__)


@bp.route('')
@require_login
def list_connects():
    q = Connect.query.filter_by(user_id=current_user.id)
    connects = q.all()
    return render_template('connects.html', connects=connects)


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
    Connect.create_token(name, token, current_user)
    return redirect('/')


def _get_service_or_404(name):
    service = getattr(oauth, name, None)
    if not service:
        abort(404)
    return service
