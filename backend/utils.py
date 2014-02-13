#coding: utf-8

import structlog
import socket

from .protocol import serialize


MAX_TRY = 10


logger = structlog.get_logger(__name__)


def _send_to_backend(event_name, event_data, client=None, tried=None):
    tried = tried or 0

    if not client:
        client = socket.socket()
        client.connect(('127.0.0.1', 1234))

    try:
        client.send(serialize(event_name, event_data))
        return client
    except socket.error as e:
        logger.warn('Send to backend failed, exec: %r' % (e))
        # Try again with new connection.
        if tried < MAX_TRY:
            return _send_to_backend(event_name, event_data, tried=tried + 1)
        else:
            logger.critical('Try to send to backend over %d times!' % MAX_TRY)
            raise e


def send_to_backend(event_name, event_data, client=None):
    return _send_to_backend(event_name, event_data, client)
