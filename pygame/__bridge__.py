# -*- coding: utf-8 -*-
"""
PyGame bridge
"""

from asyncio import run

from websockets.legacy.server import WebSocketServerProtocol

default_bridge = None


class Bridge:
    """
    bridge
    """

    def __init__(self):
        self.waiting = True
        self.event_queue = []
        self.__wss = None
        self.window = None

    def set_wss(self, wss: WebSocketServerProtocol):
        """
        set WebSocket server
        """
        if self.__wss:
            return
        self.__wss = wss

    def send_block(self, packet: dict):
        """
        send packet (blocking)
        """
        if self.__wss:
            run(self.__wss.send(packet))


def my_test_bridge(bridge: Bridge):
    """
    my test bridge
    """
    if not bridge:
        raise ValueError('PyGame is not initialized')


def my_test_bridge_waiting(bridge: Bridge):
    """
    my test bridge waiting
    """
    if not bridge.waiting:
        raise TypeError('Bridge is not waiting')
