import time

from location_approx.batch_manager import start as s
from location_approx.process_manager import start

s('test')
start()
while (True):
    print('tick')
    time.sleep(1)
