#coding: utf-8

import yaml
import pytest

from core import items


@pytest.fixture
def test_defination():
    defination = items.Defination()
    defination['id'] = 1
    defination['name'] = 'test'

    return defination


@pytest.fixture
def test_definations():
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


def test_defination_validate(test_defination):
    assert test_defination.validate() is True

    # `name` is omittable.
    del test_defination['name']
    with pytest.raises(items.WrongDefination):
        test_defination.validate()

    test_defination['name'] = 'test'

    # `id` is omittable.
    del test_defination['id']
    assert test_defination.validate() is True


def test_defination_to_str(test_defination):
    reloaded = yaml.load(str(test_defination))

    assert reloaded['id'] == test_defination['id']
    assert reloaded['name'] == test_defination['name']


def test_defination_from_dict():
    raw = dict(id=1, name='test')
    test_defination = items.Defination.from_dict(raw)
    assert test_defination['id'] == raw['id']
    assert test_defination['name'] == raw['name']

    # `id` is omittable.
    raw = dict(name='test')
    test_defination = items.Defination.from_dict(raw)
    assert test_defination['id'] is None
    assert test_defination['name'] == raw['name']

    # `name` is not omittable.
    raw = dict(id=2)
    with pytest.raises(items.WrongDefination):
        items.Defination.from_dict(raw)


def test_defination_int_id():
    raw = dict(id='cannot_be_int', name='test')
    test_defination = items.Defination.from_dict(raw)
    assert test_defination['id'] is None


def test_collect(test_definations):
    rv = items.collect(test_definations)

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
