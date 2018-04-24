import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import datetime
from src.tasks.txn_notify import listen, work_retry
from src.config import Settings

channel_id = Settings.get("channel")['transaction']['retry']
print('----  starting retry listening ----- ' + str(datetime.date.today()))
listen(channel_id=channel_id, _call=work_retry)
