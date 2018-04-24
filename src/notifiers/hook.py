import requests
import json

class WebHook:
    @staticmethod
    def run(url_hook, payload):
        headers = {'content-type': 'application/json'}
        print('post result payload')

        response = requests.post(url_hook, headers=headers, json=json.dumps(payload))

