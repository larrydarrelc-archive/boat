#coding: utf-8

import time
import json
import random
from hashlib import sha1

from backend.utils import send_to_backend


def warnning_message():
    '''Generate a random warning message.'''
    levels = ['DEBUG', 'INFO', 'WARN', 'FATAL']
    message = {
        'level': random.choice(levels),
        'message': sha1(str(time.time())).hexdigest(),
        'time': time.time()
    }
    return json.dumps(message)


def run():
    client = None
    try:
        while True:
            client = send_to_backend('warn', warnning_message(), client)
            time.sleep(5)
    except Exception:
        client.close()
        raise


if __name__ == '__main__':
    run()
