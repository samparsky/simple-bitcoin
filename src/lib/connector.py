import redis


class Connector:
    __redis = None

    @staticmethod
    def Redis():
        if Connector.__redis is None:
            try:
                # config_data = config['database']['redis']
                Connector.__redis = redis.StrictRedis(
                    host="localhost",
                    socket_timeout=6000
                )
                print('connected to redis')
                # print(Connector.__redis)
            except Exception:
                print("Couldn't Connect to Redis Server")
        return Connector.__redis

# r = redis.Redis()

