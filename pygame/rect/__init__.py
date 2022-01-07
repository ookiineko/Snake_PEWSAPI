# -*- coding: utf-8 -*-
"""
font
"""

from typing import Tuple

my_pos = Tuple[int, int]


class Rect(object):
    """
    rect
    """

    def __init__(self, pos: my_pos, size: my_pos):
        self.__pos = pos
        self.__size = size

    def my_get_pos(self) -> my_pos:
        """
        my get position
        """
        return self.__pos

    def my_get_size(self) -> my_pos:
        """
        my get size
        """
        return self.__size
