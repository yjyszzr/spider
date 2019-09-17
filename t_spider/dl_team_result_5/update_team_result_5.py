# -*- coding: utf-8 -*-
import requests
from pymysql import connect
from lxml import etree
import time
from datetime import datetime
import re

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()


ids = [1771,2043,2082,3154,3158,3172,4333,5746,5863,7669,8224,9535,9607,9683,10211]
for i in ids:
    try:
        desc = cur.execute("select * from dl_team_result_500w where team_id ={}".format(i))
        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        team_id = i
        print(1)
        url = "http://liansai.500.com/team/{}/".format(team_id)
        res = requests.get(url).content.decode('gbk')
        item = {}
        item['team_id'] = team_id
        #成立时间
        item['team_time'] = re.search('成立时间：(.*?)</td>',res).group(1)
        #球场容量
        item['team_capacity'] = re.search('球场容量：(.*?)</td>',res).group(1)

        #国家
        item['contry'] = re.search('国家地区：(.*?)</td>',res).group(1)

        #球场
        item['court'] = re.search('球场：(.*?)</td>',res).group(1)

        #城市
        item['city'] = re.search('<td>所在城市：(.*?)</td>',res).group(1)

        #球队身价
        item['team_value'] = re.search('<td>球队身价：(.*?)</td>',res).group(1)

        if desc:
            print(i)
        else:
            sql = "insert into dl_team_result_500w(team_id,team_time,team_capacity,contry,court,city,team_value,create_time) values({},'{}','{}','{}','{}','{}','{}','{}')".format(item['team_id'],item['team_time'],item['team_capacity'],item['contry'],item['court'],item['city'],item['team_value'],now_time)

            cur.execute(sql)
            db.commit()
            print("更新{}成功".format(i))
    except Exception as e:
        print(e,i)

cur.close()
db.close()