#coding: utf-8

import json

import structlog

from core.dispatch import Register
from core.items import items_pool
from .views import ClientHandler


logger = structlog.get_logger(__name__)
events = Register()


@events.reg('hello')
def greeting(request, data):
    request.write('Hello, world!')


@events.reg('quit')
def terminate(request, data):
    request.close()


@events.reg('item_<int:id>_update')
def item_data(request, raw, id):
    id = int(id)
    logger.bind(item_id=id)

    item = items_pool.get(id)
    if item is None:
        logger.warning('Cannot find item %d' % (id))
        return

    data = json.loads(raw)

    logger.info('Update item %d stat to %f' % (id, data['stat']))
    logger.info('Update item %d status %d' % (id, data['status']))
    item.update(data['stat'], data['status'])

    ClientHandler.broadcast('item_%d_update:%s' % (id, data))


@events.reg('item_<int:id>_status')
def item_status(request, data, id):
    item_data(request, data, id)
