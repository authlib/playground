import os
from website import create_app
from website.models import db

is_dev = bool(os.getenv('FLASK_DEBUG'))

if is_dev:
    conf_file = os.path.abspath('conf/dev.config.py')
    app = create_app(conf_file)

    @app.after_request
    def add_header(resp):
        resp.headers['Cache-Control'] = 'no-store'
        resp.headers['Pragma'] = 'no-cache'
        return resp

    with app.app_context():
        db.create_all()
else:
    app = create_app()
