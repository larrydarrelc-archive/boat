#coding: utf-8

import logging

import tornado.websocket

from frontend.compat import WebSocketMessageRequest


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
        cls.clients.remove(client)

    def initialize(self, dispatcher, logger=None):
        '''Initialize the handler.

        :param dispatcher: a ~:class:`utils.dispatch.Dispatcher` instance
        :param logger: logger instance
        '''
        self.dispatcher = dispatcher
        self.logger = logger or logging.getLogger(__name__)

    def open(self):
        self.logger.info('Accept new client connection.')
        ClientHandler.add_client(self)

    def on_message(self, msg):
        try:
            self.dispatcher(WebSocketMessageRequest(msg, self))
        except Exception as e:
            # TODO Let's talk about error handling here.
            self.logger.warn('Got error while dispatching %r %r' % (msg, e))

    def on_close(self):
        self.logger.info('Connection closed.')
        ClientHandler.remove_client(self)
