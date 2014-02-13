#coding: utf-8

import structlog

from backend.utils import send_to_backend
from core.dispatch import Register
from .views import ClientHandler


logger = structlog.get_logger(__name__)
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
    ClientHandler.broadcast(data)


@events.reg('update')
def update(request, data):
    logger.info('Sending %s to backend' % (data))

    send_to_backend('update', data)
