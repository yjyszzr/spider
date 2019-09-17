# -*- coding: utf-8 -*-
import requests
import time
import re
from pymysql import connect
from datetime import datetime

now = datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()

url = "http://kaijiang.500.com/dlt.shtml"
# url = "http://kaijiang.500.com/shtml/dlt/18087.shtml"
res = requests.get(url=url).content.decode('gbk')
#期号
n = re.search('<font class="cfont2"><strong>(.*?)</strong>',res).group(1)
p = {
    '一':1,
    '二':2,
    '三':3,
    '四':4,
    '五':5,
    '六':6
}
#奖金级别reward_level

#基本中奖注数reward_num1

#基本单注奖金reward_price1

#追加中奖注数reward_num2

#追加单注奖金reward_price2

data = []
# 一等奖:
item = {}
# 基本中奖注数
item['reward_num1'] = re.search('>一等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>',res,re.S).group(1)
# 基本单注奖金
item['reward_price1'] = re.search('>一等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>',res,re.S).group(2)
#追加中奖注数
item['reward_num2'] = re.search('一等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?二等奖',res,re.S).group(1)
# 追加单注奖金
item['reward_price2'] = re.search('一等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?二等奖',res,re.S).group(2)
item['reward_level'] = 1
data.append(item)

# 二等奖:
item = {}
# 基本中奖注数
item['reward_num1'] = re.search('>二等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(1)
# 基本单注奖金
item['reward_price1'] = re.search('>二等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(2)
# 追加中奖注数
item['reward_num2'] = re.search('二等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?三等奖', res, re.S).group(1)
# 追加单注奖金
item['reward_price2'] = re.search('二等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?三等奖', res, re.S).group(2)
item['reward_level'] = 2
data.append(item)

# 三等奖:
item = {}
# 基本中奖注数
item['reward_num1'] = re.search('>三等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(1)
# 基本单注奖金
item['reward_price1'] = re.search('>三等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(2)
# 追加中奖注数
item['reward_num2'] = re.search('三等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?四等奖', res, re.S).group(1)
# 追加单注奖金
item['reward_price2'] = re.search('三等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?四等奖', res, re.S).group(2)
item['reward_level'] = 3
data.append(item)

# 四等奖:
item = {}
# 基本中奖注数
item['reward_num1'] = re.search('>四等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(1)
# 基本单注奖金
item['reward_price1'] = re.search('>四等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(2)
# 追加中奖注数
item['reward_num2'] = re.search('四等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?五等奖', res, re.S).group(1)
# 追加单注奖金
item['reward_price2'] = re.search('四等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?五等奖', res, re.S).group(2)
item['reward_level'] = 4
data.append(item)

# 五等奖:
# 基本中奖注数
item = {}
item['reward_num1'] = re.search('>五等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(1)
# 基本单注奖金
item['reward_price1'] = re.search('>五等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(2)
# 追加中奖注数
item['reward_num2'] = re.search('五等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?六等奖', res, re.S).group(1)
# 追加单注奖金
item['reward_price2'] = re.search('五等奖.*?追加.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?六等奖', res, re.S).group(2)
item['reward_level'] = 5
data.append(item)

# 六等奖:
# 基本中奖注数
item={}
item['reward_num1'] = re.search('>六等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(1)
# 基本单注奖金
item['reward_price1'] = re.search('>六等奖</td>.*?<td>基本</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>', res, re.S).group(2)
item['reward_level'] = 6
data.append(item)

for i in data:
    s = "select * from dl_super_lotto_result where term_num={} and reward_level={};".format(n,i['reward_level'])
    desc = cur.execute(s)
    if desc:
        print("不需要更新")
    else:

        if i['reward_level'] ==6:
            i['reward_price1'] = i['reward_price1'].replace(',', '')
            sql = "insert into dl_super_lotto_result(term_num,reward_level,reward_num1,reward_price1,create_time) values({},{},{},'{}','{}');".format(
                n, i['reward_level'], i['reward_num1'], i['reward_price1'],
                now_time)
        else:
            i['reward_price1'] = i['reward_price1'].replace(',', '')
            i['reward_price2'] = i['reward_price2'].replace(',', '')
            sql = "insert into dl_super_lotto_result(term_num,reward_level,reward_num1,reward_price1,reward_num2,reward_price2,create_time) values({},{},{},'{}',{},'{}','{}');".format(n,i['reward_level'],i['reward_num1'],i['reward_price1'],i['reward_num2'],i['reward_price2'],now_time)
            print('插入成功>{}'.format(n))
        try:
            cur.execute(sql)
            db.commit()
        except Exception as e:
            print(e)


cur.close()
db.close()
