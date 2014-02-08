#coding: utf-8

from utils.dispatch import BaseDispatcher


__all__ = ['Dispatcher']


class Dispatcher(BaseDispatcher):
    '''Simple dispatcher with following format:

        event_name:event_data
    '''

    def dispatch(self, raw):
        incomes = raw.split(':')
        event_name = incomes.pop(0)
        event_data = ':'.join(incomes)

        return event_name, event_data
