#coding: utf-8

import json
from time import time as current_timestamp

import structlog

from backend.utils import send_to_backend
from core.dispatch import Register
from core.sqlstore import store
from .views import ClientHandler


logger = structlog.get_logger(__name__)
events = Register()


@events.reg('hello')
def greeting(request, data):
    request.write('Hello, world!')


@events.reg('quit')
def terminate(request, data):
    request.close()


@events.reg('warn')
def warning(request, data):
    logger.warn('Recevied warning from backend: %s' % (data))
    ClientHandler.broadcast(data)


@events.reg('update')
def update(request, data):
    logger.info('Sending %s to backend' % (data))

    send_to_backend('update', data)


@events.reg('logging')
def logging_message(request, data):
    '''处理后端发过来的报警信息'''
    logger.bind(event='logging')
    logger.info('Received logging message from backend.', raw_data=data)

    current = current_timestamp()

    cur = store.get_cursor()
    cur.execute('INSERT INTO logging (message, timestamp, solved) '
                'VALUES (?, ?, ?)',
                (data, current, 0))
    store.commit()

    data = json.loads(data)
    data['time'] = current_timestamp()
    data = json.dumps({
        'event': 'logging',
        'data': data
    })

    ClientHandler.broadcast(data)


@events.reg('logging-poll')
def logging_poll(request, data):
    '''获取报警信息列表'''
    logger.bind(event='logging-poll')

    cur = store.get_cursor()
    cur.execute('SELECT * FROM logging WHERE solved = 0')

    request.write(json.dumps({
        'event': 'logging-poll',
        'data': cur.fetchall()
    }))
