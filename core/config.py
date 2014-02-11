#coding: utf-8

import sys
import errno
import imp


def import_string(import_name):
    import_name = str(import_name)

    if '.' in import_name:
        module, obj = import_name.rsplit('.', 1)
    else:
        return __import__(import_name)
    try:
        return getattr(__import__(module, None, None, [obj]), obj)
    except (ImportError, AttributeError):
        modname = module + '.' + obj
        __import__(modname)
        return sys.modules[modname]


class Config(dict):

    def from_pyfile(self, filename, silent=False):
        d = imp.new_module('config')
        d.__file__ = filename
        try:
            with open(filename) as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unaable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        if isinstance(obj, str):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
