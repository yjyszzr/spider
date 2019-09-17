import os


import time
import os

while True:
	try:
		print("爬虫正在启动中....")
		os.system('scrapy crawl sup --nolog')
		print("爬虫已完毕,休眠5分钟钟")
		time.sleep(300)
	except:
		print("异常错误")
		time.sleep(5)


