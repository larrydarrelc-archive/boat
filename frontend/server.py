#coding: utf-8

import os
import structlog

import tornado.web

import views


CURRENT_DIR = os.path.dirname(__file__)


class Server(object):

    settings = {
        'FRONTEND_PORT': 1235,
        'FRONTEND_DEST': 'http://127.0.0.1'
    }

    urls = (
        (r'/', views.MainHandler),
        (r'/client', views.ClientHandler, dict(dispatcher=None, logger=None)),
        (r'/backend', views.BackendHandler,
         dict(dispatcher=None, logger=None)),
        (r'/test/(.*)', views.TestPageHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, dict(path=None))
    )

    def __init__(self, port, dispatcher, logger=None, **settings):
        self.port = port
        self.dispatcher = dispatcher
        self.logger = logger or structlog.get_logger(__name__)
        Server.settings.update(settings)

        # Inject components.
        for url in self.urls:
            if isinstance(url[-1], dict):
                args = url[-1]
                if 'dispatcher' in args:
                    args['dispatcher'] = self.dispatcher
                if 'logger' in args:
                    args['logger'] = self.logger
                if 'path' in args:
                    args['path'] = os.path.join(CURRENT_DIR, 'static')

        self.app = tornado.web.Application(self.urls, **settings)

    def run(self):
        self.logger.info('Frontend server starts listening on %d.' % self.port)
        self.app.listen(self.port)
