#coding: utf-8


class MessageRequest(object):
    '''Wrap str /bytes data with ~:class:`tornado.web.RequestHandler` to make
    it compatible to ~:class:`utils.dispatch.Dispatcher`.

    :param message: str or bytes instance
    :param handler: a ~:class:`tornado.web.RequestHandler` instance
    '''

    def __init__(self, message, handler):
        self.data = message
        self.handler = handler

    def read(self, num_bytes):
        return self.data

    def write(self, data):
        self.handler.write(data)

    def close(self):
        self.handler.finish()


class WebSocketMessageRequest(object):
    '''Wrap str / bytes data with ~:class:`torando.websocket.WebSocketHandler`
    to make it compatible to ~:class:`utils.dipatch.Dispatcher`.

    :param message: str or bytes instance
    :param handler: a ~:class:`tornado.websocket.WebSocketHandler` instance
    '''

    def __init__(self, message, handler):
        self.data = message
        self.handler = handler

    def read(self, num_bytes):
        return self.data

    def write(self, data):
        self.handler.write_message(data)

    def close(self):
        # Let the handler do some cleanup.
        self.handler.on_close()
        self.handler.close()
