# -*- coding: utf-8 -*-
import requests
from pymysql import connect
import re
import time
from lxml import etree
import time
from datetime import datetime

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
url = "http://liansai.500.com/"
res = requests.get(url=url).content.decode('gbk')
lists = re.findall('/zuqiu-(\d+)',res)
ls = set(lists)
lists = list(ls)
now = now = datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')
for league_id in lists:
    url = "http://liansai.500.com/zuqiu-{}/teams/".format(league_id)
    data = requests.get(url=url).content.decode('gbk')
    league_name = re.search('"/zuqiu-\d+/">(.*?)首页</a>',data).group(1).strip()

    html = etree.HTML(data)
    node_list = html.xpath('//tbody/tr')
    for node in node_list:
        try:
            item = {}
            item['league_id'] = league_id
            item['league_name'] = league_name
            item['price_rank'] = node.xpath('./td[1]/text()')[0]
            item['team_name'] = node.xpath('./td[2]/a/text()')[0]
            item['team_price'] = node.xpath('./td[3]/span/text()')[0]
            item['team_avg_price'] = node.xpath('./td[4]/span/text()')[0]
            item['team_num'] = node.xpath('./td[5]/text()')[0]
            item['avg_age'] = node.xpath('./td[6]/text()')[0]
            item['league_rank'] = node.xpath('./td[7]/text()')[0]
            item['team_score'] = node.xpath('./td[8]/text()')[0]
            s = "select * from dl_team_price where league_id='{}' and team_name = '{}';".format(item['league_id'],item['team_name'])
            desc = cur.execute(s)
            if desc:
                sql = "update dl_team_price set price_rank='{}',team_price='{}',team_avg_price='{}',team_num='{}',avg_age='{}',league_rank='{}',team_score='{}',update_time='{}' where league_id='{}' and team_name='{}';".format(item['price_rank'],item['team_price'],item['team_avg_price'],item['team_num'],item['avg_age'],item['league_rank'],item['team_score'],now_time,item['league_id'],item['team_name'])
                ts = "更新>{}<成功".format(item['team_name'])
            else:
                sql = "insert into dl_team_price(league_id,league_name,price_rank,team_name,team_price,team_avg_price,team_num,avg_age,league_rank,team_score,create_time,update_time) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(item['league_id'],item['league_name'],item['price_rank'],item['team_name'],item['team_price'],item['team_avg_price'],item['team_num'],item['avg_age'],item['league_rank'],item['team_score'],now_time,now_time)
                ts = "插入>{}<成功".format(item['team_name'])
            cur.execute(sql)
            db.commit()
            print(ts)
        except:
            pass

    time.sleep(1)
cur.close()
db.close()