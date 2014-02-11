#coding: utf-8

import tornado.ioloop

import backend
import frontend
from core.config import Config


def setup_logging(config):
    import logging.config

    logging.config.fileConfig(config.get('LOGGING_CONF'))


def run():
    config = Config()
    config.from_object('configs.default')

    setup_logging(config)

    backend_app = backend.build(**config)
    backend_app.run()

    frontend_app = frontend.build(**config)
    frontend_app.run()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
