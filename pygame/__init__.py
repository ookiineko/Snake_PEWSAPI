# -*- coding: utf-8 -*-
"""
PyGame wrapper
"""

from asyncio import new_event_loop, set_event_loop, run
from socket import socket, error, AF_INET, SOCK_DGRAM
from sys import version_info
from threading import Thread
from time import sleep
from traceback import format_exc
from typing import Iterable, List

from pymcwss import __version__ as pymcwss_ver
from pymcwss.mcwss import MCWSS
from pymcwss.pewsapi import gen_sub, event_player_msg, get_head, \
    get_msg_purpose, purpose_event, get_body, get_event_name, \
    get_prop, get_msg_type, msg_chat, gen_cmd, gen_all_subs, \
    msg_title, par_player_msg
from websockets.legacy.server import WebSocketServerProtocol

from pygame.constants import QUIT, KEYDOWN, K_UP, K_LEFT, K_DOWN, K_RIGHT, K_f
from pygame.event import Event

__version__ = '0.0.1'


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

    class Bridge:
        """
        bridge
        """

        def __init__(self):
            self.waiting = True
            self.__event_queue = []
            self.__wss = None

        def add_event(self, new: Event):
            """
            add a new event to the queue
            """
            self.__event_queue.append(new)

        def get_events(self) -> List[Event]:
            """
            get events from the queue
            """
            events = self.__event_queue.copy()
            self.__event_queue.clear()
            return events

        def set_wss(self, wss: WebSocketServerProtocol):
            """
            set WebSocket server
            """
            self.__wss = wss

        def send_block(self, packet: dict):
            """
            send packet (blocking)
            """
            run(self.__wss.send(packet))

        def send(self, packet: dict):
            """
            send packet (non-blocking)
            """
            send_thread = Thread(target=self.send_block, args=[packet])
            send_thread.setDaemon(True)
            send_thread.start()

    def __init__(
            self,
            wss: WebSocketServerProtocol
    ):
        MCWSS.__init__(self, wss)

        self._tellraw_temp = 'tellraw @a {"rawtext":[{"text":"%s"}]}'
        self._key_up = (0, 1, -4)
        self._key_left = (-1, 0, -4)
        self._key_down = (0, 0, -4)
        self._key_right = (1, 0, -4)
        self._key_f = (2, 2, -4)
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
        self._game_bridge_pwr_pos = (1, 0, 3)
        self._scr_width = 8
        self._scr_height = 6
        self._game_bridge_pwr_temp = 'setblock %s' % self._join_int(self._game_bridge_pwr_pos, ' ') + ' %s'
        self._player_selector = '@a[scores={flag=1},m=a]'
        self._clear_cmd = 'clear %s' % self._player_selector
        self._as_selector = '@e[tag="!__PYGKAS"]'
        self._quit_cmds = (
            self._clear_cmd,
            'gamemode c %s' % self._player_selector,
            self._game_bridge_pwr_temp % 'air',
            'execute %s ~~~ setblock ~~~1 air' % self._as_selector,
            'tp %s 0 -14514 0' % self._as_selector,
            'title @a reset',
            'closewebsocket'
        )

        import pygame.__bridge__

        self.__subs = {
            event_player_msg
        }
        self.__bridge = pygame.__bridge__.default_bridge

    @classmethod
    def on_start(cls, _host: str, port: int):
        """
        on server start
        """
        MCWSS.on_start(_host, port)
        print('/connect %s:%d' % (cls._get_lan_ip(), port))

    async def on_conn(self):
        """
        on client connected
        """
        await MCWSS.on_conn(self)
        print('Minecraft connected')
        packets = gen_all_subs(self.__subs, True)
        packets.extend([gen_sub(sub) for sub in self.__subs])
        for packet in packets:
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
                self._clear_cmd,
                'replaceitem entity %s slot.hotbar 0 stick 1 0 {"can_destroy":{' % self._player_selector +
                '"blocks":["tripwire","barrier"]}}',
                'tp %s 0.99999 0 0 facing 0.99999 2 -99999' % self._player_selector,
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
        self.__bridge.waiting = False

    async def on_recv(self, packet: dict):
        """
        on received client packet
        """
        await MCWSS.on_recv(self, packet)
        head = get_head(packet)
        msg_purpose = get_msg_purpose(head)
        if msg_purpose == purpose_event:
            body = get_body(packet)
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
                                    print('force quit is not allowed')
                                    return
                                new = Event(pygame_event_type)
                                if pygame_event_type == KEYDOWN:
                                    key = args[1]
                                    if key in self._key_names:
                                        new.key = key
                                self.__bridge.add_event(new)
                        elif msg_type == msg_chat:
                            if cmd == 'quitpygame':
                                for quit_cmd in self._quit_cmds:
                                    packet = gen_cmd(quit_cmd)
                                    await self.send(packet)
                                new = Event(QUIT)
                                self.__bridge.add_event(new)


def __start_pygame():
    event_loop = new_event_loop()
    set_event_loop(event_loop)
    PyGamePEWSAPICompact.start(14514, event_loop=event_loop)


def __watch_dog(bridge: PyGamePEWSAPICompact.Bridge):
    while bridge.waiting:
        sleep(0.05)


def init():
    """
    init
    """
    import pygame.__bridge__

    bridge = PyGamePEWSAPICompact.Bridge()
    pygame.__bridge__.default_bridge = bridge
    pygame_start_thread = Thread(target=__start_pygame)
    pygame_start_thread.setDaemon(True)
    pygame_start_thread.start()
    __watch_dog(bridge)
    bridge.waiting = True
    watch_dog_thread = Thread(target=__watch_dog, args=[bridge])
    watch_dog_thread.start()
