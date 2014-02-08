#coding: utf-8

import os

import tornado.web


__all__ = ['MainHandler']


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class MainHandler(tornado.web.RequestHandler):

    def get_template_path(self):
        return os.path.join(BASE_DIR, 'templates')

    def get(self):
        self.render('index.html')
