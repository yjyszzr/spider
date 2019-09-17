# -*- coding: utf-8 -*-
import os
import time

while True:
    os.system('scrapy crawl shooter --nolog')
    print('射手榜更新完毕!')
    time.sleep(600)