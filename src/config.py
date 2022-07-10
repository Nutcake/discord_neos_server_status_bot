import configparser
import logging


class Config:
    def __init__(self, path="config.ini"):
        config = configparser.ConfigParser()
        config.read(path)

        self.token = config.get(section="Discord", option="token")
        if self.token is None:
            logging.critical(
                "You need to provide a valid Bot-Token via the 'token' parameter in the [Discord] section of "
                "the config.ini file.")
            return

        self.host = config.get(section="General", option="host", fallback=None)
        self.port = config.getint(section="General", option="port", fallback=22122)
        self.offset = config.getint(section="General", option="count_offset", fallback=-1)
        self.timeout = config.getint(section="General", option="server_timeout", fallback=240)
