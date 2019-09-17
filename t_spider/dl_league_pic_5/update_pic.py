# -*- coding: utf-8 -*-
from pymysql import connect


db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
cur.execute("select league_id from dl_league_500w")
ids = cur.fetchall()
for i in ids:
    league_id = i[0]
    pic = "https://static.caixiaomi.net/foot/league_5/{}.png".format(league_id)
    sql = "update dl_league_500w set league_pic='{}' where league_id = {}".format(pic,league_id)
    cur.execute(sql)
    db.commit()


cur.close()
db.close()