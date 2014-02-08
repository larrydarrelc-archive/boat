#coding: utf-8

import os

from server import Server
from common import Dispatcher


def build(**settings):
    port = os.environ.get('FRONTEND_PORT') or settings.get('port', 1235)

    dispatcher = Dispatcher()

    from .events import events
    dispatcher.add_group(events)

    return Server(port, dispatcher)
