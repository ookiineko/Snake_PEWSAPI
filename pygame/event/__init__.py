# -*- coding: utf-8 -*-
"""
event
"""

from typing import List

from pygame.__bridge__ import my_test_bridge


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
    import pygame.__bridge__

    bridge = pygame.__bridge__.default_bridge
    my_test_bridge(bridge)
    events = bridge.event_queue.copy()
    bridge.event_queue = []
    return events
