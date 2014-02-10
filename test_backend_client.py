#coding: utf-8

import time

from backend.utils import send_to_backend


def run():
    client = None
    try:
        while True:
            client = send_to_backend('hellox', 'world', client)
            time.sleep(2)
    except Exception as e:
        client.close()
        raise e


if __name__ == '__main__':
    run()
