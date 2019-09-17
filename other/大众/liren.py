# -*- coding: utf-8 -*-
import requests
import re
import time
from pymysql import connect


db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
'Cookie': '__mta=50050841.1534748454662.1534748454662.1534748454662.1"; _lxsdk_cuid=165557ad977c8-0996aa2a73f718-34637908-1fa400-165557ad977c8; _lxsdk=165557ad977c8-0996aa2a73f718-34637908-1fa400-165557ad977c8; _hc.v=1174f365-74e9-1970-3c3f-64a9f1f6ff2d.1534737439; s_ViewType=10; cityid=2; msource=default; aburl=1; cy=2; cye=beijing; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1534748434; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1534748434; wedchatguest=g35443343548443078; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; logan_custom_report=; default_ab=shop%3AA%3A1%7Cindex%3AA%3A1%7CshopList%3AA%3A1; switchcityflashtoast=1; source=m_browser_test_33; logan_session_token=nr4yk5ob4iidr1jmqikl; _lxsdk_s=1655612fa5a-2a0-d79-d7d%7C%7C3948'
}
shops = []
num = 1
while num <51:
    url = "http://www.dianping.com/beijing/ch50/p{}".format(num)
    data = requests.get(url=url,headers=header).content.decode()
    d = re.findall('www.dianping.com/shop/\d+',data)
    ls = set(d)
    ll = list(ls)
    shops += ll
    print('正在存储{}'.format(num))
    num +=1
    time.sleep(1)

for ul in shops:
    try:
        url = 'http://'+ul
        #分类
        cla = '丽人'
        city = '北京'
        res = requests.get(url=url,headers=header).content.decode()
        tel = re.search('class="icon-phone">(.*?)</span>',res).group(1)
        shop_name = re.search('<h1.*?class="shop-title".*?>(.*?)</h1>',res).group(1)

        sql = "insert into dazhong(city,tel,shop_name,class) values('{}','{}','{}','{}')".format(city,tel,shop_name,cla)
        cur.execute(sql)
        db.commit()
        print("正在存储{}".format(sql))
    except Exception as e:
        with open('ero_url.txt','a') as ff:
            ff.write(ul+',\n')
        print('错误%s'%e)
    time.sleep(3)

cur.close()
db.close()

