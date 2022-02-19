import configparser
import logging

import discord.errors

from neos_player_count_client import NeosPlayerCountClient


def main():
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Parsing config-file...")
    config = configparser.ConfigParser()
    config.read("config.ini")

    token = config.get(section="Discord", option="token")
    if token is None:
        logging.critical("You need to provide a valid Bot-Token via the 'token' parameter in the [Discord] section of "
                         "the config.ini file.")
        return

    host = config.get(section="General", option="host", fallback=None)
    port = config.getint(section="General", option="port", fallback=22122)
    offset = config.getint(section="General", option="count_offset", fallback=0)

    bot = NeosPlayerCountClient(host=host, port=port, offset=offset)

    @bot.event
    async def on_ready():
        await bot.create_listener_socket()
        logging.info("Bot connected")
    try:
        bot.run(token)
    except discord.errors.LoginFailure:
        logging.critical("Specified token is invalid.")


if __name__ == '__main__':
    main()
