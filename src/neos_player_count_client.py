from discord.ext import commands

from player_count_listener import PlayerCountListener
from config import Config


class NeosPlayerCountClient(commands.Bot):
    def __init__(self, config: Config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._listener = None
        self._config = config

    async def create_listener_socket(self):
        self._listener = PlayerCountListener(self.loop, self, host=self._config.host, port=self._config.port,
                                             offset=self._config.offset, timeout=self._config.timeout)
        await self._listener.create_socket()
