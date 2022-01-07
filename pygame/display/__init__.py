# -*- coding: utf-8 -*-
"""
display
"""

from pymcwss.pewsapi import gen_cmd

from pygame.color import my_color_map
from pygame.surface import Surface

my_w_limit = my_h_limit = 128
my_scr_left_top_x = my_scr_left_top_y = -64


def set_mode(size: tuple) -> Surface:
    """
    set size
    """
    import pygame.__bridge__

    bridge = pygame.__bridge__.default_bridge
    if bridge.window:
        raise TypeError('multiple windows is not supported yet')
    w, h = size
    x_scale = my_w_limit / w if w > my_w_limit else 1
    y_scale = my_h_limit / h if h > my_h_limit else 1
    window = Surface(size, x_scale, y_scale)
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


my_fill_temp = 'fill %d 16 %d %d 16 %d concrete %d'


def update():
    """
    update
    """
    import pygame.__bridge__

    bridge = pygame.__bridge__.default_bridge
    window = bridge.window
    pos = (0, 0)
    rects = window.my_draw(pos)
    packets = []
    for pos, pos1, color in rects:
        x, y = pos
        ox = my_scr_left_top_x + x
        oy = my_scr_left_top_y + y
        op = ox, oy
        x1, y1 = pos1
        ox1 = my_scr_left_top_x + x1
        oy1 = my_scr_left_top_y + y1
        op1 = ox1, oy1
        cmd = my_fill_temp % (*op, *op1, my_color_map.get(color, 0))
        packet = gen_cmd(cmd)
        packets.append(packet)
    for packet in packets:
        bridge.send_block(packet)
