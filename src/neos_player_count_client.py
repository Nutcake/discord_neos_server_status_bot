import discord

from player_count_listener import PlayerCountListener
from config import Config


class NeosPlayerCountClient(discord.Client):
    def __init__(self, config: Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._listener = PlayerCountListener(self.loop, self, host=config.host, port=config.port, offset=config.offset,
                                             timeout=config.timeout)

    async def create_listener_socket(self):
        await self._listener.create_socket()
