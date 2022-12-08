import asyncio
import logging
from asyncio import Protocol, transports

import discord


class PlayerCountProtocol(Protocol):
    response_ok = "200 OK"
    response_br = "400 Bad Request"

    def __init__(self, client: discord.Client, loop: asyncio.AbstractEventLoop, offset: int, timeout_sec: int):
        super().__init__()
        self._client = client
        self._loop = loop
        self._offset = offset
        self._transport = None
        self._server_info = dict()
        self._timeout_tasks = dict()
        self._timeout_sec = timeout_sec

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self._transport = transport

    def eof_received(self):
        self._transport = None

    async def timeout_server(self, serv_id):
        await asyncio.sleep(self._timeout_sec)
        logging.info(f"Server {serv_id} timed out, resetting to 0...")
        self._server_info[serv_id][0] = 0
        if len(self._server_info[serv_id]) == 2:
            self._server_info[serv_id][1] = False
        msg = self.generate_count_message()
        await self._client.change_presence(
            activity=discord.Activity(
                name=msg,
                type=discord.ActivityType.playing))

    def generate_count_message(self):
        return ", ".join([f"{entry_id}: {entry_count[0]} " + (("G" if entry_count[1] else "R")
                          if len(entry_count) == 2 else '')
                          for entry_id, entry_count in self._server_info.items()])

    def data_received(self, data):
        message = data.decode().rsplit("\n")[-1]
        tokens = message.split(",")
        serv_info = [0]

        try:
            count = int(tokens[0])
            serv_id = tokens[1]
            if len(tokens) == 3:
                consent = bool(int(tokens[2]))
                serv_info.append(consent)
        except (ValueError, IndexError):
            logging.warning(f"Failed to parse a parameter in received message\n'{message}'\n, ignoring...")
            self.respond(self.response_br)
            return

        # sanity check:
        if count < 0:
            logging.warning(f"Received datagram appears to contain an invalid playercount '{count}', ignoring...")
            self.respond(self.response_br)
            return

        count += self._offset
        count = max(count, 0)
        serv_info[0] = count

        if serv_id in self._server_info.keys() and serv_info == self._server_info[serv_id]:
            logging.info("Server info unchanged, skipping...")
            self.respond(self.response_ok)
            return

        logging.info(f"Got new server info {serv_info}, updating presence...")
        self._server_info[serv_id] = serv_info

        msg = self.generate_count_message()

        try:
            running_task = self._timeout_tasks[serv_id]
            running_task.cancel()
        except KeyError:
            pass

        self._loop.create_task(self._client.change_presence(
            activity=discord.Activity(
                name=msg,
                type=discord.ActivityType.playing
            )))

        task = self._loop.create_task(self.timeout_server(serv_id))
        self._timeout_tasks[serv_id] = task
        self.respond(self.response_ok)

    def respond(self, response: str):
        if self._transport is None:
            return
        self._transport.write(f"HTTP/1.1 {response}\n\n".encode('ascii'))
        self._transport.close()
