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

data = re.findall('src="http://liansai.500.com/static/soccerdata/images/CountryPic/.*?<span>(.*?)</span>.*?(<a href="/zuqiu-\d+/" target="_blank" title=".*?">.*?</a>.*?)</div>',res,re.S)

n = 1
for i,j in data:
    ls = re.findall('<a href="/zuqiu-\d+/" target="_blank" title="(.*?)">(.*?)</a>',j)
    cur.execute('select contry_id from dl_contry_500w where contry_name="{}"'.format(i))
    contry_id = cur.fetchone()[0]
    for league_name,league_abbr in ls:
        desc = cur.execute("select * from dl_league_500w where league_abbr='{}'".format(league_abbr))
        if desc:
            pass
        else:
            sql = "insert into dl_league_500w(league_id,league_name,league_abbr,contry_id,create_time) values({},'{}','{}',{},'{}')".format(n,league_name,league_abbr,contry_id,now_time)
            cur.execute(sql)
            db.commit()
            print('插入{}成功!'.format(league_abbr))
        n +=1





cur.close()
db.close()