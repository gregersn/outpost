#!/usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

# Register your app here:
register_url = 'https://integrate.37signals.com/'

# Add details here
client_id = 'clientid'
client_secret = 'clientsecret'
accountid = None
useragent = 'Some name (and an email)'

redirect_uri = 'http://localhost:8000/auth'
baseurl = 'https://3.basecampapi.com/%d/' % (accountid, )

auth_baseurl = 'https://launchpad.37signals.com/authorization/'
auth_url_new = (auth_baseurl + "new?" +
                "client_id=%s&redirect_uri=%s&type=web_server" %
                (client_id, redirect_uri))

URL = auth_baseurl + 'token'
port = 8000
