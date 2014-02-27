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


class Defination(dict):
    '''Item defination.'''

    @staticmethod
    def from_dict(origin):
        '''Create ~:class:`Defination` from `dict` instance.

        :param origin: `dict` instance
        '''
        defination = Defination()
        defination['id'] = None
        if 'id' in origin:
            try:
                defination['id'] = int(origin['id'])
            except ValueError:
                pass
        defination['name'] = origin.get('name')

        if defination.validate():
            return defination

    def validate(self):
        '''Validate item defination.'''
        if self.get('name') is None:
            raise WrongDefination('Item name cannot be empty.')
        return True

    def __str__(self):
        return yaml.dump({
            'id': self.get('id'),
            'name': self['name']
        })


class WrongDefination(Exception):
    pass


def collect(raw):
    '''Collect items from raw configuration.

    :param raw: raw configuration string
    '''
    declaration = yaml.load(raw)

    rv = []
    seq_id, used_ids = 1, []
    for item in declaration['items']:
        defin = Defination.from_dict(item)
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
