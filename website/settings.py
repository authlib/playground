import os
ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
ASSETS_FILE = os.path.join(ROOT, 'static/assets.json')
