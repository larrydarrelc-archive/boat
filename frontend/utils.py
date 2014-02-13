#coding: utf-8

import urllib

from tornado.httpclient import AsyncHTTPClient

from .server import Server


def send_to_frontend(event_name, event_data):
    client = AsyncHTTPClient()
    payload = urllib.urlencode({'message': '%s:%s' % (event_name, event_data)})

    base = Server.settings.get('FRONTEND_DEST', 'localhost').rstrip('/')
    port = Server.settings.get('FRONTEND_PORT', 1235)
    dest = '%s:%s/backend' % (base, port)
    client.fetch(dest, method='POST', body=payload)
