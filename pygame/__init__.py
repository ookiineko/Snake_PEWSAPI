# -*- coding: utf-8 -*-
"""
PyGame wrapper
"""

from asyncio import new_event_loop, set_event_loop
from asyncio import sleep as asyncio_sleep
from json import dumps, loads, JSONDecodeError
from socket import socket, AF_INET, SOCK_STREAM, error, SOL_SOCKET, SO_REUSEADDR
from sys import version_info
from threading import Thread
from time import sleep
from traceback import format_exc
from typing import List

from pymcwss import __version__ as pymcwss_ver
from pymcwss.mcwss import MCWSS
from pymcwss.pewsapi import gen_sub, event_player_msg, get_head, \
    get_msg_purpose, purpose_event, get_body, get_event_name, \
    get_prop, get_msg_type, msg_chat, gen_cmd, gen_all_subs, \
    msg_title, par_player_msg
from websockets.legacy.server import WebSocketServerProtocol

from pygame.__my_util import get_lan_ip, join_int
from pygame.constants import QUIT, KEYDOWN, K_UP, K_LEFT, K_DOWN, K_RIGHT, K_f
from pygame.event import Event

__version__ = '0.0.1'
tellraw_temp = 'tellraw @a {"rawtext":[{"text":"%s"}]}'
key_up = (0, 1, -4)
key_left = (-1, 0, -4)
key_down = (0, 0, -4)
key_right = (1, 0, -4)
key_f = (2, 2, -4)
keys = (
    key_up,
    key_left,
    key_down,
    key_right,
    key_f
)
key_names = (
    'K_UP',
    'K_LEFT',
    'K_DOWN',
    'K_RIGHT',
    'K_f'
)
key_codes = (
    K_UP,
    K_LEFT,
    K_DOWN,
    K_RIGHT,
    K_f
)
key_map = dict(zip(key_names, key_codes))
bridge_pwr_pos = (1, 0, 3)
scr_width = 8
scr_height = 6
bridge_pwr_temp = 'setblock %s' % join_int(bridge_pwr_pos, ' ') + ' %s'
selector = '@a[scores={flag=1},m=a]'
clear_cmd = 'clear %s' % selector
as_selector = '@e[tag="!__PYGKAS"]'
quit_cmds = (
    clear_cmd,
    'gamemode c %s' % selector,
    'execute %s ~~~ setblock ~~~1 air' % as_selector,
    'kill %s' % as_selector,
    bridge_pwr_temp % 'air',
    'title @a reset',
    'closewebsocket'
)


class PyGameSocket:
    """
    PyGame socket
    """

    def __init__(self):
        self.__sock = socket(AF_INET, SOCK_STREAM)
        self.__connect = False

    def connect(self) -> bool:
        """
        connect to the PyGame socket server
        """
        if not self.__connect:
            try:
                self.__sock.connect(('127.0.0.1', 19810))
                self.__sock.settimeout(2)
                self.__connect = True
            except ConnectionRefusedError:
                pass
        return self.__connect

    def get_event_list(self) -> List[Event]:
        """
        get remote event list from queue
        """
        result = []
        if not self.__connect:
            return result
        req = {
            'type': 'get'
        }
        packet = dumps(req).encode('utf-8')
        resp = {}
        try:
            self.__sock.send(packet)
            packet = self.__sock.recv(2048)
            if packet:
                resp = loads(packet.decode())
        except (error, JSONDecodeError):
            print(format_exc())
        if resp:
            events = resp.get('events')
            if events:
                for e in events:
                    new = Event(e.get('type'))
                    key = e.get('key')
                    if key:
                        new.key = key
                    result.append(new)
        return result

    def close(self):
        """
        close client connection
        """
        self.__sock.close()


