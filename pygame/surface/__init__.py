# -*- coding: utf-8 -*-
"""
surface
"""

from pygame.color import THECOLORS


class _BaseSurface:
    def __init__(self, size: (int, int)):
        self.__size = size
        self.__bgc = THECOLORS.get('black')
        self._children = []

    def fill(self, color: (int, int, int, int)):
        """
        fill
        """
        self._children = []
        self.__bgc = color

    def get_width(self) -> int:
        """
        get width
        """
        return self.__size[0]

    def get_height(self) -> int:
        """
        get height
        """
        return self.__size[1]


class Surface(_BaseSurface):
    """
    surface
    """
    def blit(self, source: _BaseSurface, pos: (int, int)):
        """
        blit
        """
        self._children.append((source, pos))
