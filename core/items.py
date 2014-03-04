#coding: utf-8

'''items

Provide items service.

Item config example:
    items:
        - id: 1
          name: temparature

        - name: wind speed
'''

import yaml
import json
from time import time as now

from core.sqlstore import store
from common.constants import ItemsStatus, LoggingStatus

# Loaded items pool
# FIXME Use a context stack to store it.
items_pool = None


class Item(dict):
    '''Item defination.'''

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self._is_created = False
        self._log_record_id = None

        # FIXME default key
        self['id'] = self.get('id')
        self['name'] = self.get('name')
        self['stat'] = self.get('stat', 0)
        self['status'] = self.get('status', ItemsStatus.NORMAL)

    @staticmethod
    def from_dict(origin):
        '''Create ~:class:`Defination` from `dict` instance.

        :param origin: `dict` instance
        '''
        item = Item()
        item['id'] = None
        if 'id' in origin:
            try:
                item['id'] = int(origin['id'])
            except ValueError:
                pass
        item['name'] = origin.get('name')

        if item.validate():
            return item

    def validate(self):
        '''Validate item defination.'''
        if self.get('name') is None:
            raise WrongDefination('Item name cannot be empty.')
        return True

    def _must_created(self):
        '''Create item's record if not exists.'''
        if self._is_created:
            return

        id = self.get('id')
        if id is None:
            raise WrongDefination('You should set item id before update it.')

        cur = store.get_cursor()

        # Get a triggered logging record if exists.
        cur.execute('SELECT `id` FROM `logging` '
                    'WHERE `item_id` = ? AND `status` = ?',
                    (id, LoggingStatus.TRIGGERED))
        rv = cur.fetchone()
        if rv:
            self._log_record_id = rv[0]

        # Setup item record.
        cur.execute('SELECT COUNT(*) FROM `items` WHERE `id` = ?', (id, ))
        rv = cur.fetchone()
        if rv[0] != 0:
            self._is_created = True
            return

        # Not exists, create a new item record.
        cur.execute('INSERT INTO `items` (`id`, `status`, `data`, `meta`) '
                    'VALUES (?, ?, ?, ?)',
                    (id, self['status'], self['stat'], json.dumps(self)))
        store.commit()
        cur.close()
        self._is_created = True

    def trigger(self):
        '''Make a trigger log.'''
        if self._log_record_id:
            return

        status = LoggingStatus.TRIGGERED
        cur = store.get_cursor()

        cur.execute('INSERT INTO `logging` '
                    '(`item_id`, `status`, `triggered_at`) '
                    'VALUES (?, ?, ?)',
                    (self['id'], status, now()))
        self._log_record_id = cur.lastrowid
        store.commit()
        cur.close()

    def confirm(self):
        '''Make a confirm log.'''
        if not self._log_record_id:
            return

        status = LoggingStatus.CONFIRMED
        cur = store.get_cursor()

        cur.execute('UPDATE `logging` SET `status` = ?, `confirmed_at` = ? '
                    'WHERE `id` = ?',
                    (status, now(), self._log_record_id))
        store.commit()
        cur.close()

    def disappear(self):
        '''Make a disappear log.'''
        if not self._log_record_id:
            return

        status = LoggingStatus.DISAPPEARED
        cur = store.get_cursor()

        cur.execute('UPDATE `logging` SET `status` = ?, `confirmed_at` = ? '
                    'WHERE `id` = ?',
                    (status, now(), self._log_record_id))
        self._log_record_id = None
        store.commit()
        cur.close()

    def update_stat(self, stat):
        '''Update item's stat.

        :param stat: item stat
        '''
        self._must_created()

        self['stat'] = stat
        cur = store.get_cursor()
        cur.execute('UPDATE `items` SET `data` = ? WHERE `id` = ?',
                    (stat, self['id']))
        store.commit()
        cur.close()

    def update_status(self, status):
        '''Update item's status.

        :param status: item status
        '''
        self._must_created()

        self['status'] = status
        cur = store.get_cursor()
        cur.execute('UPDATE `items` SET `status` = ? WHERE `id` = ?',
                    (status, self['id']))
        store.commit()
        cur.close()

        # Update log when status had changed.
        if status == ItemsStatus.WARNING:
            self.trigger()
        elif status == ItemsStatus.NORMAL:
            self.disappear()

    def update(self, stat, status):
        '''Update item.

        :param stat: item stat
        :param status: item status
        '''
        self._must_created()

        self['stat'] = stat
        self['status'] = status

        cur = store.get_cursor()
        cur.execute('UPDATE `items` SET `data` = ?, `status` = ? '
                    'WHERE `id` = ?',
                    (stat, status, self['id']))
        store.commit()
        cur.close()

        # Update log when status had changed.
        if status == ItemsStatus.WARNING:
            self.trigger()
        elif status == ItemsStatus.NORMAL:
            self.disappear()

    def __str__(self):
        return yaml.dump({
            'id': self.get('id'),
            'name': self['name']
        })


class WrongDefination(ValueError):
    pass


def collect(raw):
    '''Collect items from raw configuration.

    :param raw: raw configuration string
    '''
    declaration = yaml.load(raw)

    rv = []
    seq_id, used_ids = 1, []
    for item in declaration['items']:
        defin = Item.from_dict(item)
        item_id = defin.get('id')
        if item_id is not None:
            if item_id in used_ids:
                raise WrongDefination('Id %d is duplicated!' % (item_id))
            used_ids.append(item_id)
        rv.append(defin)

    # Generate a new id.
    for defin in rv:
        if defin.get('id') is None:
            while seq_id in used_ids:
                seq_id = seq_id + 1
            used_ids.append(seq_id)
            defin['id'] = seq_id
            seq_id = seq_id + 1

    return rv


def configure(path):
    '''Setup items poll.'''
    global items_pool

    with open(path) as f:
        items_pool = {i['id']: i for i in collect(f.read())}
