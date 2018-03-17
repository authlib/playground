from flask import Blueprint, request
from flask import jsonify, render_template
from authlib.specs.rfc6749 import OAuth2Error
from .models import OAuth2Client
from .service import authorization, scopes
from ..auth import current_user
from ..forms.auth import ConfirmForm, LoginConfirmForm


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

    client = OAuth2Client.get_by_client_id(request.args['client_id'])
    return render_template(
        'account/authorize.html',
        grant=grant,
        scopes=scopes,
        client=client,
        form=form,
    )


@bp.route('/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_revocation_response()
