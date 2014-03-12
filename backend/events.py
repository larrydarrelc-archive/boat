#coding: utf-8

import structlog

from core.dispatch import Register
from frontend.utils import send_to_frontend


logger = structlog.get_logger(__name__)
events = Register()


@events.reg('hello')
def greeting(request, data):
    request.write('Hello, world!')


@events.reg('quit')
def terminate(request, data):
    request.close()


@events.reg('item_status')
def update_item_status(request, data):
    # Propogate to frontend.
    send_to_frontend('item_status', data)


@events.reg('item_update')
def update_item_data(request, data):
    # Propogate to frontend.
    send_to_frontend('item_update', data)
