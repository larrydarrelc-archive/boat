#coding: utf-8

import structlog

import tornado.web

from frontend.compat import MessageRequest


__all__ = ['BackendHandler']


class BackendHandler(tornado.web.RequestHandler):

    def initialize(self, dispatcher, logger=None):
        '''Initialize the handler.

        :param dispatcher: a ~:class:`utils.dispatch.Dispatcher` instance
        :param logger: logger instance
        '''
        self.dispatcher = dispatcher
        self.logger = logger or structlog.get_logger(__name__)

    def post(self):
        msg = self.get_body_argument('message')
        try:
            self.dispatcher(MessageRequest(msg, self))
        except Exception as e:
            # TODO Let's talk about error handling here.
            self.logger.warn('Got error while dispatching %r %r' % (msg, e))
            raise tornado.web.HTTPError(400)

        self.set_status(201)
