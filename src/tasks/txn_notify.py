import sys
import os
import json
from datetime import time
import random
from celery.exceptions import MaxRetriesExceededError
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from .listener import Listener
from src.config import Settings
from src.lib import BitcoinRPC, make_celery
from src.notifiers import WebHook
from src.model import TransactionModel
from src.exceptions import TargetException

config = Settings.get('celery')['notify']
db_config = Settings.get('db')

celery = make_celery(name=config['name'],
                     broker=config['broker'],
                     imports=config['imports'],
                     routes=config['routes'])

txnModel = TransactionModel()
bitcoinRPC = BitcoinRPC()


def listen(channel_id, _call):
    listener = Listener(channel_id=channel_id)
    listener.run(_call)


@celery.task
def retry(data):
    print('in retry function')
    txnModel.retry_publish(data)


@celery.task
def trigger(response, payload):
    print("in trigger")
    WebHook.run(response['hook'], payload=payload)
    return

def block_height(block_hash):
    result = bitcoinRPC.process(method="getblock", params=[block_hash, 1])
    print("result")
    print(result)
    if result:
        return int(result['result']['height'])
    return False


def process(data, queue_name='celery', _retry=False):
    response = json.loads(data)
    print(response)
    result = BitcoinRPC().process(params=[response["transaction_id"], True])
    print(result)
    if result['result'] is not None:
        # trigger the hook url
        if "target" in response:
            if "confirmations" in result['result']:
                print(' -- confirmations present --- ')
                if result['result']['confirmations'] >= response['target']:
                    # trigger web hook
                    print(' -- confirmations greater  --- ')
                    trigger.apply_async([response, result], queue=queue_name)
                else:
                    # calculate the required block height for it to be confirmed and add it to the set for the block height
                    print(' -- calculating confirmations  --- ')

                    confirmation_height = (response['target'] - 1) + block_height(result['result']['blockhash'])
                    # store in redis set
                    txnModel.confirmation(confirmation_height, response)
                    # retry.apply_async([response], queue=queue_name)
            else:
                # add to set of unconfirmed transactions
                print(" ---- adding to unconfirmed ---- ")
                txnModel.unconfirmed(response)
                # print(txnModel.get_unconfirmed())
                # retry.apply_async([response], queue=queue_name)
        else:
            # trigger web hook
            trigger.apply_async([response, result], queue=queue_name)
    else:
        if _retry:
            raise TargetException
        else:
            retry.apply_async([response], queue=queue_name)


@celery.task
def unconfirmed():
    print(" -----  unconfirmed --------- ")
    un_conf = txnModel.get_unconfirmed()
    for _un in un_conf:
        print("--------- Getting Unconfirmed txns -------------")
        print(un_conf[_un])
        txnModel.remove_unconfirmed(json.loads(un_conf[_un].decode('utf-8')))
        process(un_conf[_un].decode('utf-8'))


@celery.task
def confirmed(block_h):
    print(' ---- checking confirmations for block --- '+str(block_h))
    result = txnModel.get_all_confirm(block_h)
    print("found result")
    print(result)
    if result:
        for txn in result:
            print(txn)
            process(result[txn].decode('utf-8'))
            # data = json.loads(result[txn].decode('utf-8'))
            # block_data = BitcoinRPC().process(params=[data["transaction_id"], True])
            # trigger.apply_async([data, block_data])


@celery.task
def work(data):
    print('--------------- Trigger Worker --------------------------')
    try:
        process(data)
    except Exception as ex:
        print(ex)
        pass


@celery.task(bind=True, max_retries=5)
def work_retry(self, data):
    print('--------------- Trigger Worker Retry ---------------------')
    try:
        process(data, queue_name='retry', _retry=True)
    except TargetException as ex:
        try:
            self.retry(countdown=int(random.randrange(1, 10, 1)))
        except MaxRetriesExceededError as e:
            error = {
                "error": True,
                "message": "transaction not found"
            }
            trigger.apply_async([json.loads(data), error])

#
# @celery.task
# def decoderawtx(hexstring):
#     try:
#         result = bitcoinRPC.process(method="decoderawtransaction", params=[hexstring.decode("utf-8")])
#
#         for vout in result['result']['vout']:
#             if "addresses" in vout['scriptPubKey']:
#                 addresses = vout['scriptPubKey']['addresses']
#                 for address in addresses:
#                     ismember = txnModel.is_member(address)
#                     print('ismember', ismember)
#                     if ismember is not None:
#                         print(str(hexstring))
#                         print(result)
#                         trigger.apply_async([json.loads(ismember.decode('utf-8')), result])
#         return
#     except Exception as e:
#         print(e)
#
# @celery.task
# def getblock(hexstring):
#     # sys.exit()
#     print("--- in get block -----")
#     try:
#         result = bitcoinRPC.process(method="getblock", params=[hexstring.decode("utf-8"), 1])
#         print('result data')
#         print(result)
#         print(result['result']['height'])
#         if "height" in result['result']:
#             print(" -------- height ----- ")
#             height = result['result']['height']
#             #trigger check unconfirmed transactions
#             unconfirmed.delay()
#             #trigger items in bucket waiting for the block as confirmation
#             confirmed.delay(str(height))
#     except Exception as e:
#         print(e)
#         pass