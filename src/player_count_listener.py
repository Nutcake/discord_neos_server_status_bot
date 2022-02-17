import asyncio
import socket

import discord

from player_count_protocol import PlayerCountProtocol


class PlayerCountListener:
    def __init__(self, loop: asyncio.AbstractEventLoop, host: str, port: int):
        self._host = host
        self._port = port
        self._loop = loop
        self._server = None

    async def create_socket(self, bot: discord.Client) -> None:
        self._server = await self._loop.create_server(
            lambda: PlayerCountProtocol(bot, self._loop),
            family=socket.AF_INET,
            port=self._port,
            host=self._host,
            start_serving=True
        )
