# -*- coding: utf-8 -*-
"""
draw
"""
from pygame.color import my_color
from pygame.rect import Rect
from pygame.surface import Surface


def rect(surface: Surface, color: my_color, r: Rect):
    """
    draw rect
    """
    pos = r.my_get_pos()
    new = Surface(r.my_get_size())
    new.fill(color)
    surface.blit(new, pos)
