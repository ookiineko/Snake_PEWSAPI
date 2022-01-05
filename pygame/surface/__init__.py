# -*- coding: utf-8 -*-
"""
surface
"""


# stub
class Surface(object):
    """
    surface
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def fill(self, _color: (int, int, int)):
        """
        fill
        """
        pass

    def blit(self, _source: object, _pos: (int, int)):
        """
        blit
        """
        pass

    def get_width(self) -> int:
        """
        get width
        """
        return self.width

    def get_height(self) -> int:
        """
        get height
        """
        return self.height
