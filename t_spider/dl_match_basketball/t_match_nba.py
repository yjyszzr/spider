# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime

while True:
    now = datetime.now()
    # 取出现在的时间小时点,24小时制
    h = int(now.strftime('%H'))
    a = time.localtime()
    # 取得今天是周几(数字表示)
    n = int(time.strftime('%w', a))
    if 1 <= n <= 5:
        if 0 <= h < 9:
            time.sleep(60)
        else:
            print("爬虫正在启动中.....")
            os.system('scrapy crawl match_nba --nolog')
            print("爬虫已完毕,休眠30秒钟")
            time.sleep(30)
    else:
        if 1 <= h < 9:
            time.sleep(60)
        else:
            print("爬虫正在启动中....")
            os.system('scrapy crawl match_nba --nolog')
            print('爬虫已完毕,休眠30秒钟')
            time.sleep(30)
