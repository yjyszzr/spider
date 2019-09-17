# -*- coding: utf-8 -*-
import requests
from pymysql import connect
import time
import json
import re
import datetime


# 今天
today = datetime.date.today()
day = datetime.timedelta(days=1)
# 明日
m_day = str(today + day)
# 后天
h_day = str(today + day + day)
# 大后天
d_day = str(today + day + day + day)
db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
cur.execute("select home_team_id,visiting_team_id from dl_match where match_time like '{}%' or match_time like '{}%' or match_time like '{}%';".format(today,m_day,h_day,d_day))
ids = cur.fetchall()
s_ids = []
for h_id,a_id in ids:
    s_ids.append(h_id)
    s_ids.append(a_id)

for id in s_ids:
    try:
        s = "select team_id from dl_league_team where sporttery_teamid={};".format(id)
        cur.execute(s)
        team_id = cur.fetchone()[0]
        url = 'http://i.sporttery.cn/api/fb_match_info/get_future_matches?tid={}&limit=30'.format(team_id)
        res = requests.get(url=url).content.decode()
        dict_data = json.loads(res)
        result = dict_data['result']
        for item in result:
            match_id = item['match_id']
            match_date = item['date_cn']
            match_time = item['time_cn']
            game_week = item['gameweek']
            sporttery_matchid = item['sporttery_matchid']
            league_name = item['l_cn']
            league_abbr = item['l_cn_abbr']
            league_id = item['l_id_dc']
            home_team_name = item['h_cn']
            home_team_abbr = item['h_cn_abbr']
            home_team_id = item['h_id_dc']
            visitor_team_name = item['a_cn']
            visitor_team_abbr = item['a_cn_abbr']
            visitor_team_id = item['a_id_dc']
            create_time = int(time.time())
            sql = "insert into dl_future_match(match_id,match_date,match_time,game_week,sporttery_matchid,league_name,league_abbr,league_id,home_team_name,home_team_abbr,home_team_id,visitor_team_name,visitor_team_abbr,visitor_team_id,create_time) values({},'{}','{}','{}',{},'{}','{}',{},'{}','{}',{},'{}','{}',{},{});".format(match_id,match_date,match_time,game_week,sporttery_matchid,league_name,league_abbr,league_id,home_team_name,home_team_abbr,home_team_id,visitor_team_name,visitor_team_abbr,visitor_team_id,create_time)
            try:
                cur.execute(sql)
                db.commit()
                print("插入>>%s成功"%item['match_id'])
            except:
                pass
    except Exception as e:
        print("%s"%e)
    time.sleep(1)
cur.close()
db.close()


