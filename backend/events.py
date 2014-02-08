#coding: utf-8

import logging
import urllib

from tornado.httpclient import AsyncHTTPClient

from utils.dispatch import Register


logger = logging.getLogger(__name__)
events = Register()


@events.reg('hello')
def greeting(request, data):
    request.write('Hello, world!')


@events.reg('quit')
def terminate(request, data):
    request.close()


@events.reg('warn')
def warn_frontend(request, data):
    logger.warn('Notifying warning: %s' % (data))
    client = AsyncHTTPClient()
    payload = urllib.urlencode({'message': 'warn:%r' % (data.strip())})
    client.fetch('http://127.0.0.1:1235/backend', method='POST', body=payload)
