import configparser
import logging

import discord.errors

from neos_player_count_client import NeosPlayerCountClient
from config import Config


def main():
    logging.getLogger().setLevel(logging.WARNING)
    logging.info("Parsing config-file...")

    config = Config()
    bot = NeosPlayerCountClient(config)

    @bot.event
    async def on_ready():
        await bot.create_listener_socket()
        logging.info("Bot connected")
    try:
        bot.run(config.token)
    except discord.errors.LoginFailure:
        logging.critical("Specified token is invalid.")


if __name__ == '__main__':
    main()
