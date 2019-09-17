# -*- coding: utf-8 -*-
import requests
from pymysql import connect
import re
import time
from datetime import datetime

now = datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
ul = "http://liansai.500.com/"
rs = requests.get(url=ul).content.decode('gbk')
ids = re.findall('zuqiu-(\d+)',rs)
ids = set(ids)
ids = list(ids)

for id in ids:
    time.sleep(2)
    url = "http://liansai.500.com/zuqiu-{}/teams/".format(id)
    res = requests.get(url).content.decode('gbk')
    data = re.findall('http://liansai.500.com/team/(\d+)/">(.*?)</a></td>',res)
    for team_id,team_name in data:
        try:
            sql = "insert into dl_team_500w(team_id,team_name,season_id,create_time) values({},'{}',{},'{}')".format(team_id,team_name,id,now_time)
            cur.execute(sql)
            db.commit()
            print('插入{}成功'.format(team_id))
        except:
            pass





cur.close()
db.close()








