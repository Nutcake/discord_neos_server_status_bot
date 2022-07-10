import asyncio
import logging
from asyncio import Protocol, transports

import discord


class PlayerCountProtocol(Protocol):
    response_ok = "200 OK"
    response_br = "400 Bad Request"

    def __init__(self, client: discord.Client, loop: asyncio.AbstractEventLoop, offset: int):
        super().__init__()
        self._client = client
        self._loop = loop
        self._offset = offset
        self._transport = None
        self._server_counts = dict()

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self._transport = transport

    def eof_received(self):
        self._transport = None

    def data_received(self, data):
        message = data.decode().rsplit("\n")[-1]

        tokens = message.split(",")

        try:
            count = int(tokens[0])
        except ValueError:
            logging.warning(f"Cannot parse received message\n'{message}'\nas an integer, ignoring...")
            self.respond(self.response_br)
            return

        serv_id = tokens[1] if len(tokens) == 2 else "default"

        # sanity check:
        if count < 0:
            logging.warning(f"Received datagram appears to contain an invalid playercount '{count}', ignoring...")
            self.respond(self.response_br)
            return

        count += self._offset
        count = max(count, 0)

        if serv_id in self._server_counts.keys() and count == self._server_counts[serv_id]:
            logging.info("Count unchanged, skipping...")
            self.respond(self.response_ok)
            return

        logging.info(f"Got playercount {count}, updating presence...")
        self._server_counts[serv_id] = count

        msg = ", ".join([f"{entry_id}: {entry_count}" for entry_id, entry_count in self._server_counts.items()])

        self._loop.create_task(self._client.change_presence(
            activity=discord.Activity(
                name=msg,
                type=discord.ActivityType.playing
            )))

        self.respond(self.response_ok)

    def respond(self, response: str):
        if self._transport is None:
            return
        self._transport.write(f"HTTP/1.1 {response}\n\n".encode('ascii'))
        self._transport.close()
