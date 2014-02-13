#coding: utf-8

'''SQL storage provider.

    from sqlstore import store

    store.configure(path='./sql.db')  # sqlite3

    cursor = store.get_cursor()
'''

import sqlite3

import structlog


class Store(object):
    '''A sql connection provider.'''

    CONNECTION = {
        'path': ':memory:'
    }

    def __init__(self):
        self.conn = None
        self.logger = structlog.get_logger(__name__)

    @classmethod
    def configure(cls, path=None):
        '''Configure sql storage.

        :param path: sqlite3 database path, default is `:memory:`
        '''
        cls.CONNECTION['path'] = path or ':memory:'

    def get_cursor(self):
        if self.conn is None:
            self._create_conn()

        return self.conn.cursor()

    def commit(self):
        if self.conn is None:
            return

        self.conn.commit()

    def _create_conn(self):
        '''Create a connection.'''
        self.logger.info('Create sql connection.')
        self.conn = sqlite3.connect(Store.CONNECTION['path'])

    def __del__(self):
        '''Delete hook.'''

        # Don't forget to close the connection.
        if self.conn is not None:
            self.logger.info('Closing sql connection.')
            self.conn.close()

store = Store()
