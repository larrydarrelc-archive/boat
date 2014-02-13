#coding: utf-8

import os


LOGGING_CONF = os.path.join(os.path.dirname(__file__), 'logging.ini')

# Backend settings:
BACKEND_DEST = 'localhost'
BACKEND_PORT = 1234


# Frontend settings:
FRONTEND_DEST = 'http://127.0.0.1'
FRONTEND_PORT = 1235


# Database settings:
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                       'data',
                       'data.db')
