# -*- coding: utf-8 -*-
"""
color
"""

from typing import Tuple


my_color = Tuple[int, int, int, int]

my_black = (
    0,
    0,
    0,
    255
)

my_green_yellow = (
    173,
    255,
    47,
    255
)

my_dark_green = (
    0,
    100,
    0,
    255
)

my_orange3 = (
    205,
    133,
    0,
    255
)

my_white = (
    255,
    255,
    255,
    255
)

THECOLORS = {
    'black': my_black,
    'greenyellow': my_green_yellow,
    'darkgreen': my_dark_green,
    'orange3': my_orange3,
    'white': my_white
}

my_color_map = {
    my_black: 15,
    my_green_yellow: 5,
    my_dark_green: 13,
    my_orange3: 1,
    my_white: 0
}
