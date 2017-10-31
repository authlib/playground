import os
from website import create_app

is_dev = bool(os.getenv('FLASK_DEBUG'))

if is_dev:
    conf_file = os.path.abspath('conf/dev.config.py')
    app = create_app(conf_file)
else:
    app = create_app()
