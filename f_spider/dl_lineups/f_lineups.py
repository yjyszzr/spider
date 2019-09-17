# -*- coding: utf-8 -*-
import os
import time

while True:
    os.system('scrapy crawl lineups --nolog')
    print('爬虫执行完毕,休息十分钟')
    time.sleep(600)