# -*- coding: utf-8 -*-
import os
import time

while True:
    os.system('scrapy crawl score_5 --nolog')
    print("爬虫执行完毕!")
    time.sleep(3600)