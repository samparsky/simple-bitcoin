import logging
import asyncio


class Log:

    def __init__(self, filename="log.log"):
        self.logging = logging.basicConfig(filename=filename,
                                           level=logging.DEBUG,
                                           format='%(asctime)s %(message)s')
    def warn(self, message):
        self.logging.warning(message)

    def info(self, message):
        self.logging.info(message)

    def debug(self, message):
        self.logging.debug(message)

    def error(self, message):
        self.logging.error(message)

