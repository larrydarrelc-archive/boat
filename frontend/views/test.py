#coding: utf-8

import os

import tornado.web


__all__ = ['TestPageHandler']


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestPageHandler(tornado.web.RequestHandler):

    def get_template_path(self):
        return os.path.join(BASE_DIR, 'templates', 'test')

    def static_url(self, path, include_host=None, **kwargs):
        return '/static/%s' % (path)

    def get(self, name):
        self.render('%s.html' % (name))
