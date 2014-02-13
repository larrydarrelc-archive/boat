#coding: utf-8

import structlog

from core.dispatch import Register
from frontend.utils import send_to_frontend
from .server import BackendServer


logger = structlog.get_logger(__name__)
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
    send_to_frontend('warn', data.strip())


@events.reg('update')
def update(request, data):
    logger.info('Broadcasting to all clients')
    request.close()
    BackendServer.broadcast(data)
