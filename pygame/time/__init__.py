# -*- coding: utf-8 -*-
"""
timing
"""

from time import time, sleep

one_second = 1
game_tick_per_second = 20


class Clock(object):
    """
    clock
    """

    def __init__(self):
        self.time = -1

    def tick(self, _framerate: int):
        """
        generate specific framerate
        """
        if _framerate > game_tick_per_second:
            print('framerate higher than %d is not possible' % game_tick_per_second)
            _framerate = game_tick_per_second
        expected = one_second / _framerate
        if self.time < 0:
            self.time = time()
            sleep(expected)
        else:
            passed = time() - self.time
            if passed < expected:
                sleep(expected - passed)
            self.time = time()
