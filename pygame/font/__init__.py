# -*- coding: utf-8 -*-
"""
font
"""

from pygame.surface import Surface


# stubs
class DummyFontSurface(Surface):
    """
    dummy font surface
    """

    def __init__(self, _text: str, _antialias: bool, _font_color: (int, int, int, int)):
        Surface.__init__(self, 0, 0)
        self.text = _text
        self.antialias = _antialias
        self.font_color = _font_color


class Font(object):
    """
    game font
    """

    def __init__(self, _name: str, _size: int):
        pass

    @classmethod
    def render(cls, _text: str, _antialias: bool, _font_color: (int, int, int, int)) -> Surface:
        """
        render the font
        """
        return DummyFontSurface(_text, _antialias, _font_color)


def get_default_font() -> str:
    """
    get game default font
    """
    return 'Mojangles'


def init():
    """
    init font
    """
    pass
