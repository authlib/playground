from flask import Blueprint, request
from flask import jsonify, render_template
from authlib.specs.rfc5849 import OAuth1Error
from ..models import OAuth1Client
from ..auth import current_user
from ..forms.auth import ConfirmForm, LoginConfirmForm
from ..services.oauth1 import authorization


bp = Blueprint('oauth1', __name__)


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
        grant = authorization.check_authorization_request()
    except OAuth1Error as error:
        # TODO: add an error page
        payload = dict(error.get_body())
        return jsonify(payload), error.status_code

    credential = grant.credential
    client_id = credential.get_client_id()
    client = OAuth1Client.query.filter_by(client_id=client_id).first()
    return render_template(
        'account/authorize.html',
        grant=grant,
        client=client,
        form=form,
    )


@bp.route('/init', methods=['POST'])
def init_token():
    return authorization.create_temporary_credential_response()


@bp.route('/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()
