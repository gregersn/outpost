#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
import time
import json
import flask
import requests
import webbrowser

from cacher import Cache

try:
    import settings_local
except ImportError:
    import settings


auth_data = None

app = flask.Flask('bc3proxy', static_url_path='')
cache = Cache()


@app.route('/')
@app.route('/index')
def index():
    return flask.send_from_directory('.', 'bc3overview.html')


@app.route('/get/<path:endpoint>')
def get(endpoint):
    cached_data = cache.get(endpoint)
    if cached_data is not None:
        print(' * * Cache hit * * ')
        print(cached_data['headers'])
        return cached_data['content']

    url = settings.baseurl + endpoint
    headers = {'user-agent': settings.useragent,
               'Authorization': 'Bearer ' + auth_data['access_token']}
    r = requests.get(url, headers=headers)

    cache.add(endpoint, {'headers': r.headers, 'content': r.content})
    return(r.content)


@app.route('/auth')
def auth_request():
    code = flask.request.args.get('code')
    print(code)
    at = get_access_token(code)
    if at is None:
        return "No access!"
    return at

def get_access_token(code, filename='authdata.json'):
    global auth_data
    parameters = {
        'type': 'web_server',
        'client_id': settings.client_id,
        'redirect_uri': settings.redirect_uri,
        'client_secret': settings.client_secret,
        'code': code
    }

    r = requests.post(settings.URL, params=parameters)
    data = json.loads(r.text)
    data['time'] = time.time()
    with open(filename, 'wb') as f:
        json.dump(data, f)
    auth_data = data

    return r.text


def check_auth_data(filename='authdata.json'):
    data = None
    if os.path.isfile(filename):
        with open(filename) as f:
            data = json.load(f)

        # Check if there is an actual key
        if 'access_token' not in data:
            return None

        # Check time of key
        if time.time() - data['time'] > data['expires_in']:
            print("Need to use the refresh token")

    return data


def main():
    global auth_data
    # Check if we have auth-key, if not, open browser to get authorization,
    auth_data = check_auth_data()
    # start webserver to be able to accept it
    if auth_data is None:
        webbrowser.open(settings.auth_url_new, new=2)

    app.run(port=8000, debug=True)

if __name__ == '__main__':
    main()
