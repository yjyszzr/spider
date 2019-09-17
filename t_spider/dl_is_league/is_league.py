# -*- coding: utf-8 -*-
import requests
from pymysql import connect
from lxml import etree
import re

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
url = "http://liansai.500.com/zuqiu-4826/"
res = requests.get(url).content.decode('gbk')
ls = []
cur.execute('select league_abbr from dl_league_500w')
addr = cur.fetchall()
for i in addr:
    name = i[0]
    ls.append(name)

#联赛
datas = re.findall('<select id="select_notcups".*?</select>',res,re.S)[0]
notcups = re.findall('<option.*?>. (.*?)</option>',datas)
for n in notcups:
    if n in ls:
        sql = 'update dl_league_500w set is_league=1 where league_abbr="{}";'.format(n)
        cur.execute(sql)
        db.commit()
        print('更新联赛>{}<成功'.format(n))
    else:
        pass
#杯赛
data = re.findall('<select id="select_cups".*?</select>',res,re.S)[0]
cups = re.findall('<option.*?>. (.*?)</option>',data)
for c in cups:
    if c in ls:
        sql = 'update dl_league_500w set is_league=0 where league_abbr="{}";'.format(c)
        cur.execute(sql)
        db.commit()
        print('更新杯赛>{}<成功'.format(c))
    else:
        pass


cur.close()
db.close()