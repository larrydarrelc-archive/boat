#coding: utf-8

from core.dispatch import BaseDispatcher
from backend.message import parse


__all__ = ['Dispatcher']


class Dispatcher(BaseDispatcher):
    '''Simple dispatcher with following format:

        event_name:event_data
    '''

    def dispatch(self, raw):
        return parse(raw)
