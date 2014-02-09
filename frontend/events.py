#coding: utf-8

import logging

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
def warning(request, data):
    logger.warn('Recevied warning from backend: %s' % (data))


@events.reg('update')
def update(request, data):
    import socket

    client = socket.socket()
    client.connect(('127.0.0.1', 1234))
    client.send('update:%s\n' % (data))
    logger.info('Sending %s to backend' % (data))
