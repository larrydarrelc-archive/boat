#coding: utf-8

import pytest

from core.sqlstore import store as store_


@pytest.fixture
def store():
    store_.configure(':memory:')

    return store_


def test_configure(store):
    store.configure()
    assert store.CONNECTION['path'] == ':memory:'

    store.configure('1')
    assert store.CONNECTION['path'] == '1'

    store.configure(None)
    assert store.CONNECTION['path'] == ':memory:'


def test_cursor(store):
    assert store.get_cursor()
