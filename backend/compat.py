#coding: utf-8

import logging


class IOStreamRequest(object):
    '''Wrap ~:class:`tornado.iostream.IOStream to make it compatible to
    ~:class:`utils.dispatch.Dispatcher`.

    When a frame is ready (i.e., read to the `FRAME_END`), it will let the
    dispatcher handle the frame.

    :param stream: a ~:class:`tornado.iostream.IOStream` instance
    :param dispatcher: a ~:class:`utils.dispatch.Dispatcher` instance
    '''

    FRAME_END = '\n'

    def __init__(self, stream, dispatcher):
        self._dispatcher = dispatcher
        self._stream = stream
        self._stream.read_until(self.FRAME_END, self._read_frame)

        self.data = ''

        self.logger = logging.getLogger(__name__)

    def _read_frame(self, data):
        self.data = data

        # Consume the data when the frame is ready.
        try:
            self._dispatcher(self)
        except Exception as e:
            # TODO Let's talk about error tolerance here.
            self.logger.warn('Got error while dispatching %r %r' % (data, e))

        self.data = ''

        # Read next frame.
        if not self._stream.closed():
            self._stream.read_until(self.FRAME_END, self._read_frame)

    def read(self, num_bytes):
        return self.data

    def write(self, data):
        self._stream.write(data)

    def close(self):
        self._stream.close()
