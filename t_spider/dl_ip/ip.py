# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree
import time
from pymysql import connect
from datetime import datetime

now = now = datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')

url = "http://ipblock.chacuo.net/"
data = requests.get(url=url).content.decode()
html = etree.HTML(data)
http_list = html.xpath("//ul[@class='list clearfix inline-block']/li/a/@href")
db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
for h in http_list:
    d = h.replace('http://ipblock.chacuo.net/view/','')
    ul = "http://ipblock.chacuo.net/down/t_txt={}".format(d)
    contry = str(d)
    s = "select * from dl_ip where contry='{}';".format(contry)
    desc = cur.execute(s)
    try:
        res = requests.get(url=ul).content.decode()
        lists = re.findall('(\d+\.\d+\.\d+\.\d+).*?(\d+\.\d+\.\d+\.\d+).*?(\d+\.\d+\.\d+\.\d+/\d+).*?(\d+)',res)
        if lists:
            for start_ip,end_ip,network,ip_num in lists:
                start_ip = str(start_ip)
                end_ip = str(end_ip)
                network = str(network)
                if desc:
                    pass
                else:
                    sql = "insert into dl_ip(start_ip,end_ip,network,ip_num,contry,s_ip,e_ip,create_time) values(INET_ATON('{}'),INET_ATON('{}'),'{}',{},'{}','{}','{}','{}')".format(start_ip,end_ip,network,ip_num,contry,start_ip,end_ip,now_time)
                cur.execute(sql)
                db.commit()
    except:
        print('暂无数据')
    time.sleep(2)



