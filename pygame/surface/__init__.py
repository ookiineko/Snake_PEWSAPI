# -*- coding: utf-8 -*-
"""
surface
"""


class Surface(object):
    """
    surface
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        print('stub surface instantiation')

    @classmethod
    def fill(cls, _color: (int, int, int, int)):
        """
        fill
        """
        print('stub surface fill')

    @classmethod
    def blit(cls, _source: object, _pos: (int, int)):
        """
        blit
        """
        print('stub surface blit')

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
