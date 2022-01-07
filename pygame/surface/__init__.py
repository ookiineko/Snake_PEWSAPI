# -*- coding: utf-8 -*-
"""
surface
"""
from typing import List, Tuple, Union

from pygame.color import THECOLORS, my_color
from pygame.rect import my_pos

my_rect = Tuple[my_pos, my_pos, my_color]


class MyBaseSurface:
    """
    my base surface
    """

    def __init__(
            self,
            size: my_pos,
            my_x_scale: float = 1,
            my_y_scale: float = 1
    ):
        self.__size = size
        self.my_children = []
        self.__bgc = THECOLORS.get('black')
        self.__x_scale = my_x_scale
        self.__y_scale = my_y_scale

    def fill(self, color: my_color):
        """
        fill
        """
        self.my_children = []
        self.__bgc = color

    def my_draw_rect(
            self,
            pos: my_pos,
            x_scale: float = -1,
            y_scale: float = -1
    ) -> Union[my_rect, None]:
        """
        my draw rect
        """
        w, h = self.__size
        if w < 0 or h < 0:
            return
        if x_scale < 0:
            x_scale = self.__x_scale
        if y_scale < 0:
            y_scale = self.__y_scale
        x, y = pos
        sx = x * x_scale
        sy = y * x_scale
        sp = int(sx), int(sy)
        sw = w * x_scale
        sh = h * y_scale
        pos1 = int(sx + sw) - 1, int(sy + sh) - 1
        return (
            sp,
            pos1,
            self.__bgc
        )

    def my_draw(
            self,
            pos: my_pos,
            x_scale: float = -1,
            y_scale: float = -1
    ) -> List[my_rect]:
        """
        my draw
        """
        if x_scale < 0:
            x_scale = self.__x_scale
        if y_scale < 0:
            y_scale = self.__y_scale
        rect = self.my_draw_rect(pos, x_scale, y_scale)
        rects = [
            rect
        ]
        x, y = pos
        for c, cp in self.my_children:
            cx, cy = cp
            cdp = (x + cx, y + cy)
            crs = c.my_draw(cdp, x_scale, y_scale)
            if crs:
                rects.extend(crs)
        return rects

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


class Surface(MyBaseSurface):
    """
    my base surface
    """

    def blit(self, src: MyBaseSurface, pos: my_pos):
        """
        blit
        """
        child = (src, pos)
        self.my_children.append(child)
