#coding: utf-8

import structlog

import tornado.websocket

from frontend.compat import WebSocketMessageRequest
from common.utils import format_exception


__all__ = ['ClientHandler']


class ClientHandler(tornado.websocket.WebSocketHandler):
    '''Frontend websocket clients handler.'''

    # All connected clients.
    clients = []

    @classmethod
    def add_client(cls, client):
        if client not in cls.clients:
            cls.clients.append(client)

    @classmethod
    def remove_client(cls, client):
        if client in cls.clients:
            cls.clients.remove(client)

    @classmethod
    def broadcast(cls, data):
        for client in cls.clients:
            client.write(data)

    def initialize(self, dispatcher, logger=None):
        '''Initialize the handler.

        :param dispatcher: a ~:class:`utils.dispatch.Dispatcher` instance
        :param logger: logger instance
        '''
        self.dispatcher = dispatcher
        self.logger = logger or structlog.get_logger(__name__)

    def write(self, message, binary=False):
        # TODO Need to make a interface?
        self.write_message(message, binary)

    def open(self):
        self.logger.info('Accept new client connection.')
        # TODO Need to make a interface?
        ClientHandler.add_client(self)

    def on_message(self, msg):
        try:
            self.dispatcher(WebSocketMessageRequest(msg, self))
        except Exception as e:
            # TODO Let's talk about error handling here.
            self.logger.warn('Got error while dispatching {0} {1}'.format(
                msg,
                format_exception(e)
            ))

    def on_close(self):
        self.logger.info('Connection closed.')
        ClientHandler.remove_client(self)
