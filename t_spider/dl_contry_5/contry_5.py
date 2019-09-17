# -*- coding: utf-8 -*-
import requests
import re
from pymysql import connect
from datetime import datetime
import time

now = datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')
db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
url = "http://liansai.500.com/"
res = requests.get(url).content.decode('gbk')
contrys = re.findall('(http://liansai.500.com/static/soccerdata/images/CountryPic/.*?[pb].*?)">.*?<span>(.*?)</span>',res,re.S)

j = 1
for ul,name in contrys:

    try:
        data = requests.get(url=ul).content
        with open('/Users/admin/Desktop/spider/t_spider/dl_contry_5/images/{}.jpg'.format(j),'wb') as f:
            f.write(data)
        pic = 'https://static.caixiaomi.net/foot/contry_5/{}.jpg'.format(j)
        sql = "insert into dl_contry(contry_id,contry_name,contry_pic,league_from,create_time) values({},'{}','{}',1,'{}')".format(j,name,pic,now_time)
        cur.execute(sql)
        db.commit()
        print('插入{}成功!'.format(name))
        j +=1
        time.sleep(2)
    except:
        print(name)

cur.close()
db.close()