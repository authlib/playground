from flask import Blueprint
from flask import url_for, redirect, render_template
from ..auth import current_user, logout as _logout
from ..forms.user import AuthenticateForm, UserCreationForm

bp = Blueprint('account', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user:
        return redirect(url_for('front.home'))
    form = AuthenticateForm()
    if form.validate_on_submit():
        form.login()
        return redirect(url_for('front.home'))
    return render_template('account/login.html', form=form)


@bp.route('/logout')
def logout():
    _logout()
    return redirect(url_for('front.home'))


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user:
        return redirect(url_for('front.home'))
    form = UserCreationForm()
    if form.validate_on_submit():
        form.signup()
        return redirect(url_for('front.home'))
    return render_template('account/signup.html', form=form)
