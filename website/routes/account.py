from flask import Blueprint
from flask import url_for, redirect
from authlib.client.apps import google
from ..models import User, Connect

bp = Blueprint('account', __name__)


@bp.route('/login')
def login():
    callback_uri = url_for('.authorize', _external=True)
    return google.authorize_redirect(callback_uri)


@bp.route('/auth')
def authorize():
    token = google.authorize_access_token()
    profile = google.parse_openid(token)
    user = User.get_or_create(profile)
    Connect.create_token('google', token, user)
    user.login()
    return redirect('/')
