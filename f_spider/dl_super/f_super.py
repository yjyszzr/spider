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
    if n==1 or n ==3 or n ==6:

        if 19 <= h < 22:
            os.system('python3 super_lotto.py')
            os.system('python3 super_desc.py')
            os.system('scrapy crawl super --nolog')
            print('数据存储完毕')
            time.sleep(600)
        # elif h == 15:
        #     print('现在时间是:{}'.format(now.strftime('%Y-%m-%d %H:%M:%S')))
          #  time.sleep(3)
        else:
            time.sleep(1800)
    else:
        time.sleep(84400)