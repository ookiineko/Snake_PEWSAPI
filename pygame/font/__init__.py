# -*- coding: utf-8 -*-
"""
font
"""

from pygame.color import my_color
from pygame.surface import Surface


class Font(object):
    """
    game font
    """

    def __init__(self, _name: str, _size: int):
        # print('stub font instantiation')
        pass

    @classmethod
    def render(cls, _text: str, _antialias: bool, _font_color: my_color) -> Surface:
        """
        render the font
        """
        # print('stub font render')
        return Surface((0, 0))


# stubs

def get_default_font() -> str:
    """
    get game default font
    """
    return 'Mojangles'


def init():
    """
    init font
    """
