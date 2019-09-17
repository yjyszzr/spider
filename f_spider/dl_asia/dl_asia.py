import time 
import os

while True:
	try:
		print("爬虫马上启动....")
		os.system('scrapy crawl real_ya --nolog')
		print("爬虫已完毕,休眠5秒钟")
		time.sleep(5)
	except:
		print("异常错误稍后五秒重试!")
		time.sleep(5)