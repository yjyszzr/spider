# -*- coding: utf-8 -*-
import os
import time

while True:

    os.system('scrapy crawl live --nolog')
    print('爬虫执行完毕,休息10秒钟')
    time.sleep(10)
