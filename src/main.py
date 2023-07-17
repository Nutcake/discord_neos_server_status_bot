import asyncio
import logging

import discord.errors
import datetime

from neos_player_count_client import NeosPlayerCountClient
from config import Config


async def main():
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Parsing config-file...")
    intents = discord.Intents(messages=True, message_content=True)

    config = Config()
    bot = NeosPlayerCountClient(config, command_prefix="!", intents=intents)

    @bot.command()
    async def week(ctx):
        today = datetime.datetime.now().isocalendar()
        week_txt = config.week_a if today[1] % 2 == 1 else config.week_b
        if today[2] < 5:
            await ctx.send(f"The coming weekend is **{week_txt}**!")
        else:
            await ctx.send(
                f"The current weekend is **{week_txt}**! Next weekend will be {config.week_a if today[1] % 2 == 0 else config.week_b}")

    @bot.event
    async def on_ready():
        await bot.create_listener_socket()
        logging.info("Bot connected")

    try:
        await bot.start(config.token)
    except discord.errors.LoginFailure:
        logging.critical("Specified token is invalid.")


if __name__ == '__main__':
    asyncio.run(main())
