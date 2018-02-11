from flask import Blueprint, url_for
from flask import abort, redirect, render_template
from ..auth import require_login, current_user
from ..models import OAuth1Client, OAuth2Client
from ..forms.client import (
    Client1Form,
    Client2Form, OAuth2ClientWrapper
)

bp = Blueprint('client', __name__)


@bp.route('')
@require_login
def list_clients():
    q = OAuth1Client.query.filter_by(user_id=current_user.id)
    oauth1_clients = q.order_by(OAuth1Client.id.desc()).limit(50).all()

    q = OAuth2Client.query.filter_by(user_id=current_user.id)
    oauth2_clients = q.order_by(OAuth2Client.id.desc()).limit(50).all()
    return render_template(
        'client/list.html',
        oauth1_clients=oauth1_clients,
        oauth2_clients=oauth2_clients,
    )


@bp.route('/<int:version>/create', methods=['GET', 'POST'])
@require_login
def create_client(version):
    if version == 1:
        form = Client1Form()
    else:
        form = Client2Form()

    if form.validate_on_submit():
        form.save(current_user)
        return redirect(url_for('.list_clients'))
    return render_template('client/create.html', form=form)


@bp.route('/<int:version>/<client_id>', methods=['GET', 'POST'])
@require_login
def edit_client(version, client_id):
    if version == 1:
        client = OAuth1Client.query.filter_by(client_id=client_id).first()
        if not client or client.user_id != current_user.id:
            abort(404)
        form = Client1Form(obj=client)
    else:
        client = OAuth2Client.query.filter_by(client_id=client_id).first()
        if not client or client.user_id != current_user.id:
            abort(404)
        form = Client2Form(obj=OAuth2ClientWrapper(client))

    if form.validate_on_submit():
        form.update(client)
        return redirect(url_for('.list_clients'))
    return render_template('client/edit.html', form=form)
