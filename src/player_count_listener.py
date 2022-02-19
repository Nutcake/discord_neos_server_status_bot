import asyncio
import socket

import discord

from player_count_protocol import PlayerCountProtocol


class PlayerCountListener:
    def __init__(self, loop: asyncio.AbstractEventLoop, bot: discord.Client, host: str, port: int, offset: int):
        self._host = host
        self._port = port
        self._loop = loop
        self._server = None
        self._offset = offset
        self._instance = PlayerCountProtocol(bot, self._loop, self._offset)

    async def create_socket(self) -> None:
        self._server = await self._loop.create_server(
            lambda: self._instance,
            family=socket.AF_INET,
            port=self._port,
            host=self._host,
            start_serving=True
        )
