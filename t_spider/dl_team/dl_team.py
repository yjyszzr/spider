import os
import time


while True:

    print("爬虫正在启动中.....")
    os.system('scrapy crawl team --nolog')
    print("爬虫已完毕,休眠一天")
    time.sleep(43200)
	
