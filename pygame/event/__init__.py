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
    import pygame.__bridge__

    bridge = pygame.__bridge__.default_bridge
    return bridge.get_events()
