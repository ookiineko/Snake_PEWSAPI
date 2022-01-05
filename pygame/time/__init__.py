"""
timing
"""

from time import time, sleep

one_second = 1


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
        expected = one_second / _framerate
        if self.time < 0:
            self.time = time()
            sleep(expected)
        else:
            passed = time() - self.time
            if passed < expected:
                sleep(expected - passed)
            self.time = time()
