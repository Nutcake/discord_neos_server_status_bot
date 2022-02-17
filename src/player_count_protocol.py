import asyncio
import logging
from asyncio import Protocol

import discord


class PlayerCountProtocol(Protocol):
    def __init__(self, client: discord.Client, loop: asyncio.AbstractEventLoop):
        super().__init__()
        self._client = client
        self._loop = loop
        self._last_count = 0

    def eof_received(self):
        pass

    def data_received(self, data):
        message = data.decode().rsplit("\n")[-1]
        try:
            count = int(message)
        except ValueError:
            logging.warning(f"Cannot parse received message\n'{message}'\nas an integer, ignoring...")
            return

        # sanity check:
        if count < 0:
            logging.warning(f"Received datagram appears to contain an invalid playercount '{count}', ignoring...")
            return

        if count == self._last_count:
            logging.info("Count unchanged, skipping...")
            return

        logging.info(f"Got playercount {count}, updating presence...")
        self._last_count = count
        self._loop.create_task(self._client.change_presence(
            activity=discord.Activity(
                name=f"with {count} Users",
                type=discord.ActivityType.playing
            )))
