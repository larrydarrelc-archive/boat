#coding: utf-8

EVENT_SEPARATOR = ':'
FRAME_END = '\n'


def serialize(event_name, event_data):
    return '%s%s%s%s' % (event_name, EVENT_SEPARATOR, event_data, FRAME_END)


def parse(raw):
    raw = raw.strip(FRAME_END)
    event = raw.split(':')

    return event[0], ''.join(event[1:])
