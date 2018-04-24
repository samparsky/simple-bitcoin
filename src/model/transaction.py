from src.lib import Connector
from src.config import Settings
# from config import Log
import json


class TransactionModel:
    def __init__(self):
        self.redis = Connector.Redis()
        self.config = Settings.get('db')['transaction']

    def publish(self, data):
        try:
            data = json.dumps(data)
            print(data)
            result = self.redis.publish(Settings.get("channel")['transaction']['default'], data)
            print('d')
            print(result)
            if result:
                return True
            return False
        except Exception as e:
            if hasattr(e, 'message'):
                pass
            return False
                # Log.app_log().error(e.message)

    def retry_publish(self, data):
        try:
            result = self.redis.publish(Settings.get("channel")['transaction']['retry'], json.dumps(data))
            if result:
                return True
            return False
        except Exception as e:
            if hasattr(e, 'message'):
                pass
            return False

    @staticmethod
    def to(method):
        pass

    def unconfirmed(self, data):
        try:
            result = self.redis.hset(self.config['unconfirmed'], data['transaction_id'], json.dumps(data))
            return True
        except Exception as e:
            # log error
            return False

    def get_unconfirmed(self):
        try:
            result = self.redis.hgetall(self.config['unconfirmed'])
            return result
        except Exception as e:
            # log error
            return False

    def remove_unconfirmed(self, data):
        print(" ---- removing unconfirmed ----")
        print(data)
        try:
            result = self.redis.hdel(self.config['unconfirmed'], data['transaction_id'])
            return True
        except Exception as e:
            # log error
            return False

    def confirmation(self, block_height, data):
        print(" --- in confirmations ---- ")
        try:
            result = self.redis.hset(str(block_height), data['transaction_id'], json.dumps(data))
            print(" --- addding to block --- ")
            print(result)
            return result
        except Exception as e:
            print(e)
            pass

    def exists(self, block_height):
        print(" ----  exists --- ")
        try:
            result = self.redis.exists(str(block_height))
            print(result)
            return result
        except Exception as e:
            print(e)
            pass

    def get_all_confirm(self, block_height):
        try:
            result = self.redis.hgetall(block_height)
            return result
        except Exception as e:
            pass

    def is_member(self, address):
        try:
            ismember = self.redis.hget(Settings.get('db')['name'], address)
            return ismember
        except Exception as e:
            print(e)
            pass

