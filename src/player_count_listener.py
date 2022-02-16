import asyncio
import socket

import discord

from player_count_protocol import PlayerCountProtocol


class PlayerCountListener:
    def __init__(self, loop: asyncio.AbstractEventLoop, host: str, port: int):
        family, _, _, _, addr = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_DGRAM)[0]
        self._addr = addr
        self._loop = loop
        self._transport = None

    async def create_socket(self, bot: discord.Client) -> None:
        self._transport, _ = await self._loop.create_datagram_endpoint(
            lambda: PlayerCountProtocol(bot, self._loop),
            family=socket.AF_INET,
            local_addr=self._addr
        )
