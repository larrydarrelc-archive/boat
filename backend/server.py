#coding: utf-8

import logging

from tornado.tcpserver import TCPServer

from .compat import IOStreamRequest


class BackendServer(TCPServer):

    def __init__(self, port, dispatcher, **settings):
        super(BackendServer, self).__init__(**settings)
        self.port = int(port)
        self.dispatcher = dispatcher
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info('Backend server starts listening on %d.' % self.port)
        self.listen(self.port)

    def handle_stream(self, stream, address):
        IOStreamRequest(stream, self.dispatcher)
