from werkzeug.local import LocalProxy
from .models import get_current_user


current_user = LocalProxy(get_current_user)
