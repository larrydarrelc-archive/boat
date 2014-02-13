#coding: utf-8

import os

from server import Server
from common import Dispatcher


def build(**settings):
    port_key = 'FRONTEND_PORT'
    port = os.environ.get(port_key) or settings.get(port_key, 1235)

    dispatcher = Dispatcher()

    from .events import events
    dispatcher.add_group(events)

    return Server(port, dispatcher)
