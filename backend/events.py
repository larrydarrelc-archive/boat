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


@events.reg('item_<int:id>_status')
def update_item_status(request, data, id):
    # Propogate to frontend.
    send_to_frontend('item_%s_status' % (id), data)


@events.reg('item_<int:id>_update')
def update_item_data(request, data, id):
    # Propogate to frontend.
    send_to_frontend('item_%s_update' % (id), data)
