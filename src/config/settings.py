from .config import config
# from lib import Logger


class Settings:
    @staticmethod
    def get(key):
        if key is not None and key in config:
            return config[key]
        else:
            raise Exception("Key not present in the config file")

    @staticmethod
    def error_codes():
        return Settings.get('error_code')
    # def app_logger(self):
    #     filename = Settings.get('logging')['app']['filename']
    #     return Logger(filename=filename)

    # def