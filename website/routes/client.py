from flask import Blueprint
from flask import render_template
from ..auth import require_login
from ..models import OAuth2Client

bp = Blueprint('client', __name__)


@bp.route('')
@require_login
def list_clients():
    return render_template('client/list.html')


@bp.route('/create')
@require_login
def create_client():
    return render_template('client/create.html')


@bp.route('/<client_id>')
@require_login
def edit_client(client_id):
    client = OAuth2Client.get_by_client_id(client_id)
    return render_template('client/edit.html', client=client)
