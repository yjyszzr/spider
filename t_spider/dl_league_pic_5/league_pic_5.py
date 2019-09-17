# -*- coding: utf-8 -*-
import requests
import json
import time
import re
from pymysql import connect

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
erro = []
for i in range(0,6):
    url = "https://ews.500.com/library/zq/leagues?areaid={}".format(i)
    res = requests.get(url).content.decode()
    datas = re.findall('"matchgbname": "(.*?)".*?"matchlogo": "(.*?)"',res,re.S)
    for name,pic in datas:
        try:
            cur.execute("select league_id from dl_league_500w where league_name='{}';".format(name))
            league_id = cur.fetchone()[0]
            dat = requests.get(url=pic).content
            with open('/Users/admin/Desktop/spider/t_spider/dl_league_pic_5/league_image/{}.png'.format(league_id),'wb') as f:
                f.write(dat)
                print('正在写入{}'.format(name))
        except:
            erro.append(name)

print(erro)