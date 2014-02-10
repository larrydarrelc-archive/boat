#coding: utf-8

import urllib

from tornado.httpclient import AsyncHTTPClient


def send_to_frontend(event_name, event_data):
    client = AsyncHTTPClient()
    payload = urllib.urlencode({'message': '%s:%s' % (event_name, event_data)})
    client.fetch('http://127.0.0.1:1235/backend', method='POST', body=payload)
