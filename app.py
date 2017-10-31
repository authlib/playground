import os
from website import create_app
from website.models import db

is_dev = bool(os.getenv('FLASK_DEBUG'))

if is_dev:
    conf_file = os.path.abspath('conf/dev.config.py')
    app = create_app(conf_file)
    with app.app_context():
        db.create_all()
else:
    app = create_app()
