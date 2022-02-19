import discord

from player_count_listener import PlayerCountListener


class NeosPlayerCountClient(discord.Client):
    def __init__(self, host: str, port: int, offset: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._listener = PlayerCountListener(self.loop, self, host=host, port=port, offset=offset)

    async def create_listener_socket(self):
        await self._listener.create_socket()
