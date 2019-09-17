# -*- coding: utf-8 -*-
import os
import time

while True:
    os.system('scrapy crawl team_record --nolog')
    print("爬虫执行完毕!")
    time.sleep(3600)