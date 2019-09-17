# -*- coding: utf-8 -*-
import os
import time

while True:
    os.system('scrapy crawl season_match --nolog')
    print("season_match采集完毕")
    time.sleep(3600)