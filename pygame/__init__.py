# -*- coding: utf-8 -*-
"""
PyGame wrapper
"""

from asyncio import new_event_loop, set_event_loop
from socket import socket, error, AF_INET, SOCK_DGRAM
from sys import version_info
from threading import Thread
from time import sleep
from traceback import format_exc
from typing import Iterable

from pymcwss import __version__ as pymcwss_ver
from pymcwss.mcwss import MCWSS
from pymcwss.pewsapi import gen_sub, event_player_msg, get_head, \
    get_msg_purpose, purpose_event, get_body, get_event_name, \
    get_prop, get_msg_type, msg_chat, gen_cmd, msg_title, \
    par_player_msg, purpose_cmd_resp, purpose_error, \
    par_cmd_resp_or_error
from websockets.legacy.server import WebSocketServerProtocol

from pygame.__bridge__ import my_test_bridge, Bridge
from pygame.constants import QUIT, KEYDOWN, K_UP, K_LEFT, K_DOWN, K_RIGHT, K_f
from pygame.event import Event
from pygame.surface import Surface
from pygame.time import one_second, game_tick_per_second

__version__ = '0.0.1'
one_game_tick = one_second / game_tick_per_second


class PyGamePEWSAPICompact(MCWSS):
    """
    PyGame PEWSAPI compatible layer
    """

    @classmethod
    def _get_lan_ip(cls):
        sock = socket(AF_INET, SOCK_DGRAM)
        try:
            sock.connect(('1.2.3.4', 1))
            ip = sock.getsockname()[0]
        except error:
            print(format_exc())
            ip = '127.0.0.1'
        finally:
            sock.close()
        return ip

    @classmethod
    def _join_int(cls, iterable: Iterable, s: str) -> str:
        return s.join([str(x) for x in iterable])

    def __init__(
            self,
            wss: WebSocketServerProtocol
    ):
        MCWSS.__init__(self, wss)

        self._tellraw_temp = 'tellraw @a {"rawtext":[{"text":"%s"}]}'
        self._key_up = (0, 2, -4)
        self._key_left = (-1, 1, -4)
        self._key_down = (0, 1, -4)
        self._key_right = (1, 1, -4)
        self._key_f = (0, -1, -4)
        self._keys = (
            self._key_up,
            self._key_left,
            self._key_down,
            self._key_right,
            self._key_f
        )
        self._key_names = (
            'K_UP',
            'K_LEFT',
            'K_DOWN',
            'K_RIGHT',
            'K_f'
        )
        self._key_codes = (
            K_UP,
            K_LEFT,
            K_DOWN,
            K_RIGHT,
            K_f
        )
        self._key_map = dict(zip(self._key_names, self._key_codes))
        self._game_bridge_pwr_pos = (1, 2, 1)
        self._scr_width = 8
        self._scr_height = 6
        self._game_bridge_pwr_temp = 'setblock %s' % self._join_int(self._game_bridge_pwr_pos, ' ') + ' %s'
        self._player_selector = '@a[scores={flag=1},m=a]'
        self._as_selector = '@e[tag="!__PYGKAS"]'
        self._quit_cmds = (
            'effect %s clear' % self._player_selector,
            'gamemode c %s' % self._player_selector,
            self._game_bridge_pwr_temp % 'air',
            'execute %s ~~~ setblock ~~~1 air' % self._as_selector,
            'tp %s 0 -14514 0' % self._as_selector,
            'title @a reset',
            'scoreboard objectives remove "!__PYGCSO"',
            'closewebsocket'
        )

        import pygame.__bridge__

        self.__subs = {
            event_player_msg
        }
        self.__bridge = pygame.__bridge__.default_bridge
        my_test_bridge(self.__bridge)

    @classmethod
    def on_start(cls, host: str, port: int):
        """
        on server start
        """
        MCWSS.on_start(host, port)
        print('/connect %s:%d' % (cls._get_lan_ip(), port))

    async def on_conn(self):
        """
        on client connected
        """
        await MCWSS.on_conn(self)
        print('Minecraft connected')
        for packet in [gen_sub(sub) for sub in self.__subs]:
            await self.send(packet)
        cmds = [
        ]
        for key_pos, key_name in zip(self._keys, self._key_names):
            as_name = '!__PYGEKD#' + key_name
            cmds.append('summon armor_stand "%s" %s' % (as_name, self._join_int(key_pos, ' ')))
            cmds.append('tag @e[name="%s",c=1] add "!__PYGKAS"' % as_name)
        cmds.extend(
            [
                'effect %s invisibility 99999 255 true' % self._as_selector,
                'execute %s ~~~ setblock ~~~1 tripwire 0 keep' % self._as_selector,
                'title @a times 0 0 0',
                self._game_bridge_pwr_temp % 'redstone_block',
                'gamemode a @a[scores={flag=1},m=c]',
                'effect %s night_vision 99999 255 true' % self._player_selector,
                'tp %s 0 0 0 facing 0 2 -99999' % self._player_selector,
                self._tellraw_temp % 'pygame_PEWSAPI %s (pyMCWSS %s, Python %s)' % (
                    pymcwss_ver,
                    __version__,
                    self._join_int(version_info[:3], '.')
                ),
                self._tellraw_temp % 'Hello from the pygame community. https://www.pygame.org/contribute.html'
            ]
        )
        for cmd in cmds:
            packet = gen_cmd(cmd)
            await self.send(packet)
        self.__bridge.set_wss(self)
        self.__bridge.waiting = False

    async def on_dc(self):
        """
        on client disconnected
        """
        await MCWSS.on_dc(self)
        print('Minecraft disconnected')
        new = Event(QUIT)
        self.__bridge.event_queue.append(new)
        self.__bridge.waiting = False

    async def on_recv(self, packet: dict):
        """
        on received client packet
        """
        await MCWSS.on_recv(self, packet)
        head = get_head(packet)
        msg_purpose = get_msg_purpose(head)
        if msg_purpose in (purpose_event, purpose_cmd_resp, purpose_error):
            body = get_body(packet)
            if msg_purpose == purpose_event:
                event_name = get_event_name(body)
                if event_name == event_player_msg:
                    prop = get_prop(body)
                    msg_type = get_msg_type(prop)
                    if msg_type in (msg_title, msg_chat):
                        _, _, msg = par_player_msg(prop)
                        if msg.startswith('!__'):
                            cmd = msg[3:]
                            if msg_type == msg_title:
                                if cmd.startswith('PYGE'):
                                    args = cmd[4:].split('#')
                                    pygame_event_type = args[0]
                                    if pygame_event_type == QUIT:
                                        print('force quit will cause issues, not allowed here')
                                        return
                                    new = Event(pygame_event_type)
                                    if pygame_event_type == KEYDOWN:
                                        key = args[1]
                                        if key in self._key_names:
                                            new.key = key
                                    self.__bridge.event_queue.append(new)
                            elif msg_type == msg_chat:
                                if cmd == 'quitpygame':
                                    for quit_cmd in self._quit_cmds:
                                        packet = gen_cmd(quit_cmd)
                                        await self.send(packet)
            else:
                status_code, status_msg = par_cmd_resp_or_error(body)
                if status_code < 0:
                    print(status_msg)


def __start_pygame():
    event_loop = new_event_loop()
    set_event_loop(event_loop)
    PyGamePEWSAPICompact.start(14514, event_loop=event_loop)


def __watch_dog(bridge: Bridge):
    while bridge.waiting:
        sleep(one_game_tick)


def init():
    """
    init
    """
    import pygame.__bridge__

    bridge = Bridge()
    default_bridge = pygame.__bridge__.default_bridge
    if default_bridge:
        raise TypeError('PyGame is already initialized')
    pygame.__bridge__.default_bridge = bridge
    pygame_start_thread = Thread(target=__start_pygame)
    pygame_start_thread.setDaemon(True)
    pygame_start_thread.start()
    __watch_dog(bridge)
    bridge.waiting = True
    watch_dog_thread = Thread(target=__watch_dog, args=[bridge])
    watch_dog_thread.start()
