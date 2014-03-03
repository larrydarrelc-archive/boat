#coding: utf-8

import yaml
import pytest

from core import items
from core.sqlstore import store


store.configure(path=':memory:')
cur = store.get_cursor()
with open('data/2.items.sql') as f:
    cur.executescript(f.read())
    store.commit()


@pytest.fixture
def test_item():
    defination = items.Item()
    defination['id'] = 1
    defination['name'] = 'test'

    return defination


@pytest.fixture
def test_items():
    definations = {
        'items': [{
            'id': 1,
            'name': 'test1'
        }, {
            'name': 'test2'
        }, {
            'id': '2',
            'name': 'test3'
        }]
    }
    return yaml.dump(definations)


def test_item_validate(test_item):
    assert test_item.validate() is True

    # `name` is omittable.
    del test_item['name']
    with pytest.raises(items.WrongDefination):
        test_item.validate()

    test_item['name'] = 'test'

    # `id` is omittable.
    del test_item['id']
    assert test_item.validate() is True


def test_item_to_str(test_item):
    reloaded = yaml.load(str(test_item))

    assert reloaded['id'] == test_item['id']
    assert reloaded['name'] == test_item['name']


def test_item_from_dict():
    raw = dict(id=1, name='test')
    test_item = items.Item.from_dict(raw)
    assert test_item['id'] == raw['id']
    assert test_item['name'] == raw['name']

    # `id` is omittable.
    raw = dict(name='test')
    test_item = items.Item.from_dict(raw)
    assert test_item['id'] is None
    assert test_item['name'] == raw['name']

    # `name` is not omittable.
    raw = dict(id=2)
    with pytest.raises(items.WrongDefination):
        items.Item.from_dict(raw)


def test_item_int_id():
    raw = dict(id='cannot_be_int', name='test')
    test_item = items.Item.from_dict(raw)
    assert test_item['id'] is None


def test_collect(test_items):
    rv = items.collect(test_items)

    ids = [i['id'] for i in rv]
    group_by_ids = {i['id']: i for i in rv}

    assert len(rv) == 3
    assert 1 in ids
    assert 2 in ids
    assert 3 in ids
    assert group_by_ids[1]['name'] == 'test1'
    assert group_by_ids[2]['name'] == 'test3'
    assert group_by_ids[3]['name'] == 'test2'


def test_collect_duplicated_id():
    definations = yaml.dump({
        'items': [{
            'id': 1,
            'name': 'test1'
        }, {
            'name': 'test2'
        }, {
            'id': '1',
            'name': 'test3'
        }]
    })

    with pytest.raises(items.WrongDefination):
        items.collect(definations)


def test_update_stat(test_item):
    test_item.update_stat(123)
    assert test_item['stat'] == 123


def test_update_status(test_item):
    test_item.update_status(0)
    assert test_item['status'] == 0

    test_item.update_status(1)
    assert test_item['status'] == 1


def test_update_without_id(test_item):
    test_item['id'] = None

    with pytest.raises(items.WrongDefination):
        test_item.update_status(0)

    with pytest.raises(items.WrongDefination):
        test_item.update_stat(1)
