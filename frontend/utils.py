#coding: utf-8

import urllib

from tornado.httpclient import AsyncHTTPClient

from .server import Server


def send_to_frontend(event_name, event_data):
    client = AsyncHTTPClient()
    payload = urllib.urlencode({'message': '%s:%s' % (event_name, event_data)})

    base = Server.settings['FRONTEND_DEST'].rstrip('/')
    port = Server.settings['FRONTEND_PORT']
    dest = '%s:%s/backend' % (base, port)
    client.fetch(dest, method='POST', body=payload)
