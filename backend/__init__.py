#coding: utf-8

import os

from common import Dispatcher

from .server import BackendServer


def build(**settings):
    port = os.environ.get('BACKEND_PORT') or settings.get('port', 1234)

    dispatcher = Dispatcher()

    from .events import events
    dispatcher.add_group(events)

    return BackendServer(port, dispatcher)
