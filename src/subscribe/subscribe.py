import binascii
import asyncio
import zmq
import zmq.asyncio
import signal
import struct
import requests
import json
import sys
from src.lib import Connector, BitcoinRPC
from src.config import Settings
from src.tasks import unconfirmed, confirmed
from src.model import TransactionModel

class ZMQHandler():
    def __init__(self):

        config_data = Settings.get('zero_mq')
        self.db_config = Settings.get('db')
        # print(config_data)
        self.redis = Connector.Redis()
        self.bitcoinRPC = BitcoinRPC()
        self.txnModel = TransactionModel()

        self.loop = zmq.asyncio.install()
        self.zmqContext = zmq.asyncio.Context()

        self.zmqSubSocket = self.zmqContext.socket(zmq.SUB)
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "hashblock")
        self.zmqSubSocket.setsockopt_string(zmq.SUBSCRIBE, "rawtx")
        self.zmqSubSocket.connect("tcp://%s:%i" % (config_data['host'], int(config_data['port'])))

    def trigger(self, response, payload):
        headers = {'content-type': 'application/json'}
        # response = json.dumps(response)
        # print(response.get('hook'))
        response = requests.post(response.get('hook'), headers=headers, json=json.dumps(payload))
        return

    def decoderawtx(self, hexstring):
        try:
            result = self.bitcoinRPC.process(method="decoderawtransaction", params=[hexstring.decode("utf-8")])

            for vout in result['result']['vout']:
                if "addresses" in vout['scriptPubKey']:
                    addresses = vout['scriptPubKey']['addresses']
                    for address in addresses:
                        ismember = self.redis.hget(self.db_config['name'], address)
                        print('ismember', ismember)
                        if ismember is not None:
                            print(str(hexstring))
                            print(result)
                            self.trigger(json.loads(ismember.decode('utf-8')), result)
            return
        except Exception as e:
            print(e)

    def getblock(self, hexstring):
        # sys.exit()
        print("--- in get block -----")
        try:
            result = self.bitcoinRPC.process(method="getblock", params=[hexstring.decode("utf-8"), 1])
            print('result data')
            print(result)
            print(result['result']['height'])
            if "height" in result['result']:
                print(" -------- height ----- ")
                height = result['result']['height']
                # trigger check unconfirmed transactions
                unconfirmed.delay()
                # trigger items in bucket waiting for the block as confirmation
                if self.txnModel.exists(height):
                    confirmed.delay(str(height))
        except Exception as e:
            print(e)
            pass
        # asyncio.ensure_future(self.handle())

    @asyncio.coroutine
    def handle(self):
        msg = yield from self.zmqSubSocket.recv_multipart()
        topic = msg[0]
        body = msg[1]
        sequence = "Unknown"
        if len(msg[-1]) == 4:
          msgSequence = struct.unpack('<I', msg[-1])[-1]
          sequence = str(msgSequence)
        if topic == b"rawtx":
            print('- RAW TX ('+sequence+') -')
            # print(binascii.hexlify(body))
            self.decoderawtx(binascii.hexlify(body))
            print('topic', topic)
        if topic == b"hashblock":
            print('- HASH TX (' + sequence + ') -')
            print(binascii.hexlify(body))
            self.getblock(binascii.hexlify(body))
        # schedule ourselves to receive the next message
        asyncio.ensure_future(self.handle())

    def start(self):
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.create_task(self.handle())
        self.loop.run_forever()

    def stop(self):
        self.loop.stop()
        self.zmqContext.destroy()
