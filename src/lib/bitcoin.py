import requests, json
from src.config import Settings


class BitcoinRPC:

    def __init__(self):
        configdata = Settings.get('rpc')
        rpcHost = configdata['host']
        rpcPort = configdata['port']
        rpcUser = configdata['user']
        rpcPassword = configdata['password']

        print('rpc configuration')
        print(rpcPassword, rpcPort, rpcUser, rpcHost)
        self.serverUrl = "http://"+rpcUser+":"+rpcPassword+"@"+rpcHost+":"+str(rpcPort)

    def process(self, method='getrawtransaction', params=["a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d", True] ):
        headers = {'content-type': 'application/json'}
        payload = json.dumps({
                "method": method,
                "params": params,
                "id": "jsonrpc"
            })

        try:
            response = requests.post(self.serverUrl, headers=headers, data=payload)
            return response.json()
        except Exception as e:
            #log error
            print('An error occured')
            return {}
