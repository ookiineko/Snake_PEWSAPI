# -*- coding: utf-8 -*-
"""
display
"""

from pygame.surface import Surface
from pymcwss.pewsapi import gen_cmd


def set_mode(size: tuple) -> Surface:
    """
    set size
    """
    import pygame.__bridge__

    bridge = pygame.__bridge__.default_bridge
    if bridge.window:
        raise TypeError('multiple windows is not supported yet')
    window = Surface(size)
    bridge.window = window
    return window


def set_caption(caption: str):
    """
    set caption
    """
    import pygame.__bridge__

    bridge = pygame.__bridge__.default_bridge
    for cmd in (
        'scoreboard objectives remove "!__PYGCSO"',
        'scoreboard objectives add "!__PYGCSO" dummy "%s"' % caption,
        'scoreboard objectives setdisplay sidebar "!__PYGCSO"'
    ):
        packet = gen_cmd(cmd)
        bridge.send_block(packet)


def update():
    """
    update
    """
    # print('stub update')
