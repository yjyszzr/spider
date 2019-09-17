# -*- coding: utf-8 -*-
import os
import time

while True:
    os.system('scrapy crawl future --nolog')
    print("赛季更新完毕!")
    time.sleep(3600)