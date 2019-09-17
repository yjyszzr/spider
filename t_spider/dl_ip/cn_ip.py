# -*- coding: utf-8 -*-
import requests
from lxml import etree
import time
import re
from pymysql import connect
from datetime import datetime


now = now = datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
urls = [
    '/cn/tianjin/',
    '/cn/beijing/',
    '/cn/shanghai/',
    '/cn/xianggang/',
    '/cn/chongqing/',
]
for i in urls:
    try:
        url = 'http://ip.yqie.com' + i
        res = requests.get(url=url).content.decode()
        html = etree.HTML(res)
        nodes = html.xpath('//*[@id="GridViewOrder"]//tr')
    except Exception as e:
        print(e)
        nodes = []
    for node in nodes:
        try:
            s_ip = node.xpath('./td[2]/text()')[0]
            e_ip = node.xpath('./td[3]/text()')[0]
            address = node.xpath('./td[4]/text()')[0]
            province_code = re.search('http://ip.yqie.com/cn/(.*?)/',url).group(1)
            city_code = re.search('http://ip.yqie.com/cn/(.*?)/',url).group(1)
            sql = "insert into dl_china_ip(start_ip,end_ip,province_code,city_code,address,s_ip,e_ip,create_time) values(INET_ATON('{}'),INET_ATON('{}'),'{}','{}','{}','{}','{}','{}')".format(s_ip,e_ip,province_code,city_code,address,s_ip,e_ip,now_time)
            cur.execute(sql)
            db.commit()
            print('插入成功>{}'.format(address))
        except:
            print('暂无数据')

    time.sleep(3)

cur.close()
db.close()