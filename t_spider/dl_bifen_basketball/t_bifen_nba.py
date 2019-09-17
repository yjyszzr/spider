# -*- coding: utf-8 -*-
import os
import time

while True:
    print('爬虫正在启动中...')
    os.system('scrapy crawl bifen_nba --nolog')
    print('爬虫执行完毕休息30秒')
    time.sleep(30)