#coding: utf-8

import os

from .server import BackendServer


def build(**settings):
    port_key = 'BACKEND_PORT'
    port = os.environ.get(port_key) or settings.get(port_key, 1234)

    from common import Dispatcher
    dispatcher = Dispatcher()

    from .events import events
    dispatcher.add_group(events)

    return BackendServer(port, dispatcher)
