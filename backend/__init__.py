#coding: utf-8

import os

from common import Dispatcher

from .server import BackendServer


def build(**settings):
    port_key = 'BACKEND_PORT'
    port = os.environ.get(port_key) or settings.get(port_key, 1234)

    dispatcher = Dispatcher()

    from .events import events
    dispatcher.add_group(events)

    return BackendServer(port, dispatcher)
