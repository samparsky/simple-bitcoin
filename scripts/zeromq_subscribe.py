import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from src.subscribe import ZMQHandler

daemon = ZMQHandler()
daemon.start()
