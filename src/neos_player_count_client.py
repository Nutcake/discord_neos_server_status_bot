import discord

from player_count_listener import PlayerCountListener


class NeosPlayerCountClient(discord.Client):
    def __init__(self, host: str, port: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._listener = PlayerCountListener(self.loop, host=host, port=port)

    async def create_listener_socket(self):
        await self._listener.create_socket(self)
