import datetime
import time

from location_approx.batch_manager import start as s
from location_approx.process_manager import start

s('test', date=datetime.datetime(2013, 11, 7, 8, 0))
start()
while (True):
    time.sleep(1)
