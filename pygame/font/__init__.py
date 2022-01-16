# -*- coding: utf-8 -*-
"""
font
"""

from pygame.color import my_color
from pygame.surface import Surface


# stubs

class Font(object):
    """
    game font
    """

    def __init__(self, _name: str, _size: int):
        pass

    @classmethod
    def render(cls, _text: str, _antialias: bool, _font_color: my_color) -> Surface:
        """
        render the font
        """
        return Surface((0, 0))


def get_default_font() -> str:
    """
    get game default font
    """
    return 'Mojangles'


def init():
    """
    init font
    """
