#coding: utf-8

import re


class EventNotFoundError(Exception):
    pass


class Register(object):
    '''A simple event base callback functions register.'''

    def __init__(self):
        # Callback functions map, use `event_name` as key.
        self.callbacks = {}

        # Event patterns map, use `event_name` as key.
        self.patterns = {}

    def create_pattern(self, event_name):
        '''Generate a pattern match function from `event_name`.

        :param event_name: event's name
        '''
        converters = {
            'int': '(\d+)',
            'str': '(\w+)'
        }
        format_ = re.compile('(.*)<(.*)>')
        converter_ = re.compile('(.*):(.*)')
        params = []
        converter = 'str'

        while True:
            matched = format_.match(event_name)
            if matched is None:
                break
            event_name, param = matched.groups()
            matched = converter_.match(param)
            if matched:
                converter, param = matched.groups()
            event_name = '%s%s' % (event_name, converters[converter])
            params.append(param)
        # Using greedy matching here,
        # so the rightest will be matched first.
        params.reverse()

        return {
            'pattern': re.compile(event_name),
            'params': params
        }

    def register_callback(self, event_name, func):
        '''Register a callback function.

        Each callback function should take two arguments:

            - `request`: The incoming request object.
            - `data`: Optional data from the request object.

        :param event_name: event's name
        :param func: callback function
        '''
        self.callbacks[event_name] = func
        self.patterns[event_name] = self.create_pattern(event_name)

    def reg(self, event_name):
        '''Register a callback function with decorator:

            @dispatch.reg('event_name')
            def event_callback(request, data):
                # Handle request here.
        '''
        def wrapper(func):
            self.register_callback(event_name, func)
            return func
        return wrapper

    def get(self, event_name):
        '''Retrieve a callback function with event_name.

        :param event_name: event name
        '''
        for k, v in self.callbacks.items():
            pattern = self.patterns[k]
            matched = pattern['pattern'].match(event_name)
            if matched is not None:
                return v, dict(zip(pattern['params'], matched.groups()))
        return None


class BaseDispatcher(Register):
    '''A simple dispatcher:

        class EchoDispatcher(BaseDispatcher):

            def dispatch(self, raw):
                return raw.strip().lower(), None

        dispatch = EchoDispatcher()

    - Pattern matching:

        Specify your own parsing implementation in `dispatch` method by
        subclassing the ~:class:`BaseDispatcher`.

    - Registering:

        @dispatch.reg('echo')
        def echo(request, data):
            request.write(data)


        @dispatch.reg(event_name='ping')
        def pong(request, times):
            try:
                times = int(times)
            except:
                times = 1
            times = max(times, 1)

            request.write('pong' * times)

    - Group registering:

        group = Register()

        @group.reg('pong')
        def ping(request, times):
            try:
                times = int(times)
            except:
                times = 1
            times = max(times, 1)

            request.write('ping' * times)

        dispatch.add_group(group)

    - Dispatching:

        # `request` is an object with `read` / `write` / `close` method.
        dispatch(request)
    '''

    # Received event message size.
    message_buffer_size = 1024

    def add_group(self, group):
        '''Add ~:class:`Register` registered callback functions.'''
        self.callbacks.update(group.callbacks)
        self.patterns.update(group.patterns)

    def dispatch(self, raw):
        '''Put your own pattern parsing implementation here.

        Your implementation should return a tuple or list which contains the
        `event_name` and event data.

        :param raw: raw incomes data
        '''
        raise NotImplementedError

    def __call__(self, request):
        incomes = request.read(self.message_buffer_size)
        event_name, event_data = self.dispatch(incomes)

        rv = self.get(event_name)
        if rv is None:
            raise EventNotFoundError(event_name)
        callback, params = rv
        return callback(request, event_data, **params)
