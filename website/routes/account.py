from flask import Blueprint
from flask import url_for, redirect, render_template
from authlib.client.apps import google
from .. import auth
from ..models import User, Connect
from ..forms.user import AuthenticateForm, UserCreationForm

bp = Blueprint('account', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if auth.current_user:
        return redirect(url_for('front.home'))
    form = AuthenticateForm()
    if form.validate_on_submit():
        form.login()
        return redirect(url_for('front.home'))
    return render_template('account/login.html', form=form)


@bp.route('/logout')
def logout():
    auth.logout()
    return redirect(url_for('front.home'))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if auth.current_user:
        return redirect(url_for('front.home'))
    form = UserCreationForm()
    if form.validate_on_submit():
        form.signup()
        return redirect(url_for('front.home'))
    return render_template('account/signup.html', form=form)


@bp.route('/login/google')
def login_by_google():
    callback_uri = url_for('.authorize', _external=True)
    return google.authorize_redirect(callback_uri)


@bp.route('/auth/google')
def authorize():
    token = google.authorize_access_token()
    profile = google.parse_openid(token)
    user = User.get_or_create(profile)
    Connect.create_token('google', token, user)
    auth.login(user)
    return redirect('/')
