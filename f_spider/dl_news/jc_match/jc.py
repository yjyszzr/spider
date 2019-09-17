import os
import time


while True:
    print('爬虫马上执行...')
    os.system('scrapy crawl jcm --nolog')
    print('爬虫执行完毕,休息10分钟')
    time.sleep(600)