class PyGamePEWSAPICompact(MCWSS):
    """
    PyGame PEWSAPI compatible layer
    """

    class Bridge:
        """
        bridge
        """

        def __init__(self):
            self.waiting = True

    def __init__(
            self,
            ws: WebSocketServerProtocol,
            sock: socket,
            bridge: Bridge
    ):
        MCWSS.__init__(self, ws)
        self.__subs = {
            event_player_msg
        }
        self.__sock = sock
        self.__event_queue = []
        self.__bridge = bridge

    @classmethod
    def on_start(cls, _host: str, port: int):
        """
        on server start
        """
        MCWSS.on_start(_host, port)
        print('/connect %s:%d' % (get_lan_ip(), port))

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
        sock_server_thread = Thread(target=self.__sock_server)
        sock_server_thread.setDaemon(True)
        sock_server_thread.start()
        cmds = [
            'title @a times 0 0 0',
            bridge_pwr_temp % 'redstone_block'
        ]
        for key_pos, key_name in zip(keys, key_names):
            x, y, z = key_pos
            pos = (x, y, z + 1)
            as_name = '!__PYGEKD#' + key_name
            cmds.append('setblock %s tripwire 0 keep' % join_int(pos, ' '))
            cmds.append('summon armor_stand "%s" %s' % (as_name, join_int(key_pos, ' ')))
            cmds.append('tag @e[name="%s",c=1] add "!__PYGKAS"' % as_name)
        cmds.extend(
            [
                'effect %s invisibility 99999 255 true' % as_selector,
                'gamemode a @a[scores={flag=1},m=c]',
                clear_cmd,
                'replaceitem entity %s slot.hotbar 0 stick 1 0 {"can_destroy":{' % selector +
                '"blocks":["tripwire","barrier"]}}',
                'tp %s 0.99999 0 0 facing 0.99999 2 -99999' % selector,
                tellraw_temp % 'pygame_PEWSAPI %s (pyMCWSS %s, Python %s)' % (
                    pymcwss_ver,
                    __version__,
                    join_int(version_info[:3], '.')
                ),
                tellraw_temp % 'Hello from the pygame community. https://www.pygame.org/contribute.html'
            ]
        )
        for cmd in cmds:
            packet = gen_cmd(cmd)
            await self.send(packet)
        await asyncio_sleep(2)
        self.__bridge.waiting = False

    async def on_dc(self):
        """
        on client disconnected
        """
        await MCWSS.on_dc(self)
        print('Minecraft disconnected')
        self.__bridge.waiting = False

    @classmethod
    async def pygame_ws_handler(
            cls,
            ws: WebSocketServerProtocol,
            _path: str,
            sock: socket,
            bridge: Bridge
    ):
        """
        WebSocket handler
        """
        instance = cls(ws, sock, bridge)
        await instance.main_loop()

    @classmethod
    def pygame_start(cls, port: int, bridge: Bridge):
        """
        start PyGame
        """
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', 19810))
        sock.listen(4096)
        event_loop = new_event_loop()
        set_event_loop(event_loop)
        cls.start(
            port,
            ws_handler=lambda ws, path: cls.pygame_ws_handler(
                ws,
                path,
                sock,
                bridge
            ),
            event_loop=event_loop
        )

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
                                new = {
                                    'type': pygame_event_type
                                }
                                if pygame_event_type == KEYDOWN:
                                    key = args[1]
                                    if key in key_names:
                                        new['key'] = key
                                self.__event_queue.append(new)
                        elif msg_type == msg_chat:
                            if cmd == 'quitpygame':
                                for quit_cmd in quit_cmds:
                                    packet = gen_cmd(quit_cmd)
                                    await self.send(packet)
                                await asyncio_sleep(2)
                                new = {
                                    'type': QUIT
                                }
                                self.__event_queue.append(new)

    def __sock_server(self):
        while self.connected:
            client, _ = self.__sock.accept()
            client_thread = Thread(target=self.__sock_client, args=[client])
            client_thread.setDaemon(True)
            client_thread.start()

    def __sock_client(self, client: socket):
        while True:
            try:
                data = client.recv(2048)
                if not data:
                    break
                req = loads(data.decode(encoding='utf-8'))
                if req:
                    req_type = req.get('type')
                    if req_type == 'get':
                        resp = {
                            'events': self.__event_queue
                        }
                        packet = dumps(resp).encode(encoding='utf-8')
                        client.send(packet)
                        self.__event_queue.clear()
            except (error, JSONDecodeError, UnicodeDecodeError):
                print(format_exc())
                break
        if client:
            client.close()


def __watch_dog(bridge: PyGamePEWSAPICompact.Bridge):
    while bridge.waiting:
        sleep(2)


def init():
    """
    init
    """
    bridge = PyGamePEWSAPICompact.Bridge()
    pygame_start_thread = Thread(target=PyGamePEWSAPICompact.pygame_start, args=[14514, bridge])
    pygame_start_thread.setDaemon(True)
    pygame_start_thread.start()
    while bridge.waiting:
        sleep(2)
    bridge.waiting = True
    watch_dog_thread = Thread(target=__watch_dog, args=[bridge])
    watch_dog_thread.start()
