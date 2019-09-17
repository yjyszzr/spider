import os
import time


while True:
	try:
	    print("爬虫正在启动中.....")
	    os.system('scrapy crawl ou --nolog')
	    print("爬虫已完毕,休眠1分钟")
	    time.sleep(60)
	except:
		print("异常错误请60秒后重试!")
		time.sleep(60)
