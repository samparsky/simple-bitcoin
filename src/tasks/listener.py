from src.lib import Connector


class Listener:
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.redis = Connector.Redis()
        self.pubsub = self.redis.pubsub()
        try:
            self.pubsub.subscribe(channel_id)
        except ConnectionError as e:
            pass

    def run(self, callable):
        for item in self.pubsub.listen():
            print(item)
            if item['type'] == 'message':
                print('item')
                print(item['data'].decode('utf8'))
                callable.delay(item['data'].decode('utf8'))
