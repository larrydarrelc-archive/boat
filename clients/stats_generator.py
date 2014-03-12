#coding: utf-8

import time
import json
import random

from common import constants as con
from backend.utils import send_to_backend


IDS = range(1, 3)
STATS_RANGE = [0, 50]
THRESHOLD = 25
EVENT_NAME = 'item_status'


def generate_message(item_id):
    stat = random.uniform(*STATS_RANGE)
    if stat > THRESHOLD:
        status = con.ItemsStatus.WARNING
    else:
        status = con.ItemsStatus.NORMAL
    return json.dumps({
        'id': item_id,
        'stat': stat,
        'status': status
    })


def run(interval=None):
    interval = interval or 2
    client = None
    try:
        while True:
            id = random.choice(IDS)
            message = generate_message(id)
            client = send_to_backend(EVENT_NAME, message, client)
            time.sleep(interval)
    except KeyboardInterrupt:
        if client is not None:
            client.close()
