import random
import string
import urllib.parse
from os import environ as env

import requests
from flask import Flask, request


SCOPES = [
    'email',
    'incognito',
    'account',
    'expenses',
    'orders',
    'transactions',
    'virtualCards',
    'updates',
    'conversations',
    'webhooks',
    'host',
]

BASE_URL = 'https://' + env['DOMAIN']
REDIRECT_URI = BASE_URL + '/token'
STATE = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

app = Flask(__name__)


@app.route("/")
def home():
    params = {
        'client_id': env['OC_CLIENT_ID'],
        'response_type': 'code',
        'scope': ','.join(SCOPES),
        'state': STATE,
        'redirect_uri': REDIRECT_URI
    }
    url = 'https://opencollective.com/oauth/authorize?' + urllib.parse.urlencode(params)
    return f'<a href="{url}">Get a token</a>'


@app.route("/token")
def get_token():
    request_state = request.args['state']
    assert request_state == STATE, f"States didn't match. Original: {STATE}; Request: {request_state}"
    code = request.args['code']

    data = {
        'grant_type': 'authorization_code',
        'client_id': env['OC_CLIENT_ID'],
        'client_secret': env['OC_CLIENT_SECRET'],
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post('https://opencollective.com/oauth/token', data=data)
    assert response.status_code == 200, f'Status code was {response.status_code}'

    payload = response.json()
    return payload['access_token']


if __name__ == '__main__':
    app.run(port=8080, debug=True)
