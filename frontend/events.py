#coding: utf-8

import json

import structlog

from core.dispatch import Register
from core.items import items_pool
from common.constants import ItemsStatus
from .views import ClientHandler


logger = structlog.get_logger(__name__)
events = Register()


@events.reg('hello')
def greeting(request, data):
    request.write('Hello, world!')


@events.reg('quit')
def terminate(request, data):
    request.close()


@events.reg('item_update')
def item_data(request, raw):
    data = json.loads(raw)
    id = int(data['id'])
    logger.bind(item_id=id)

    item = items_pool.get(id)
    if item is None:
        logger.warning('Cannot find item %d' % (id))
        return

    logger.info('Update item %d stat to %f' % (id, data['stat']))
    logger.info('Update item %d status %d' % (id, data['status']))
    item.update(data['stat'], data['status'])

    ClientHandler.broadcast('item_update:%s' % item.to_json())


@events.reg('item_status')
def item_status(request, data):
    item_data(request, data)


@events.reg('item_confirm')
def item_confirm(request, id):
    id = int(id)
    logger.bind(item_id=id)

    item = items_pool.get(id)
    if item is None:
        logger.warning('Cannot find item %d' % (id))
        return

    if item['status'] != ItemsStatus.WARNING:
        logger.warning('Item %d is not in warning mode' % (id))
        return

    logger.info('Confirm item %d' % (id))
    item.confirm()

    ClientHandler.broadcast('item_update:%s' % item.to_json())


@events.reg('items')
def items(request, raw):
    '''Get all item's status.'''
    request.write('items:%s' % (json.dumps(items_pool.values())))
