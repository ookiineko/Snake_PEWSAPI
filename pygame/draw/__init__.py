# -*- coding: utf-8 -*-
"""
draw
"""
from pygame.color import my_color
from pygame.rect import Rect
from pygame.surface import Surface


def rect(surface: Surface, color: my_color, _rect: Rect):
    """
    draw rect
    """
    new = Surface(_rect.my_get_size())
    new.fill(color)
    surface.blit(new, _rect.my_get_pos())
