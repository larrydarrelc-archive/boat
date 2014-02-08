#coding: utf-8

from importlib import import_module

import tornado.ioloop

import backend
import frontend


def run():
    # A ugly hack to setup logging configurations.
    import_module('configs.default')

    backend_app = backend.build()
    backend_app.run()

    frontend_app = frontend.build()
    frontend_app.run()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    run()
