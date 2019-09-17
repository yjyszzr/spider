# -*- coding: utf-8 -*-
from pymysql import connect
import re

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')

cur = db.cursor()
cur.execute("select sporttery_teamid from dl_league_team")
ids = cur.fetchall()

s1 = []
for i, in ids:
    s1.append(str(i))
ss = set(s1)
s2 = list(ss)

for j in s2:
    l = re.findall('%s'%str(j),str(s1))
    print(l)

