from flask import Blueprint, url_for
from flask import render_template, abort, redirect
from authlib.client.apps import (
    twitter, facebook, google, github,
)
from ..auth import oauth, require_login, current_user
from ..models import Connect

bp = Blueprint('connect', __name__)


@bp.route('')
@require_login
def list_connects():
    services = oauth._registry.keys()
    q = Connect.query.filter_by(user_id=current_user.id)
    connects = {item.name: item for item in q}
    return render_template(
        'connects.html',
        connects=connects,
        services=services,
    )


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
    user_info = service.fetch_user()
    token['sub'] = user_info.id
    Connect.create_token(name, token, current_user)
    return redirect(url_for('.list_connects'))


def _get_service_or_404(name):
    services = {
        'twitter': twitter,
        'google': google,
        'github': github,
        'facebook': facebook,
    }
    if name not in oauth._registry:
        abort(404)
    return services[name]
