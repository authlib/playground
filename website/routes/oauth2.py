from flask import Blueprint
from flask import jsonify, render_template
from authlib.specs.rfc6749 import OAuth2Error
from ..auth import current_user
from ..forms.oauth2 import ConfirmForm, LoginConfirmForm
from ..services.oauth2 import authorization


bp = Blueprint('oauth2', __name__)


@bp.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if current_user:
        form = ConfirmForm()
    else:
        form = LoginConfirmForm()

    if form.validate_on_submit():
        if form.confirm.data:
            # granted by current user
            grant_user = current_user
        else:
            grant_user = None
        return authorization.create_authorization_response(grant_user)

    try:
        grant = authorization.validate_authorization_request()
    except OAuth2Error as error:
        # TODO: add an error page
        payload = dict(error.get_body())
        return jsonify(payload), error.status_code

    return render_template(
        'oauth2/authorize.html',
        user=current_user,
        grant=grant,
        form=form,
    )


@bp.route('/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_revocation_response()
