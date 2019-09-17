# -*- coding: utf-8 -*-
import requests
import re
from pymysql import connect
import time

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
cur.execute('select league_id from dl_league_info;')
ids = cur.fetchall()
for i in ids:

    # try:
    #     league_id = i[0]
    #     url = "http://static.sporttery.cn/pres/proj/2018/201806_TeamLogo/fb/matchName/{}.jpg".format(league_id)
    #     res = requests.get(url).content
    #     with open('/Users/admin/Desktop/spider/t_spider/dl_league_info/pic/{}.jpg'.format(league_id),'wb') as f:
    #         f.write(res)
    #     print('正在写入{}'.format(league_id))
    #     time.sleep(3)
    # except Exception as e:
    #     print(e)

    try:
        league_id = i[0]
        pic = "https://static.caixiaomi.net/foot/league/{}.jpg".format(league_id)
        sql = "update dl_league_info set league_pic='{}' where league_id={}".format(pic,league_id)
        cur.execute(sql)
        db.commit()
        print("更新成功{}".format(league_id))
    except:
        pass
"""
/static/cxm_files/foot/league/{}.jpg
"""



cur.close()
db.close()
