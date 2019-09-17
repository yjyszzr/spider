# -*- coding: utf-8 -*-
import requests
from pymysql import connect
import re
from datetime import datetime


now = datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
                     charset='utf8')
cur = db.cursor()

# 1
oz = ['欧罗巴', '欧超杯', '欧冠', '欧洲杯', '世外欧洲', '欧U19', '女欧杯', '欧U17', '欧青赛', '酋长杯', '欧U21外', '奥女欧预', '欧国联']
for i in oz:
    sql = "insert into dl_league_500w(league_name,league_abbr,is_league,create_time,group_id) values('{}','{}',{},'{}',1)".format(i,i,0,now_time)
    cur.execute(sql)
    db.commit()


# 2
mz = ['金杯赛', '世外南美', '美洲杯', '解放者杯', '世外北美', '南俱杯', '南美超', '中美杯', '美冠杯']
for j in mz:
    sql = "insert into dl_league_500w(league_name,league_abbr,is_league,create_time,group_id) values('{}','{}',{},'{}',2)".format(j,j,0,now_time)
    cur.execute(sql)
    db.commit()
# 3
yz = ['女亚洲杯', '亚洲杯', '亚冠杯', '东南锦', '海湾杯', '世外亚洲', '亚协杯', '亚运女足', '亚运男足', '东亚杯', '东亚女足', '亚挑杯', '奥女亚预', '亚青U23', '日泰杯']
for k in yz:
    sql = "insert into dl_league_500w(league_name,league_abbr,is_league,create_time,group_id) values('{}','{}',{},'{}',3)".format(k,k,0,now_time)
    cur.execute(sql)
    db.commit()
# 5
fz = ['非洲杯', '世外非洲', '非冠联', '非青杯', '非国锦标', '南非协杯']

for f in fz:
    sql = "insert into dl_league_500w(league_name,league_abbr,is_league,create_time,group_id) values('{}','{}',{},'{}',5)".format(f,f,0,now_time)
    cur.execute(sql)
    db.commit()
cur.close()
db.close()