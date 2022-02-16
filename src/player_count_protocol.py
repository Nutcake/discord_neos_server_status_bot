import asyncio
import logging
from asyncio import BaseProtocol

import discord


class PlayerCountProtocol(BaseProtocol):
    def __init__(self, client: discord.Client, loop: asyncio.AbstractEventLoop):
        super().__init__()
        self._client = client
        self._loop = loop

    def datagram_received(self, data, addr):
        message = data.decode()
        try:
            count = int(message)
        except ValueError:
            logging.warning(f"Cannot parse received datagram '{message}' from {addr} as an integer, ignoring...")
            return

        # sanity check:
        if count > 64 or count < 0:
            logging.warning(f"Received datagram appears to contain an invalid playercount '{count}', ignoring...")
            return

        self._loop.create_task(self._client.change_presence(
            activity=discord.Activity(
                name=f"with {count} Users",
                type=discord.ActivityType.playing
            )))
