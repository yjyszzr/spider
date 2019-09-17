# -*- coding: utf-8 -*-
import requests
import re
from pymysql import connect
import json
import time

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
data_list = []
for i in range(0,6):
    url = "https://ews.500.com/library/zq/leagues?areaid={}".format(i)
    res = requests.get(url=url).content.decode()
    data = json.loads(res)['data']
    for d in data:
        try:
            item ={}
            item['league_id'] = d['leagueid']
            item['league_name'] = d['matchgbname']
            data_list.append(item)
        except:
            for j in d['leaguelist']:
                item = {}
                item['league_id'] = j['leagueid']
                item['league_name'] = j['matchgbname']
                data_list.append(item)
for l in data_list:
    sql = "update dl_league_500w set l_id={} where league_name='{}'".format(l['league_id'],l['league_name'])
    cur.execute(sql)
    db.commit()

cur.close()
db.close()