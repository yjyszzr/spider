import os
import time

while True:
    print('爬虫正在启动中...')
    os.system('scrapy crawl newresult --nolog')
    print('爬虫执行完毕休息5秒')
    time.sleep(5)