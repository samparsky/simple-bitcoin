import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from src.tasks.txn_notify import listen, work
from src.config import Settings

channel_id = Settings.get("channel")['transaction']['default']
print('----  starting listening ----- '+str(datetime.date.today()))
listen(channel_id=channel_id, _call=work)
