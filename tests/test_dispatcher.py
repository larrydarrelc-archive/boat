#coding: utf-8

import pytest

from common import Dispatcher
from frontend.compat import MessageRequest


@pytest.fixture
def dispatcher():
    return Dispatcher()


def create_request(message):
    return MessageRequest(message, None)


def test_regex_match(dispatcher):

    @dispatcher.reg('test_int_<int:id>')
    def wrap(request, data, id):
        return id

    @dispatcher.reg('test_str_<anything>')
    def wrap2(request, data, anything):
        return anything

    @dispatcher.reg('<int:id>')
    def wrap3(request, data, id):
        return id

    @dispatcher.reg('normal')
    def wrap4(request, data):
        return 'normal'

    assert dispatcher(create_request('test_int_1:')) == '1'
    assert dispatcher(create_request('test_int_123123123:')) == '123123123'

    with pytest.raises(Exception):
        dispatcher(create_request('test_int_not-a-str:'))

    assert dispatcher(create_request('test_str_anything:')) == 'anything'
    assert dispatcher(create_request('test_str_123123:')) == '123123'

    assert dispatcher(create_request('123123:')) == '123123'

    assert dispatcher(create_request('normal:')) == 'normal'
