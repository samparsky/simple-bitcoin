import os
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)


config = {
    "debug": True,
    "port": int(os.environ.get('PORT')) if os.environ.get("PORT") else 8082,
    "logging": {
        "app": {
            "filename": "./app.log"
        },
        "file": "logs.log",
        "level": "DEBUG"
    },
    "rpc": {
        "host": os.environ.get('RPC_HOST'),
        "port": os.environ.get('RPC_PORT'),
        "user": os.environ.get('RPC_USER'),
        "password": os.environ.get('RPC_PASSWORD')
    },
    "channel": {
        "transaction":{
            "default": "notify",
            "retry": "notify_retry"
        },
        "address": {
            "default": "address_watch"
        }
    },
    "zero_mq": {
        "host": os.environ.get('ZERO_MQ_HOST'),
        "port": int(os.environ.get('ZERO_MQ_PORT'))
    },
    "error_code": {
        "10": "Failed to publish",
        "20": "Redis server down. try again later",
        "30": "Missing details",
        "40": "Specified address missing",
        "50": "Transaction not found",
    },
    "db": {
        "name": "notification",
        "transaction": {
            "unconfirmed": "unconfirmed"
        }
    },
    "celery": {
        "notify": {
            "name": "src.tasks",
            "broker": "redis://localhost:6379/0",
            "imports": ("src.tasks.txn_notify", ),
            "routes": {
                'src.tasks.txn_notify.work_retry': {'queue': 'retry'}
            }
        },
    }

}
