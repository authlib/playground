# Authlib Playground

> An online playground for [Authlib](https://authlib.org).

Play Authlib with <https://play.authlib.org/>.


## Dive into Authlib

1. Create an account at <https://play.authlib.org/>
2. Try Authlib client features with **Connects**
3. Try Authlib OAuth servers with **Apps**

## OAuth 2 Server

Read the documentation on [OAuth 2 Flask server](https://docs.authlib.org/en/latest/flask/oauth2.html).

### Endpoints

- Authorization Endpoint: `https://play.authlib.org/oauth2/authorize`
- Token Endpoint: `https://play.authlib.org/oauth2/token`
- Revocation Endpoint: `https://play.authlib.org/oauth2/revoke`

### APIs

- User profile (no scope): `https://play.authlib.org/api/2/me`
- User email (scope: email): `https://play.authlib.org/api/2/me/email`
- User connects (scope: connects): `https://play.authlib.org/api/2/connects`

## OAuth 1 Server

Read the documentation on [OAuth 1 Flask server](https://docs.authlib.org/en/latest/flask/oauth1.html).

### Endpoints

- Authorization Endpoint: `https://play.authlib.org/oauth1/authorize`
- Temporary Credentials Endpoint: `https://play.authlib.org/oauth1/init`
- Token Credentials Endpoint: `https://play.authlib.org/oauth1/token`

### APIs

- User profile: `https://play.authlib.org/api/1/me`

---

## Local development

To run this playground, you need to clone this repo at first:

    $ git clone git@github.com:authlib/playground.git

Create an virtualenv, and install the requirements:

    $ pip install -r requirements.txt

Copy the sample conf file in `conf` directory:

    $ cp conf/dev.config.py.sample conf/dev.config.py

You need to register client Apps in these websites:

1. Google
2. [Twitter](https://apps.twitter.com/)
3. Facebook
4. GitHub

Get the client_id/consumer_key and client_secret/consumer_secret from these
services and fill them into `conf/dev.config.py`.

Please remember to set the right callback uri:

1. Google: `http://127.0.0.1:5000/connect/authorize/google`
2. Twitter: `http://127.0.0.1:5000/connect/authorize/twitter`
3. Facebook: `http://127.0.0.1:5000/connect/authorize/facebook`
4. GitHub: `http://127.0.0.1:5000/connect/authorize/github`

Run the example server with:

    $ export FLASK_APP=app.py
    $ export FLASK_DEBUG=1
    $ flask run
