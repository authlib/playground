from flask import Blueprint
from flask import jsonify
from authlib.flask.oauth1 import current_credential
from ..models import User
from ..services.oauth1 import require_oauth

bp = Blueprint('api_1', __name__)


@bp.route('/me')
@require_oauth()
def user_profile():
    user = User.query.get(current_credential.user_id)
    return jsonify(user.to_dict())
