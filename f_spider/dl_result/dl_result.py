import os
import time


while True:
	try:
	    print("爬虫正在启动中.....")
	    os.system('scrapy crawl result --nolog')
	    print("爬虫已完毕,休眠5分钟")
	    time.sleep(300)
	except:
		print("异常错误")
		time.sleep(5)