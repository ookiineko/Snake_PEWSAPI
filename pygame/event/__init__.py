# -*- coding: utf-8 -*-
"""
event
"""

from typing import List


class Event(object):
    """
    game event
    """

    def __init__(self, _type: int, _key: int = None):
        self.type = _type
        self.key = _key


def get() -> List[Event]:
    """
    get event
    """
    from pygame import PyGameSocket

    client = PyGameSocket()
    result = []
    status = client.connect()
    if status:
        result = client.get_event_list()
    client.close()
    return result
