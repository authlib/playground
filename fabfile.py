import os
import json
import hashlib
from fabric.api import env, local, cd, run
from fabric.operations import put

env.use_ssh_config = True
env.user = 'web'
env.hosts = ['authlib-web-p0']

DOMAIN = 'play.authlib.org'
REMOTE_STATIC_DIR = '/var/www/{}/static'.format(DOMAIN)
LOCAL_STATIC_DIR = 'public/static'
ASSETS_FILE = 'website/static/assets.json'

BIN_PATH = '/var/venv/playground/bin'
BIN_PIP = '{}/pip'.format(BIN_PATH)
BIN_FLASK = '{}/flask'.format(BIN_PATH)


def build():
    with open(ASSETS_FILE) as f:
        data = json.load(f)

    def _build_assets(key, assets):
        print('Build: {}'.format(key))
        css = ''
        for name in assets['styles']:
            file_path = 'website{}'.format(name)
            with open(file_path) as f:
                css += f.read()

        css_file = os.path.join(LOCAL_STATIC_DIR, key + '.css')
        with open(css_file, 'w') as f:
            f.write(css)

    for key in data:
        _build_assets(key, data[key])


def upload():
    run('mkdir -p {}'.format(REMOTE_STATIC_DIR))
    url_maps = {}

    def _gen_assets(url_maps):
        with open(ASSETS_FILE) as f:
            assets = json.load(f)

        for k in assets:
            item = assets[k]
            item['styles'] = [url_maps[k + '.css']]

        return assets

    def _hash_put(name):
        filepath = os.path.join(LOCAL_STATIC_DIR, name)
        with open(filepath, 'rb') as f:
            code = hashlib.md5(f.read()).hexdigest()

        bits = name.split('.')
        bits.insert(1, code[5:18])
        hash_name = '.'.join(bits)
        put(filepath, '{}/{}'.format(REMOTE_STATIC_DIR, hash_name))
        url_maps[name] = '/static/{}'.format(hash_name)
        return hash_name

    for name in os.listdir(LOCAL_STATIC_DIR):
        if not name.endswith('.map'):
            _hash_put(name)

    assets = _gen_assets(url_maps)
    temp_file = 'public/assets.json'
    with open(temp_file, 'w') as f:
        json.dump(assets, f)

    put(temp_file, '/code/playground/conf/assets.json')


def publish():
    local('rm -fr {}'.format(LOCAL_STATIC_DIR))
    local('mkdir -p {}'.format(LOCAL_STATIC_DIR))
    build()
    upload()


def deploy():
    local('git push origin master')
    with cd('/code/playground/src/playground'):
        run('git pull origin master')
        run('{} install -r requirements.txt'.format(BIN_PIP))


def flask(cmd):
    """Run flask command"""
    _env = 'WEBSITE_CONF=/code/playground/conf/config.py FLASK_APP=app.py'
    with cd('/code/playground/src/playground'):
        run('%s %s %s' % (_env, BIN_FLASK, cmd))


def restart():
    env.user = 'lepture'
    run('sudo supervisorctl pid playground | sudo xargs kill -s HUP')
