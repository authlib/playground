from flask import Blueprint
from flask import render_template
from ..auth import current_user
from ..models import Connect

bp = Blueprint('front', __name__)


@bp.route('/')
def home():
    if current_user:
        connects = Connect.query.filter_by(user_id=current_user.id).all()
    else:
        connects = None

    services = ['twitter', 'facebook', 'github']
    return render_template(
        'home.html',
        user=current_user,
        connects=connects,
        services=services,
    )
