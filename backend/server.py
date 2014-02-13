#coding: utf-8

import structlog
from tornado.tcpserver import TCPServer

from .compat import IOStreamRequest


class BackendServer(TCPServer):

    settings = {
        'BACKEND_PORT': 1234,
        'BACKEND_DEST': '127.0.0.1'
    }

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

    def __init__(self, port, dispatcher, **settings):
        super(BackendServer, self).__init__(**settings)
        BackendServer.settings = settings
        self.port = int(port)
        self.dispatcher = dispatcher
        self.logger = structlog.get_logger(__name__)

    def run(self):
        self.logger.info('Backend server starts listening on %d.' % self.port)
        self.listen(self.port)

    def handle_stream(self, stream, address):
        self.logger.info('Accept new client connection.')
        client = IOStreamRequest(stream, self.dispatcher, BackendServer)
        BackendServer.add_client(client)
