from src.lib import Connector
from src.config import Settings
# from config import Log
import json


class AddressModel:
    def __init__(self):
        self.redis = Connector.Redis()
        self.config = Settings.get('db')

    def remove(self, data):
        # result = self.redis.delete(data['address'])
        try:
            result = self.redis.hdel(self.config['name'], data['address'])
            print('result')
            print(result)
            if result:
                return True
            return False
        except Exception as e:
            # log error
            return False

    def store(self, data):

        try:
            # add the address to
            result = self.redis.hset(self.config['name'], data['address'], json.dumps(data))
            print('result')
            print(result)
            return True
        except Exception as e:
            if hasattr(e, 'message'):
                pass
            return False
                # Log.app_log().error(e.message)

