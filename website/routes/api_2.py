from flask import Blueprint
from flask import jsonify
from authlib.flask.oauth2 import current_token
from ..models import db, User, Connect
from ..services.oauth2 import require_oauth

bp = Blueprint('api_2', __name__)


@bp.route('/me')
@require_oauth()
def user_profile():
    user = User.query.get(current_token.user_id)
    return jsonify(user.to_dict())


@bp.route('/me/email')
@require_oauth('email')
def user_email():
    user = User.query.get(current_token.user_id)
    return jsonify(email=user.email)


@bp.route('/connects')
@require_oauth('connects')
def user_connects():
    q = db.session.query(Connect.name)
    rv = [n for n, in q.filter_by(user_id=current_token.user_id)]
    return jsonify(rv)
