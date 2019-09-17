# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from pymysql import connect
import  re
now = datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
url = 'http://liansai.500.com/'
res = requests.get(url=url).content.decode('gbk')
t = re.findall('class="lrace_bei".*?id="match-cup-\d+".*?</table>',res,re.S)
ls = []
for i in t:
    l = re.findall('/zuqiu-(\d+)/".*?>(.*?)</a></td>',i)
    ls += l
for i,j in ls:
    u = "http://liansai.500.com/zuqiu-{}/teams/".format(i)
    cur.execute("select league_id from dl_league_500w where league_abbr='{}'".format(j))
    league_id = cur.fetchone()
    r = requests.get(url=u).content.decode('gbk')

    print(i,j)


cur.close()
db.close()