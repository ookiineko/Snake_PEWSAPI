# -*- coding: utf-8 -*-
"""
utilities
"""

from socket import socket, AF_INET, SOCK_DGRAM, error
from typing import Iterable


def get_lan_ip():
    """
    get LAN ip
    """
    sock = socket(AF_INET, SOCK_DGRAM)
    try:
        sock.connect(('1.2.3.4', 1))
        ip = sock.getsockname()[0]
    except error:
        ip = '127.0.0.1'
    finally:
        sock.close()
    return ip


def join_int(iterable: Iterable, s: str) -> str:
    """
    join int
    """
    return s.join([str(x) for x in iterable])
