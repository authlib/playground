# Authlib Playground

This project is designed to be an online playground for
[Authlib](https://authlib.org). It's not ready for a deployment at the
moment, but you can play it locally by yourself.


## Get Started

To run this playground, you need to clone this repo at first:

    $ git clone git@github.com:authlib/playground.git

Create an virtualenv, and install the requirements:

    $ pip install -r requirements.txt

## Configuration

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

## Run Server

Run the example server with:

    $ export FLASK_APP=app.py
    $ export FLASK_DEBUG=1
    $ flask run

I'll deploy it online in the future.
