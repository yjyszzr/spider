# -*- coding: utf-8 -*-
import requests
from pymysql import connect
import os
import json
import time
#正式
# db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',charset='utf8')

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
cur.execute('select changci_id from dl_match where DATEDIFF(show_time,NOW()) >= 0 and is_del = 0 and is_show=1 and TIMESTAMPDIFF(MINUTE, match_time, NOW()) < 10')
ids = cur.fetchall()
ls = os.listdir('/static/cxm_files/foot/team/full')
teams = []
for i in ls:
    try:
        team_id = i.replace('.jpg','')
        teams.append(team_id)
    except:
        pass

for i in ids:
    try:
        changci_id = i[0]
        url = "http://i.sporttery.cn/api/fb_match_info/get_match_info?mid={}".format(changci_id)
        res = requests.get(url).content.decode()
        d = json.loads(res)["result"]
        h_id = str(d['h_id_dc'])
        a_id = str(d['a_id_dc'])

        if d['h_pic']:
            if h_id not in teams:
                p1 = requests.get(url=d['h_pic']).content
                with open('/static/cxm_files/foot/team/full/{}.jpg'.format(h_id),'wb') as e:
                    print('changciid:{}正在写入{}'.format(changci_id,h_id))
                    e.write(p1)
        if d['a_pic']:
            if a_id not in teams:
                p2 = requests.get(url=d['a_pic']).content
                with open('/static/cxm_files/foot/team/full/{}.jpg'.format(a_id), 'wb') as f:
                    print("changciid:{}正在写入{}".format(changci_id,a_id))
                    f.write(p2)
        time.sleep(2)
    except:
        pass

cur.close()
db.close()