# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime
import random

while True:
    r = random.randint(1800, 3600)
    now = datetime.now()
    h = int(now.strftime('%H'))
    if h == 10:
        os.system('python3 smail.py')
    time.sleep(r)