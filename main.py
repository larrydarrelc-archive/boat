#coding: utf-8

import tornado.ioloop

import backend
import frontend
from core.config import Config


def setup_logging(config):
    import logging.config
    import structlog

    logging.config.fileConfig(config.get('LOGGING_CONF'))

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.KeyValueRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True
    )


def setup_database(path):
    from core.sqlstore import store

    store.configure(path=path)


def run():
    config = Config()
    config.from_object('configs.default')

    setup_logging(config)
    setup_database(config.get('DB_PATH'))

    backend_app = backend.build(**config)
    backend_app.run()

    frontend_app = frontend.build(**config)
    frontend_app.run()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
