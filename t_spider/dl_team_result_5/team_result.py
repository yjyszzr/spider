# -*- coding: utf-8 -*-
import requests
from pymysql import connect
from lxml import etree
import time
from datetime import datetime

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
cur.execute("select team_id from dl_team_500w;")
ids = cur.fetchall()

for i in ids:
    try:
        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        team_id = i[0]
        url = "http://liansai.500.com/team/{}/".format(team_id)
        res = requests.get(url).content
        html = etree.HTML(res)
        item = {}
        item['team_id'] = team_id
        #成立时间
        item['team_time'] = html.xpath('//div[@class="itm_bd"]//tr[1]/td[1]/text()')[0].replace('成立时间：','')
        #球场容量
        item['team_capacity'] = html.xpath('//div[@class="itm_bd"]//tr[1]/td[2]/text()')[0].replace('球场容量：','')
        #国家
        item['contry'] = html.xpath('//div[@class="itm_bd"]//tr[2]/td[1]/text()')[0].replace('国家地区：','')
        #球场
        item['court'] = html.xpath('//div[@class="itm_bd"]//tr[2]/td[2]/text()')[0].replace('球场：','')
        #城市
        item['city'] = html.xpath('//div[@class="itm_bd"]//tr[3]/td[1]/text()')[0].replace('所在城市：','')
        #球队身价
        item['team_value'] = html.xpath('//div[@class="itm_bd"]//tr[3]/td[2]/text()')[0].replace('球队身价：','')
        sql = "insert into dl_team_result_500w(team_id,team_time,team_capacity,contry,court,city,team_value,create_time) values({},'{}','{}','{}','{}','{}','{}','{}')".format(item['team_id'],item['team_time'],item['team_capacity'],item['contry'],item['court'],item['city'],item['team_value'],now_time)
        cur.execute(sql)
        db.commit()
        time.sleep(2)
    except Exception as e:
        with open('team_id.txt','a') as f:
            f.write(str(team_id))


cur.close()
db.close()