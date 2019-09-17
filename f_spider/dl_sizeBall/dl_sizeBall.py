import os
import time

while True:
    print("爬虫正在启动中...")
    os.system('scrapy crawl size --nolog')
    print("爬虫执行完毕,休息十分钟")
    time.sleep(600)