from lib import Log
from .settings import Settings


class Log:
    @staticmethod
    def app_log():
        filename = Settings.get('logging')['app']['filename']
        return Log(filename=filename)